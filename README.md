# GST Fraud Detection - Neural Network + Flask + SQLite

    pip install -r requirements.txt        # exact tested versions: requirements-lock.txt
    python generate_dataset.py     # 1. creates data/train_dataset.csv and data/transactions.csv
    python train_model.py          # 2. trains the neural network -> model/
    python app.py                  # 3. open http://127.0.0.1:5000 and upload data/transactions.csv

Pages
- /          upload a CSV, choose the flag threshold
- /report/<id>      report with 10 matplotlib charts and a final verdict
- /history          all saved reports (open, download JSON, delete)
- /api/report/<id>  the stored report as JSON

Database: data/gst_reports.db (SQLite). Table `reports` stores each report as a JSON document
(report_json) and its chart images (charts_json). Query it with any SQLite tool.

Your CSV needs: seller_gstin, buyer_gstin, amount.
Optional: invoice_id, invoice_date, tax_rate, itc_amount, seller_age_days.
data/transactions_with_answers.csv is the same test file WITH labels, for checking accuracy.

Security and settings
- All settings are environment variables, see `config.py` and `.env.example` (login, port, limits, retention).
- `python test_security.py` runs the automated security checks.
- Read `CHECKLIST.md` (hardcoding, security, licences, third-party) and `THIRD_PARTY_LICENSES.md`.
- Replace the placeholder name in `LICENSE` before sharing.
