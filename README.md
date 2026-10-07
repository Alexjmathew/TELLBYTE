# TELLBYTE HARBINGERS

## GST Invoice Fraud Detection System

TELLBYTE HARBINGERS is a locally run tool designed to help identify suspicious GST invoices and possible circular trading patterns. It combines neural-network-based invoice risk detection with company-network analysis and generates reports to support audit review.

## Problem Statement

Manual verification is difficult at the scale of millions of monthly GST invoices. Common fraud patterns and challenges include:

- **Circular trading:** Companies pass invoices between shell entities without corresponding movement of goods to generate fake Input Tax Credit (ITC).
- **Shell sellers:** Newly created entities report unusually large sales and then disappear.
- **Hidden relationships:** Suspicious activity can become apparent only when seller-buyer relationships are analyzed across invoices.
- **Slow audits:** Manual checks may identify fraud only after claims or refunds have occurred.
- **Limited explainability:** Basic warning flags may not explain why an invoice is suspicious.

## Key Features

- **End-to-end workflow:** Supports data generation, model training, web upload, reporting, and storage in one tool.
- **Neural-network detection:** Scores potentially suspicious invoices and provides simple explanations.
- **Fraud-ring detection:** Uses NetworkX to identify possible circular trading relationships between companies.
- **Audit-oriented reports:** Presents risk levels, key findings, and recommended audit actions.
- **Adjustable threshold:** Allows reviewers to adjust the detection threshold.
- **Local report storage:** Stores reports in SQLite.
- **Local-first operation:** Designed to run without cloud services or paid APIs, keeping taxpayer data on the officer's machine.

## Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Language | Python 3 (tested with Python 3.12) | Backend, model training, and data processing |
| Neural network | TensorFlow / Keras | Dense network with 64 → 32 → 16 → sigmoid architecture, dropout, class weighting, and early stopping |
| Data and ML utilities | pandas, NumPy, scikit-learn | CSV handling, feature engineering, scaling, train/test split, and metrics |
| Graph analysis | NetworkX | Circular-trading analysis and network visualization |
| Web backend | Flask | Routes, uploads, CSRF protection, security headers, and HTML templates |
| Charts | Matplotlib | Generates report charts as PNG images |
| Database | SQLite (`sqlite3`) | Stores reports and chart images in `data/gst_reports.db` |
| Configuration | Environment variables and `config.py` | Secrets, ports, limits, and detection rules |
| Model files | `.keras` model, JSON scaler and metadata, SHA-256 manifest | Model persistence and tamper checking |

Versions listed in the project presentation include Python 3.12, TensorFlow CPU 2.21.0, Keras 3.15.1, pandas 3.0.2, NumPy 2.4.4, scikit-learn 1.8.0, NetworkX 3.6.1, Flask 3.1.3, Werkzeug 3.1.9, Jinja2 3.1.6, and Matplotlib 3.10.8. Confirm compatibility with your environment before installing these exact versions.

## Workflow

The project presentation describes an end-to-end pipeline covering data generation, model training, web upload, reporting, and storage. Exact commands and route names depend on the implementation in the repository.

## Getting Started

The project presentation does not include the source-code file tree, dependency file, or application entry-point name. Use the repository's actual filenames when following these steps.

1. Install Python 3.12 or another version supported by the project.
2. Create and activate a virtual environment.
3. Install the dependencies from the project's dependency file, if one is provided.
4. Configure the environment variables and settings in `config.py` as required by the implementation.
5. Run the project's Flask application using its documented entry point.
6. Open the local address printed by Flask in your browser and follow the application's upload and reporting workflow.

### Create a virtual environment

**Windows (PowerShell)**

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

## Data, Reports, and Model Integrity

- Report storage is described as `data/gst_reports.db`.
- The model is saved as a `.keras` file alongside a JSON scaler and metadata.
- A SHA-256 manifest is used for a model tamper check.
- Keep input invoice data, model files, configuration secrets, and generated reports protected. The application is designed for local use, but local operation alone does not guarantee security.

## Important Notes

- This tool is intended to support review and audit prioritization; a model-generated risk score is not proof of fraud.
- Verify suspicious invoices and network patterns against source records and applicable procedures before taking action.
- The presentation does not specify the exact CSV schema, required column names, Flask startup command, URL routes, or test commands. Consult the source code or project documentation for these details.

## Project Name

**TELLBYTE HARBINGERS** — GST invoice risk detection and circular-trading analysis.
