"""Public entry point for Ágata café applications."""

import streamlit as st

from scripts.brand import brand_guide
from scripts.portal_config import Service, read_setting, valid_app_url
from scripts.ui import LOGO, app_header, service_card, styles


SERVICES = (
    Service("sales", "Sales",
            "Record coffee orders, customers and payments.",
            "SALES_APP_URL"),
    Service("inventory", "Inventory",
            "Track green and roasted coffee, roasts, packaging and stock movements.",
            "INVENTORY_APP_URL"),
    Service("reconciliation", "Reconciliation",
            "Review bank transactions and prepare monthly account reconciliations.",
            "RECONCILIATION_APP_URL"),
    Service("equity", "Equity and contributions",
            "Record partner contributions and keep the cap table up to date.",
            "EQUITY_APP_URL"),
)

# User-confirmed deployments; the matching setting overrides each one. Never guess URLs.
DEFAULT_URLS: dict[str, str] = {
    "SALES_APP_URL": "https://agatacafe-sales.streamlit.app/",
    "INVENTORY_APP_URL": "https://agatacafe-inventory.streamlit.app/",
    "RECONCILIATION_APP_URL": "https://agatacafe-reconciliation.streamlit.app/",
    "EQUITY_APP_URL": "https://agatacafe-equity.streamlit.app/",
}


def main():
    st.set_page_config(page_title="Ágata café: administration", page_icon=str(LOGO), layout="wide")
    styles()
    app_header()
    applications, brand = st.tabs(["Applications", "Brand guide"])
    with applications:
        st.header("Applications")
        for start in range(0, len(SERVICES), 2):
            with st.container(key=f"service_row_{start}"):
                columns = st.columns(2, gap="large")
                for column, service in zip(columns, SERVICES[start:start + 2]):
                    with column:
                        value = read_setting(service.setting).strip() or DEFAULT_URLS.get(service.setting, "")
                        url = valid_app_url(value)
                        service_card(service, url, invalid=bool(value) and url is None)
        st.caption("Each application manages its own access and records.")
    with brand:
        brand_guide()


if __name__ == "__main__":
    main()
