import logging
from typing import Optional
from streamlit_modal import Modal
import streamlit as st
import pandas as pd

from email_utils import is_email, is_email_domain_free, is_email_domain_in_blocklist, send_email


def show_email_modal(open_modal: bool, raw_relevant_fields: pd.DataFrame):
    modal = Modal("Request", key="email_modal")

    if open_modal:
        modal.open()

    if modal.is_open():

        def is_invalid_full_name() -> Optional[str]:
            full_name_: Optional[str] = st.session_state.get("email_full_name")
            logging.info(f"Full name: `{full_name_}`")
            if "email_full_name" in st.session_state and full_name_ is not None and len(full_name_.strip()) == 0:
                return "required"

        def is_invalid_email() -> Optional[str]:
            company_email_: Optional[str] = st.session_state.get("email_company_email")
            logging.info(f"Company email: `{company_email_}`")
            if "email_company_email" not in st.session_state or company_email_ is None:
                return None
            if len(company_email_.strip()) == 0:
                return "required"
            if not is_email(company_email_):
                return "invalid"
            if is_email_domain_in_blocklist(company_email_):
                return "email domain is in blocklist"
            if is_email_domain_free(company_email_):
                return "email has free domain"

        def is_invalid_message() -> Optional[str]:
            email_message_: Optional[str] = st.session_state.get("email_message")
            logging.info(f"Message: `{email_message_}`")
            if "email_message" in st.session_state and email_message_ is not None and len(email_message_.strip()) == 0:
                return "required"

        def email_callback():
            full_name_: Optional[str] = st.session_state.get("email_full_name")
            company_email_: Optional[str] = st.session_state.get("email_company_email")
            email_message_: Optional[str] = st.session_state.get("email_message")

            is_sent = False
            try:
                is_sent = send_email(
                    full_name_,
                    company_email_,
                    email_message_,
                    raw_relevant_fields,
                )
            except Exception:
                logging.exception("Failed to send email")
            if is_sent:
                st.info("Request sent, thank you")
                modal.close(rerun=False)
            else:
                st.warning("Send failed, please try again")

        with modal.container():
            full_name_invalid_message = is_invalid_full_name()
            full_name_label = (
                "Full name*" if full_name_invalid_message is None else f"Full name* :red[({full_name_invalid_message})]"
            )
            full_name_value = st.session_state.get("email_full_name") or ""
            st.text_input(label=full_name_label, value=full_name_value, key="email_full_name")

            company_email_invalid_message = is_invalid_email()
            company_email_label = (
                "Company email*"
                if company_email_invalid_message is None
                else f"Company email* :red[({company_email_invalid_message})]"
            )
            company_email_value = st.session_state.get("email_company_email") or ""
            st.text_input(label=company_email_label, value=company_email_value, key="email_company_email")

            message_invalid_message = is_invalid_message()
            message_label = (
                "Message*" if message_invalid_message is None else f"Message* :red[({message_invalid_message})]"
            )
            message_value = st.session_state.get("email_message") or ""
            st.text_area(label=message_label, value=message_value, key="email_message")
            disabled_submit = (
                is_invalid_full_name() is not None or is_invalid_email() is not None or is_invalid_message() is not None
            )
            st.button(
                label="Request quote",
                on_click=email_callback,
                type="primary",
                disabled=disabled_submit,
            )
