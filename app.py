"""Portal público de las aplicaciones de Ágata café."""

import streamlit as st

from scripts.brand import brand_guide
from scripts.portal_config import Service, read_setting, valid_app_url
from scripts.ui import LOGO, app_header, service_card, styles


SERVICES = (
    Service("sales", "Ventas",
            "Registre pedidos de café, clientes y pagos.",
            "SALES_APP_URL"),
    Service("inventory", "Inventario",
            "Controle el café verde y tostado, los tuestes, el empaque y los movimientos de inventario.",
            "INVENTORY_APP_URL"),
    Service("reconciliation", "Conciliación",
            "Revise las transacciones bancarias y prepare las conciliaciones mensuales.",
            "RECONCILIATION_APP_URL"),
    Service("equity", "Capital y aportes",
            "Registre los aportes de los socios y mantenga al día la tabla de capitalización.",
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
    st.set_page_config(page_title="Ágata café: administración", page_icon=str(LOGO), layout="wide")
    styles()
    app_header()
    applications, brand = st.tabs(["Aplicaciones", "Guía de marca"])
    with applications:
        st.header("Aplicaciones")
        for start in range(0, len(SERVICES), 2):
            with st.container(key=f"service_row_{start}"):
                columns = st.columns(2, gap="large")
                for column, service in zip(columns, SERVICES[start:start + 2]):
                    with column:
                        value = read_setting(service.setting).strip() or DEFAULT_URLS.get(service.setting, "")
                        url = valid_app_url(value)
                        service_card(service, url, invalid=bool(value) and url is None)
        st.caption("Cada aplicación maneja su propio acceso y sus registros.")
    with brand:
        brand_guide()


if __name__ == "__main__":
    main()
