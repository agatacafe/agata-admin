"""Ágata café header, styles and native Streamlit service cards."""

import base64
from pathlib import Path

import streamlit as st

BRAND = Path(__file__).resolve().parents[1] / "assets" / "brand"
LOGO = BRAND / "agata-bean.svg"


def styles():
    st.html("""<style>
    [data-testid="stMainBlockContainer"] {max-width:1440px;padding-top:3rem;padding-bottom:3rem;}
    h1 {font-size:clamp(1.9rem,3.2vw,2.75rem);line-height:1.3;letter-spacing:-.01em;padding-top:.25em;overflow:visible;}
    .st-key-agata_header {
        margin-bottom:1.25rem;padding-bottom:1.25rem;border-bottom:1px solid rgba(122,127,94,.35);
    }
    .st-key-agata_header .agata-logo {
        margin-left:auto;width:96px;aspect-ratio:325/409;background:currentColor;
        mask:var(--agata-logo) center/contain no-repeat;
        -webkit-mask:var(--agata-logo) center/contain no-repeat;
    }
    [class*="st-key-service_"]:not([class*="st-key-service_row_"]) {
        border-top:3px solid #7A7F5E;background:rgba(122,127,94,.07);
        border-radius:.65rem;justify-content:space-between;
    }
    [data-testid="stLinkButton"] a {border-color:#7A7F5E;}
    @media(max-width:640px) {
        [data-testid="stMainBlockContainer"] {padding-top:1.5rem;padding-bottom:2rem;}
        .st-key-agata_header [data-testid="stHorizontalBlock"],
        [class*="st-key-service_row_"] [data-testid="stHorizontalBlock"] {flex-direction:column;}
        .st-key-agata_header [data-testid="stColumn"],
        [class*="st-key-service_row_"] [data-testid="stColumn"] {width:100%;flex:0 0 auto;min-width:0;}
        .st-key-agata_header .agata-logo {width:80px;margin-left:0;}
    }
    </style>""")


def app_header():
    # The bean's alpha shape is used as a mask so it follows the native text color:
    # olive on the light theme, cream on the dark theme.
    encoded = base64.b64encode(LOGO.read_bytes()).decode("ascii")
    with st.container(key="agata_header"):
        text, mark = st.columns([4, 1], vertical_alignment="center")
        with text:
            st.title("Ágata café: administration")
            st.write("Choose an application to manage Ágata café. Carrizal, Costa Rica.")
        with mark:
            st.html('<div class="agata-logo" role="img" aria-label="Ágata café bean" '
                    'style="--agata-logo:url(data:image/svg+xml;base64,' + encoded + ')"></div>')


def service_card(service, url, *, invalid=False):
    with st.container(border=True, height=250, key=f"service_{service.slug}"):
        with st.container():
            st.subheader(service.title)
            st.write(service.description)
        with st.container():
            if url:
                st.link_button(f"Open {service.title}", url, width="stretch")
            else:
                st.button(f"Open {service.title}", disabled=True, width="stretch", key=service.slug,
                          help="The configured app link is invalid. Contact the administrator." if invalid else None)
                st.caption("App link will be available after deployment.")
