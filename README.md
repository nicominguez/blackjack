# Blackjack simulator

## How to run

### Frontend layout

- Streamlit frontend files are in `/frontend`.
- `streamlit_app.py` at the repository root is kept as a launcher entrypoint.
- A static `frontend/index.html` is included for GitHub Pages hosting.

Update models

```bash
python3 -m tools.ml_trainer
```

Run Streamlit app

```bash
streamlit run streamlit_app.py
```

Run Simulation

```bash
python3 -m test.main
```
