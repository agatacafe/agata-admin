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
    st.header("Guía de marca")
    st.write("Logo, colores y etiqueta de producto de Ágata café.")
    st.download_button("Descargar kit de marca", brand_kit(), file_name="Agata-cafe-kit-de-marca.zip",
                       mime="application/zip")

    st.subheader("Logo")
    st.write(guide["logo"]["description"])
    for column, filename, background, label in zip(st.columns(3),
            ("agata-bean.svg", "agata-bean-olive.svg", "agata-bean-cream.svg"), ("#7A7F5E", "#FBF7EE", "#7A7F5E"),
            ("Grano de ágata · a color", "Una tinta · oliva", "Una tinta · crema")):
        with column:
            svg = (BRAND / filename).read_text(encoding="utf-8")
            encoded = base64.b64encode(svg.encode()).decode()
            st.html(_swatch(background, f'<img src="data:image/svg+xml;base64,{encoded}" height="110" alt="{label}">'))
            st.caption(label)
            st.download_button("Descargar " + filename, svg, file_name=filename, mime="image/svg+xml")
    for rule in guide["logo"]["rules"]:
        st.write("• " + rule)

    st.subheader("Arte de empaque")
    for column, filename, caption in zip(st.columns(2), ("wordmark.png", "product-label.png"),
                                         ("Logotipo manuscrito con el grano de ágata ilustrado", "Etiqueta de producto")):
        with column:
            st.image(str(BRAND / "reference" / filename), caption=caption, width="stretch")

    st.subheader("Colores")
    for start in range(0, len(guide["colors"]), 3):
        for column, color in zip(st.columns(3), guide["colors"][start:start + 3]):
            with column:
                hex_value = color["hex"]
                st.html(f'<div style="height:64px;background:{hex_value};border:1px solid #7A7F5E;'
                        f'border-radius:8px" aria-label="Muestra de color {color["name"]}"></div>')
                st.write("**" + color["name"] + "**")
                st.code(hex_value, language=None)
                st.caption("RGB " + ", ".join(str(int(hex_value[i:i + 2], 16)) for i in (1, 3, 5)))
                st.write(color["use"])

    st.subheader("Campos de la etiqueta")
    st.table({"Campo": [f for f, _ in guide["label_fields"]],
              "Contenido": [c for _, c in guide["label_fields"]]})
    st.caption("Contacto en el empaque: " + " · ".join(guide["contact"]))
    st.caption("Referencia actualizada: " + guide["version"])
