from typing import List, Optional
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
import pandas as pd
from io import StringIO
from upgini.http import get_rest_client, SearchProgress, ProgressStage, LoggerFactory
from upgini.errors import ValidationError
import logging
from upgini import SearchKey

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from email_modal import show_email_modal  # noqa: E402
from features_enricher import fetch_results, run_search  # noqa: E402
from ner_search_key_detector import auto_detect_search_keys  # noqa: E402

stages_messages = {
    ProgressStage.START_FIT.value: "Checking labeled dataset...",
    # temporary workaround
    "CREATING": "Uploading labeled dataset...",
    ProgressStage.CREATING_FIT.value: "Uploading labeled dataset...",
    ProgressStage.MATCHING.value: "Matching with data sources",
    ProgressStage.SEARCHING.value: "Searching relevant features...",
    ProgressStage.GENERATING_REPORT.value: "Generating report...",
    # temporary workaround
    ProgressStage.DOWNLOADING.value: "Generating report...",
    ProgressStage.FINISHED.value: "Finished",
    ProgressStage.FAILED.value: "Failed",
}

if "logger" not in st.session_state:
    try:
        st.session_state.logger = LoggerFactory().get_logger(api_token=st.secrets["UPGINI_API_KEY"])
    except Exception:
        st.session_state.logger = logging.getLogger()
if "df" not in st.session_state:
    st.session_state.df = None
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
if "relevant_fields" not in st.session_state:
    st.session_state.relevant_fields = None
if "raw_relevant_fields" not in st.session_state:
    st.session_state.raw_relevant_fields = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "file_uploader_disabled" not in st.session_state:
    st.session_state.file_uploader_disabled = False
if "text_area_disabled" not in st.session_state:
    st.session_state.text_area_disabled = False
if "text_area_reset_visible" not in st.session_state:
    st.session_state.text_area_reset_visible = False
if "exclude_columns_selector" not in st.session_state:
    st.session_state.exclude_columns_selector = None
if "enricher" not in st.session_state:
    st.session_state.enricher = None
if "data_for_fit" not in st.session_state:
    st.session_state.data_for_fit = None
if "progress_bar" not in st.session_state:
    st.session_state.progress_bar = None


def upload_file_submit(*args, **kwargs):
    file_uploader_state = st.session_state.get("file_uploader")
    st.session_state.relevant_fields = None
    st.session_state.raw_relevant_fields = None
    st.session_state.summary = None
    st.session_state.text_area_disabled = file_uploader_state is not None
    st.session_state.data_loaded = file_uploader_state is not None


def upload_text_submit(*args, **kwargs):
    st.session_state.relevant_fields = None
    st.session_state.raw_relevant_fields = None
    st.session_state.file_uploader_disabled = True
    st.session_state.text_area_reset_visible = True
    st.session_state.data_loaded = True
    # do smth here


def text_area_reset(*args, **kwargs):
    st.session_state.file_uploader_disabled = False
    st.session_state.text_area_reset_visible = False
    st.session_state["text_area"] = ""
    st.session_state.relevant_fields = None
    st.session_state.raw_relevant_fields = None
    st.session_state.summary = None
    st.session_state.data_loaded = False


def has_double_usage(cols: list) -> bool:
    non_empty_cols = [c for c in cols if c is not None and len(c) > 0]
    return len(non_empty_cols) != len(set(non_empty_cols))


try:
    st.set_page_config(page_icon="🔎", page_title="Find the right data listing")

    # For proxima-nova font
    st.markdown(
        """<link rel="stylesheet" href="https://use.typekit.net/qls3unz.css" media="all" />""",
        unsafe_allow_html=True,
    )

    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    uploaded_file = None
    df_text = None
    ip_col = None
    date_col = None
    target_col = None
    exclude_columns = []
    detected_search_keys = []
    detected_generate_features = []
    df = st.session_state.df

    if "search_started" not in st.session_state or not st.session_state.search_started:
        if not st.session_state.data_loaded:
            exm_container = st.expander(
                (
                    ":green[Use your labeled training dataset for ML task with Date, Country, "
                    "Postal code and Label columns.]\n "
                    "**:green[Click for example how to format dataset 👇 or]** "
                    "**:green[[check docs]"
                    "(https://github.com/upgini/upgini#2--use-your-labeled-training-dataset-for-search)]**"
                ),
                expanded=False,
            )
            sample = {
                "Date (STRING)": [
                    "2023.01.01",
                    "2023.01.02",
                    "2023.01.03",
                ],
                "Country (STRING)": ["EC", "GB", "JP"],
                "Postal code (STRING)": [
                    "170515",
                    "PO16 7GZ",
                    "730-8511",
                ],
                "Label (INT, FLOAT, STRING)": [0, 1, 0],
            }
            if sample:
                exm_container.write(pd.DataFrame(sample))

    if "search_started" not in st.session_state or not st.session_state.search_started:
        c1, c2, c3 = st.columns([6, 1, 6])
        with c1:
            uploaded_file: UploadedFile = st.file_uploader(
                ":blue[**Drop / Upload file**]",
                key="file_uploader",
                type=["csv", "csv.zip", "csv.gz", "tar.gz", "parquet", "xlsx", "xls"],
                disabled=st.session_state.file_uploader_disabled,
                on_change=upload_file_submit,
            )
            if uploaded_file is not None:
                try:
                    if ".parquet" in uploaded_file.name:
                        df_file = pd.read_parquet(uploaded_file)
                    elif ".xls" in uploaded_file.name:
                        df_file = pd.read_excel(uploaded_file)
                    else:
                        try:
                            df_file = pd.read_csv(uploaded_file, sep=None, engine="python")
                        except Exception:
                            try:
                                df_file = pd.read_csv(
                                    uploaded_file,
                                    sep=None,
                                    engine="python",
                                    compression="zip",
                                )
                            except Exception:
                                df_file = pd.read_csv(
                                    uploaded_file,
                                    sep=None,
                                    engine="python",
                                    compression="gzip",
                                )
                    st.session_state.logger.info("Dataframe read from uploaded file")
                except Exception:
                    st.session_state.logger.exception("Failed to read uploaded file")
                    st.warning("Unsupported file format")
                    uploaded_file = None

        with c2:
            st.write("**OR**")

        with c3:
            text_area_height = 112 if st.session_state.text_area_reset_visible else 171
            text_area_text = (
                (st.session_state.get("text_area") or "") if st.session_state.text_area_reset_visible else ""
            )

            uploaded_text = st.text_area(
                ":blue[**Paste from spreadsheet or table**]",
                height=text_area_height,
                value=text_area_text,
                placeholder="\n✅ Paste here",
                key="text_area",
                disabled=st.session_state.text_area_disabled,
                on_change=upload_text_submit,
            )

            if st.session_state.text_area_reset_visible:
                st.button(
                    "Reset text input",
                    on_click=text_area_reset,
                    type="primary",
                    use_container_width=True,
                    kwargs={},
                )

            if uploaded_text:
                df_text = pd.read_csv(StringIO(uploaded_text), sep=None, engine="python")
                st.session_state.logger.info("Dataframe read from input text")

        if uploaded_file:
            file_container = st.expander("Preview uploaded dataset")
            uploaded_file.seek(0)
            file_container.write(df_file.head(100))
            df = df_file
        elif df_text is not None and len(df_text) > 0:
            file_container = st.expander("Preview uploaded dataset")
            file_container.write(df_text.head(100))
            df = df_text
        else:
            df = None
        st.session_state.df = df

        if df is not None:
            if "Unnamed: 0" in df.columns:
                df = df.drop(columns="Unnamed: 0")
            with st.spinner("Detecting column types..."):
                detected_search_keys, detected_generate_features = auto_detect_search_keys(
                    df, st.secrets["OPENAI_API_KEY"], _logger=st.session_state.logger
                )
                st.session_state.logger.info(f"Autodetected search keys: {detected_search_keys}")
                st.session_state.logger.info(f"Autodetected generate features: {detected_generate_features}")

            c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
            with c1:
                date_index = 0
                columns_for_date = [""] + df.columns.to_list()
                if st.session_state.get("date_selector") is not None:
                    date_index = columns_for_date.index(st.session_state.get("date_selector"))
                else:
                    for col in df.columns:
                        if detected_search_keys.get(col) in ["DATE", "DATETIME"]:
                            date_index = columns_for_date.index(col)
                            break
                date_col = st.selectbox(
                    "Date/Datetime",
                    columns_for_date,
                    key="date_selector",
                    index=date_index,
                )
            with c2:
                country_index = 0
                columns_for_country = [""] + df.columns.to_list()
                if st.session_state.get("country_selector") is not None:
                    country_index = columns_for_country.index(st.session_state.get("country_selector"))
                else:
                    for col in columns_for_country:
                        if detected_search_keys.get(col) in ["COUNTRY"]:
                            country_index = columns_for_country.index(col)
                            break
                country_col = st.selectbox(
                    "Country",
                    columns_for_country,
                    key="country_selector",
                    index=country_index,
                )
            with c3:
                postal_index = 0
                columns_for_postal = [""] + df.columns.to_list()
                if st.session_state.get("postal_selector") is not None:
                    postal_index = columns_for_postal.index(st.session_state.get("postal_selector"))
                else:
                    for col in columns_for_postal:
                        if detected_search_keys.get(col) in ["POSTAL_CODE"]:
                            postal_index = columns_for_postal.index(col)
                            break
                postal_col = st.selectbox(
                    "Postal code",
                    columns_for_postal,
                    key="postal_selector",
                    index=postal_index,
                )
            with c4:
                target_index = 0
                columns_for_target = df.columns.to_list()
                if st.session_state.get("target_selector") is not None:
                    target_index = columns_for_target.index(st.session_state.get("target_selector"))
                else:
                    for key, value in enumerate(columns_for_target):
                        if "target" in str(value).lower():
                            target_index = key
                target_col = st.selectbox(
                    "Target label*",
                    columns_for_target,
                    key="target_selector",
                    index=target_index,
                )

            columns_to_exclude = [x for x in df.columns if x not in [ip_col, target_col]]
            exclude_columns = []
            if len(columns_to_exclude) > 0:
                values: Optional[List[str]] = st.session_state.get("exclude_columns_selector")
                if values and date_col and date_col in values:
                    st.session_state.exclude_columns_selector = []
                exclude_columns = st.multiselect(
                    "Columns to exclude", columns_to_exclude, key="exclude_columns_selector"
                )

            columns_for_generate = [
                x
                for x in detected_generate_features.keys()
                if x not in [date_col, country_col, postal_col, target_col] + (exclude_columns or [])
            ]
            generate_features = []
            if len(columns_for_generate) > 0:
                generate_features = st.multiselect(
                    "Columns for features generation (max 10)",
                    columns_for_generate,
                    key="generate_features_selector",
                )

            search_btn = st.button("Search", type="primary")
            if search_btn:
                st.session_state.logger.info("Started search from Widget")
                df_copy = df.copy()
                if has_double_usage([date_col, country_col, postal_col, target_col]):
                    st.error("The same column cannot be used multiple times")
                    st.stop()
                if target_col is None:
                    st.error("Target column is empty")
                    st.stop()
                if date_col is None or len(date_col) == 0:
                    date_col = None
                if country_col is None or len(country_col) == 0:
                    country_col = None
                if postal_col is None or len(postal_col) == 0:
                    postal_col = None
                if date_col is None and country_col is None and postal_col is None:
                    st.error("At least one search key should be selected")
                    st.stop()
                if postal_col is not None and country_col is None:
                    st.error("Country search key required if Postal code is present")
                    st.stop()
                if len(generate_features) > 10:
                    st.error("Too many columns selected for feature generation")
                    st.stop()

                def rename_columns(from_, df_, date_col_, country_col_, postal_col_, target_col_):
                    to_ = f"client_{from_}"
                    df_ = df_.rename(columns={from_: to_})
                    if date_col_ == from_:
                        date_col_ = to_
                    if country_col_ == from_:
                        country_col_ = to_
                    if postal_col_ == from_:
                        postal_col_ = to_
                    if target_col_ == from_:
                        target_col_ = to_
                    if from_ in generate_features:
                        generate_features.remove(from_)
                        generate_features.append(to_)
                    return df_, date_col_, country_col_, postal_col_, target_col_

                # Rename system columns
                if "system_record_id" in df_copy.columns and "system_record_id" not in (exclude_columns or []):
                    df_copy, date_col, country_col, postal_col, target_col = rename_columns(
                        "system_record_id", df_copy, date_col, country_col, postal_col, target_col
                    )
                if "eval_set_index" in df_copy.columns and "eval_set_index" not in (exclude_columns or []):
                    df_copy, date_col, country_col, postal_col, target_col = rename_columns(
                        "eval_set_index", df_copy, date_col, country_col, postal_col, target_col
                    )
                if (
                    "target" in df_copy.columns
                    and "target" != target_col
                    and "target" not in (exclude_columns or [])
                ):
                    df_copy, date_col, country_col, postal_col, target_col = rename_columns(
                        "target", df_copy, date_col, country_col, postal_col, target_col
                    )

                if exclude_columns is not None and len(exclude_columns) > 0:
                    df_copy = df_copy.drop(columns=[c for c in exclude_columns if c in df_copy.columns])

                st.session_state.relevant_fields = None
                st.session_state.raw_relevant_fields = None
                st.session_state.summary = None
                st.session_state.search_started = True
                st.session_state.data_for_fit = (
                    df_copy,
                    target_col,
                    date_col,
                    country_col,
                    postal_col,
                    generate_features,
                )
                st.experimental_rerun()

    def reset_input():
        st.session_state.search_started = False
        st.session_state.relevant_fields = None
        st.session_state.raw_relevant_fields = None
        st.session_state.summary = None
        st.session_state.text_area_disabled = False
        st.session_state.file_uploader_disabled = False
        st.session_state.df = None
        st.session_state.progress_bar = None
        st.session_state.data_for_fit = None
        if (
            ("search_finished" not in st.session_state or not st.session_state.search_finished)
            and "enricher" in st.session_state
            and st.session_state.enricher is not None
            and st.session_state.enricher._search_task is not None
        ):
            print("Cancel search task...")
            get_rest_client(api_token=st.session_state.enricher.api_key).stop_search_task_v2(
                "", st.session_state.enricher._search_task.search_task_id
            )
            st.session_state.enricher = None
        else:
            print("Search for cancel not found")
        st.session_state.search_finished = False

    def progress_callback(progress: SearchProgress):
        if "search_started" not in st.session_state or not st.session_state.search_started:
            print("Search canceled. Stop progress")
            raise KeyboardInterrupt()
        if "progress_bar" in st.session_state and st.session_state.progress_bar is not None:
            message = f"{int(progress.percent)}% {stages_messages[progress.stage]}"
            if progress.error_message is not None:
                message = f"{message} {progress.error_message}"
            st.session_state.progress_bar.progress(progress.percent / 100.0, message)
            if progress.eta is not None and "estimated_remaining_time" in st.session_state:
                st.session_state.estimated_remaining_time.markdown(
                    f"<p style='font-size: 14px'>Approximately {progress.eta_time()} remaining</p>",
                    unsafe_allow_html=True,
                )

    if "search_started" in st.session_state and st.session_state.search_started:
        if (
            "data_for_fit" in st.session_state
            and st.session_state.data_for_fit is not None
            and ("search_finished" not in st.session_state or not st.session_state.search_finished)
        ):
            st.session_state.progress_bar = st.progress(0.01, "0% Checking labeled dataset...")
            st.session_state.estimated_remaining_time = st.empty()

        st.button("Reset Search", on_click=reset_input)

        if st.session_state.data_for_fit is not None:
            try:
                (
                    df_copy,
                    target_col,
                    date_col,
                    country_col,
                    postal_col,
                    generate_features,
                ) = st.session_state.data_for_fit
                search_keys = dict()
                if date_col is not None:
                    search_keys[date_col] = SearchKey.DATE
                if country_col is not None:
                    search_keys[country_col] = SearchKey.COUNTRY
                if postal_col is not None:
                    search_keys[postal_col] = SearchKey.POSTAL_CODE

                st.session_state.enricher = run_search(
                    df_copy,
                    target_col,
                    search_keys,
                    generate_features,
                    progress_callback=progress_callback,
                )
            except ValidationError as e:
                st.warning(e)
                st.stop()
                # st.session_state.search_started = False
                # st.experimental_rerun()
                # st.warning(e)
            except Exception:
                st.warning("Internal error. Try again later")
                st.stop()
                # st.session_state.search_started = False
                # st.experimental_rerun()

        if (
            "enricher" in st.session_state
            and st.session_state.enricher is not None
            and ("search_finished" not in st.session_state or not st.session_state.search_finished)
        ):
            relevant_fields, summary, raw_relevant_fields = fetch_results(st.session_state.enricher)
            st.session_state.progress_bar = None
            st.session_state.data_for_fit = None
            st.session_state.relevant_fields = relevant_fields
            st.session_state.raw_relevant_fields = raw_relevant_fields
            st.session_state.summary = summary
            st.session_state.search_finished = True
            st.experimental_rerun()

    if "relevant_fields" in st.session_state and st.session_state.relevant_fields is not None:
        if len(st.session_state.relevant_fields) == 0:
            st.write("Your search did not find any relevant fields in the data listings for you ML task")
            st.markdown(
                """Suggestions:
    - Make sure that the labeled dataset is correct
    - Ensure that the columns with IPv4 and Target label are correctly chosen
    - Exclude any columns that are not IPv4 or the Target label
    - Try to add more rows to a labeled dataset
    - Try adding a date/datetime column to the labeled dataset
    """
            )
            if st.session_state.df is not None:
                file_container = st.expander("Preview uploaded dataset", expanded=True)
                file_container.write(st.session_state.df.sample(n=4))

        else:
            if (
                "summary" in st.session_state
                and st.session_state.summary is not None
                and len(st.session_state.summary) > 0
            ):
                st.subheader("Relevant data sources")

                open_modal = None
                proportions = [1, 1, 1, 1, 1.5]
                columns = st.columns(proportions)
                for col, name in zip(columns, st.session_state.summary.columns):
                    if name != "Action":
                        col.write(f"**{name}**")
                    else:
                        col.markdown("<b style='color: white'>Action</b>", unsafe_allow_html=True)
                button_counter = 1
                open_modals = []
                for i, row in st.session_state.summary.iterrows():
                    next_columns = st.columns(proportions)
                    for col, value in zip(next_columns, row):
                        if value == "Request a quote":
                            with col:
                                open_modal = st.button(
                                    "Request a quote", key=f"request_quote_{button_counter}", type="primary"
                                )
                                open_modals.append(open_modal)
                                button_counter += 1
                        else:
                            if isinstance(value, float):
                                value = round(value, 6)
                            col.markdown(value, unsafe_allow_html=True)

                show_email_modal(any(open_modals), st.session_state.raw_relevant_fields)

            st.subheader("Relevant features")
            proportions = [3, 1, 3]
            columns = st.columns(proportions)
            for col, name in zip(columns, st.session_state.relevant_fields.columns):
                if name:
                    col.write(f"**{name}**")
                else:
                    col.markdown("</p>", unsafe_allow_html=True)
            for i, row in st.session_state.relevant_fields.iterrows():
                next_columns = st.columns(proportions)
                for i, (col, value) in enumerate(zip(next_columns, row)):
                    if isinstance(value, float):
                        value = round(value, 6)
                    if i == 1:
                        value = f"{value}</p>"
                    col.markdown(value, unsafe_allow_html=True)
except Exception:
    st.session_state.logger.exception("Something went wrong in Widget")
    st.error("Something went wrong. Please, reload page and try again")
