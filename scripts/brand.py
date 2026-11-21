"""Public Ágata café brand reference and downloadable assets."""

import base64
import io
import json
from zipfile import ZipFile, ZIP_DEFLATED

import streamlit as st

from scripts.ui import BRAND


def brand_kit():
    output = io.BytesIO()
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for path in sorted(BRAND.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(BRAND).as_posix())
    return output.getvalue()


def _swatch(background, inner):
    return (f'<div style="background:{background};border:1px solid #CDD3AC;border-radius:8px;'
            f'padding:24px;text-align:center">{inner}</div>')


def brand_guide():
    guide = json.loads((BRAND / "guide.json").read_text(encoding="utf-8"))
    st.header("Brand guide")
    st.write("Logo, colors and product label reference for Ágata café.")
    st.download_button("Download brand kit", brand_kit(), file_name="Agata-cafe-brand-kit.zip",
                       mime="application/zip")

    st.subheader("Logo")
    st.write(guide["logo"]["description"])
    for column, filename, background, label in zip(st.columns(2),
            ("agata-bean.svg", "agata-bean-cream.svg"), ("#FBF7EE", "#7A7F5E"),
            ("Olive bean · light background", "Cream bean · olive background")):
        with column:
            svg = (BRAND / filename).read_text(encoding="utf-8")
            encoded = base64.b64encode(svg.encode()).decode()
            st.html(_swatch(background, f'<img src="data:image/svg+xml;base64,{encoded}" height="110" alt="{label}">'))
            st.caption(label)
            st.download_button("Download " + filename, svg, file_name=filename, mime="image/svg+xml")
    for rule in guide["logo"]["rules"]:
        st.write("• " + rule)

    st.subheader("Packaging artwork")
    for column, filename, caption in zip(st.columns(2), ("wordmark.png", "product-label.png"),
                                         ("Script wordmark with the illustrated agate bean", "Product label")):
        with column:
            st.image(str(BRAND / "reference" / filename), caption=caption, width="stretch")

    st.subheader("Colors")
    for start in range(0, len(guide["colors"]), 3):
        for column, color in zip(st.columns(3), guide["colors"][start:start + 3]):
            with column:
                hex_value = color["hex"]
                st.html(f'<div style="height:64px;background:{hex_value};border:1px solid #7A7F5E;'
                        f'border-radius:8px" aria-label="{color["name"]} color swatch"></div>')
                st.write("**" + color["name"] + "**")
                st.code(hex_value, language=None)
                st.caption("RGB " + ", ".join(str(int(hex_value[i:i + 2], 16)) for i in (1, 3, 5)))
                st.write(color["use"])

    st.subheader("Product label fields")
    st.table({"Field": [f for f, _ in guide["label_fields"]],
              "Content": [c for _, c in guide["label_fields"]]})
    st.caption("Contact on packaging: " + " · ".join(guide["contact"]))
    st.caption("Reference updated: " + guide["version"])
