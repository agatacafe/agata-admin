# Ágata café: administration

A public Streamlit landing page that links to Ágata café's separate applications,
with a Brand guide tab. It follows the same pattern as Elaenia Technologies'
administration portal: it reads public URL settings and local brand assets only,
and needs no credentials, database or business records.

Deployed at https://agatacafe-admi.streamlit.app/ from `agatacafe/agata-admin`,
branch `main`, entry point `app.py`. Use this URL for "Back to administration"
links in Ágata café's other apps.

## Applications

| Card | Setting |
| --- | --- |
| Sales | `SALES_APP_URL` |
| Inventory | `INVENTORY_APP_URL` |
| Reconciliation | `RECONCILIATION_APP_URL` |
| Equity and contributions | `EQUITY_APP_URL` |

None of these apps is deployed yet, so every card starts disabled with
"App link will be available after deployment." Set a URL in
`.streamlit/secrets.toml` (copy `secrets.example.toml`) or as an environment
variable to enable a card. Environment values take precedence. Invalid,
credential-bearing or non-HTTP(S) URLs keep only that card disabled. Once a URL
is confirmed, it can also be added to `DEFAULT_URLS` in `app.py`.

## Logo

`assets/brand/agata-bean.svg` is a flat vector version of the illustrated
packaging bean: an S-shaped crease, rippled agate layers that follow each half,
thin cream veins and a glossy highlight, in roast, amber, honey, sand and cream.
It carries its own colours, so the header shows it unchanged in light and dark
themes (80 px on desktop, 60 px on phones). `agata-bean-olive.svg` and
`agata-bean-cream.svg` are one-colour versions for single-ink uses.

The SVGs are generated; change `scripts/make_logo.py` and run
`python scripts/make_logo.py assets/brand` rather than editing them by hand.
The painted bean and the script wordmark stay as packaging artwork in
`assets/brand/reference/`.

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Tests

```powershell
python -m unittest discover -s tests -v
```

Tests use invented URLs and make no network calls.
