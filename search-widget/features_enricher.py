import re
from typing import Any, Callable, List, Tuple, Dict
import streamlit as st
from upgini import FeaturesEnricher, SearchKey
from upgini.metadata import RuntimeParameters
from upgini.http import SearchProgress
from upgini.errors import ValidationError
import pandas as pd
from pandas.api.types import is_float_dtype
import textwrap


field_column_header = "Feature"
shap_column_header = "SHAP value"
included_in_data_listings_header = "Included in data sources"
data_listings_header = "Data source"
all_fields_shap_header = "All features SHAP"
relevant_features_header = "Relevant features"
price_header = "Price"
action_header = "Action"


def run_search(
    df: pd.DataFrame,
    target_column: str,
    search_keys: Dict[str, SearchKey],
    generate_features: List[str],
    progress_callback: Callable[[SearchProgress], Any],
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    runtime_parameters = RuntimeParameters(
        properties={"downsampling_limit": 40_000}
    )
    enricher = FeaturesEnricher(
        search_keys=search_keys,
        generate_features=generate_features,
        api_key=st.secrets["UPGINI_API_KEY"],
        runtime_parameters=runtime_parameters,
        detect_missing_search_keys=False,
        raise_validation_error=True,
    )
    st.session_state.enricher = enricher
    try:
        enricher.fit(
            df.drop(columns=target_column),
            df[target_column],
            calculate_metrics=False,
            progress_callback=progress_callback,
        )
    except ValidationError as e:
        if (
            e.args[0] == "y is a constant. Relevant feature search requires a non-constant y"
            or e.args[0] == "y contains only one distinct value"
        ):
            raise ValidationError("Target label is a constant. Relevant feature search requires a non-constant target")
        if e.args[0] == "y contains only NaN or incorrect values.":
            raise ValidationError("Target label contains only NaN or incorrect values")
        if e.args[0] == "X size should be at least 100 rows after validation":
            raise ValidationError("Labeled dataset size with unique IPv4 must be not less than 1000 rows")
        if e.args[0] == "There is empty train dataset after removing data before '2000-01-01'":
            raise ValidationError("There is empty labeled dataset after removing data before '2000-01-01'")
        if e.args[0] == "Too big size of dataframe X for processing. Please reduce number of rows or columns":
            raise ValidationError(
                "Too big size of labeled dataset for processing. Please reduce number of rows or columns"
            )
        else:
            raise e
    return enricher


def fetch_results(enricher: FeaturesEnricher) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    fi = enricher.get_features_info()

    relevant_fields = fi.rename(
        columns={"Source": included_in_data_listings_header, "Feature name": field_column_header}
    )
    relevant_fields = relevant_fields.query("Provider != ''")
    relevant_fields = relevant_fields.drop(columns=["Coverage %", "Feature type"])

    raw_relevant_fields = relevant_fields.copy()

    def remove_anchor(s):
        return re.sub(r"<a[^>]+>([\w\s]+)<\/a>", r"\1", s)

    def get_original_name(s):
        s = re.sub(r"<a.+>f_(.+)_\w+<\/a>", r"\1", s)
        return re.sub(r"f_(.+)_\w+", r"\1", s)

    features_df = enricher._search_task.get_all_initial_raw_features(
        "download_sample_features_from_widget", metrics_calculation=True
    )

    def add_hint(feature):
        sample = []
        for c in features_df.columns:
            if c in feature:
                column: pd.Series = features_df[c]
                sample = column.dropna().sample(n=10, random_state=42)
                if is_float_dtype(sample):
                    sample = sample.round(4)
                sample = sample.astype(str).values
        sample_markup = "</br>".join(sample)
        match_with_link = re.match("(<a.+>)f_(.+)_\\w+(<\\/a>)", feature)
        match_without_link = re.match("f_(.+)_\\w+", feature)
        length_limit = 34
        if match_with_link is not None:
            f = match_with_link.group(2)
            if len(f) > length_limit:
                f = "</br>".join(textwrap.wrap(f, length_limit))
            renamed_feature = f"{match_with_link.group(1)}{f}{match_with_link.group(3)}"
        elif match_without_link is not None:
            renamed_feature = match_without_link.group(1)
            if len(renamed_feature) > length_limit:
                renamed_feature = "</br>".join(textwrap.wrap(renamed_feature, length_limit))
        else:
            renamed_feature = feature
            if len(renamed_feature) > length_limit:
                renamed_feature = "</br>".join(textwrap.wrap(renamed_feature, length_limit))

        return f"<div class='tooltip'>{renamed_feature}<span class='tooltiptext'>{sample_markup}</span></div>"

    relevant_fields[field_column_header] = relevant_fields[field_column_header].apply(add_hint)
    summary = (
        raw_relevant_fields[raw_relevant_fields["Provider"] != "Upgini"]
        .drop(columns="Provider")
        .groupby(by=included_in_data_listings_header)
        .agg(
            shap=pd.NamedAgg(column=shap_column_header, aggfunc="sum"),
            count=pd.NamedAgg(column=shap_column_header, aggfunc="count"),
        )
        .sort_values(by="shap", ascending=False)
        .reset_index()
        .rename(
            columns={
                included_in_data_listings_header: data_listings_header,
                "shap": all_fields_shap_header,
                "count": relevant_features_header,
            }
        )
    )
    relevant_fields = relevant_fields.drop(columns="Provider")

    summary[action_header] = "Request a quote"

    def price_by_listing(listing):
        if "IP Address Data for Mobile Carrier Detection" in listing:
            return "Trial 30 days, $80/month"
        elif "Privacy detection database" in listing:
            return "$1000/one-off"
        elif "IP Geolocation Data" in listing:
            return "No Trial, $800/month"
        else:
            return "By request"

    summary[price_header] = summary[data_listings_header].apply(price_by_listing)
    summary[relevant_features_header] = summary[relevant_features_header].astype(int)
    summary = summary.rename(columns={shap_column_header: all_fields_shap_header})
    summary = summary[
        [data_listings_header, all_fields_shap_header, relevant_features_header, price_header, action_header]
    ]

    relevant_fields = relevant_fields[[field_column_header, shap_column_header, included_in_data_listings_header]]

    # Using for email
    raw_relevant_fields = raw_relevant_fields.drop(columns="Provider")
    raw_relevant_fields[included_in_data_listings_header] = raw_relevant_fields[included_in_data_listings_header].apply(
        remove_anchor
    )
    raw_relevant_fields[field_column_header] = raw_relevant_fields[field_column_header].apply(get_original_name)

    return relevant_fields, summary, raw_relevant_fields
