# TellByte Harbingers

**GST Invoice Fraud Detection System** — a local-first neural network tool for scoring suspicious GST invoices and detecting circular-trading patterns, built to support audit review.

![HackAthena'26](https://img.shields.io/badge/HackAthena'26-%23hackthedifference%202.0-blue)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Keras-orange)
![Local-first](https://img.shields.io/badge/Local--first-offline-green)

## Table of Contents

1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Key Features](#key-features)
4. [Architecture](#architecture)
5. [Workflow](#workflow)
6. [Technology Stack](#technology-stack)
7. [Neural Network Design](#neural-network-design)
8. [Fraud Signals](#fraud-signals)
9. [Circular Trading (Ring) Detection](#circular-trading-ring-detection)
10. [Reporting](#reporting)
11. [Installation](#installation)
12. [Usage](#usage)
13. [Configuration](#configuration)
14. [Security and Privacy](#security-and-privacy)
15. [Prototype Demo](#prototype-demo)
16. [Important Notes](#important-notes)
17. [Team](#team)

## Overview

TellByte Harbingers is a locally run tool that helps identify suspicious GST invoices and possible circular trading patterns. It combines neural-network-based invoice risk scoring with company-network analysis, and generates reports to support audit review.

> The system is designed around one constraint: a tax officer should be able to run it on a laptop, offline, and be able to explain every flag.

## Problem Statement

Manual verification is difficult at the scale of millions of monthly GST invoices. Common fraud patterns and challenges include:

- **Circular trading:** Companies pass invoices between shell entities without corresponding movement of goods, to generate fake Input Tax Credit (ITC).
- **Shell sellers:** Newly created entities report unusually large sales and then disappear.
- **Hidden relationships:** Suspicious activity may only become apparent when seller-buyer relationships are analyzed across invoices.
- **Slow audits:** Manual checks may identify fraud only after claims or refunds have occurred.
- **Limited explainability:** Basic warning flags often do not explain why an invoice is suspicious.

## Key Features

| Feature | Description |
|---|---|
| End-to-end workflow | Data generation, model training, web upload, reporting, and storage in one tool |
| Neural-network detection | Scores potentially suspicious invoices and provides simple explanations |
| Fraud-ring detection | Uses NetworkX to identify possible circular trading between companies |
| Audit-oriented reports | Presents risk levels, key findings, and recommended audit actions |
| Adjustable threshold | Reviewers can change the detection threshold and re-score |
| Local report storage | Reports are stored in SQLite for history and reproducibility |
| Local-first operation | No cloud services or paid APIs; taxpayer data stays on the officer's machine |
| Model integrity | A SHA-256 manifest provides a tamper check on the saved model |

## Architecture

```text
Upload (CSV) -> Validation -> Feature Engineering -> Neural Network -> Risk Score
                                                                          |
SQLite Storage <- Report Generator <- NetworkX Ring Detection <-----------+
```

Every stage runs locally on the officer's machine.

## Workflow

1. **Upload:** The user adds `transactions.csv` on the web page.
2. **Check:** The app confirms the file is a CSV within the size limit and has the required columns: `seller_gstin`, `buyer_gstin`, `amount`. If invalid, an error message is shown and processing stops.
3. **Features:** The app calculates fraud signals such as ITC ratio, repeated seller-buyer pairs, and seller age.
4. **Score:** The trained neural network assigns each invoice a fraud probability and a risk level.
5. **Report:** The app builds charts, top suspicious invoices, circular rings, a final verdict, and recommended actions.

Example scoring output:

| Invoice | Fraud Probability | Risk Level |
|---|---|---|
| INV-001 | 0.12 | Low |
| INV-002 | 0.68 | High |
| INV-003 | 0.43 | Medium |

## Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Language | Python 3 (tested with 3.12) | Backend, model training, data processing |
| Neural network | TensorFlow / Keras | Dense network (64 → 32 → 16 → sigmoid) with dropout, class weighting, early stopping |
| Data and ML utilities | pandas, NumPy, scikit-learn | CSV handling, feature engineering, scaling, train/test split, metrics |
| Graph analysis | NetworkX | Circular-trading analysis and network visualization |
| Web backend | Flask | Routes, uploads, CSRF protection, security headers, HTML templates |
| Charts | Matplotlib | Report charts as PNG images |
| Database | SQLite (`sqlite3`) | Stores reports and chart images in `data/gst_reports.db` |
| Configuration | Environment variables and `config.py` | Secrets, ports, limits, detection rules |
| Model files | `.keras` model, JSON scaler and metadata, SHA-256 manifest | Model persistence and tamper checking |

Versions used in the project presentation: Python 3.12, TensorFlow CPU 2.21.0, Keras 3.15.1, pandas 3.0.2, NumPy 2.4.4, scikit-learn 1.8.0, NetworkX 3.6.1, Flask 3.1.3, Werkzeug 3.1.9, Jinja2 3.1.6, Matplotlib 3.10.8. Confirm compatibility with your environment before installing these exact versions.

## Neural Network Design

```text
Input (engineered features)
  -> Dense(64) + Dropout
  -> Dense(32) + Dropout
  -> Dense(16) + Dropout
  -> Dense(1, sigmoid)  -> fraud probability
```

Training configuration:

- Class weighting to handle imbalanced fraud labels
- Early stopping
- Feature scaling (scaler parameters saved as JSON)
- Train/test split
- Evaluation metrics: precision, recall, F1, ROC-AUC

## Fraud Signals

| Signal | Logic | Fraud interpretation |
|---|---|---|
| ITC ratio | ITC relative to output tax | Abnormally high ratios may indicate fake input credit claims |
| Repeated pairs | Count of repeated `(seller_gstin, buyer_gstin)` pairs | High frequency may suggest circular trading without goods movement |
| Seller age | Age category of the seller | New sellers with very large sales are a common shell-company indicator |

## Circular Trading (Ring) Detection

Using NetworkX, the system builds a directed graph where:

- **Nodes** are GSTINs (sellers and buyers)
- **Edges** are invoice relationships between them

Cycles in this graph represent possible circular trading. Detected rings are shown as network diagrams in the final report.

## Reporting

Each report includes:

- **Risk level split:** donut chart of High / Medium / Low invoices
- **Score distribution:** histogram with the threshold line
- **Top suspicious invoices:** ranked by fraud probability
- **Circular ring visualizations:** network graphs of detected cycles
- **Final verdict:** aggregated risk assessment
- **Recommended actions:** review top suspicious invoices, verify seller/buyer GSTIN details, and reassess ITC claims for high-risk cases

Reports are stored in SQLite, and can be exported as a flagged CSV, report JSON, or printed to PDF.

## Installation

**Requirements:** Python 3.12, pip, and enough disk space for TensorFlow (CPU).

Create a virtual environment.

Windows (PowerShell):

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install dependencies and run:

```bash
pip install -r requirements.txt
python app.py
```

Open the local address printed by Flask in your browser.

> **TODO:** Confirm that `requirements.txt` and `app.py` match the actual filenames in this repository, and add the `.env` setup step if one is required.

## Usage

1. Open the web interface in your browser.
2. Upload a `transactions.csv` file with the columns `seller_gstin`, `buyer_gstin`, and `amount`.
3. Wait for validation and feature extraction.
4. Review the generated fraud analysis report (flagged CSV, report JSON, print / PDF export).
5. Adjust the detection threshold if needed and re-score.
6. Open the history of past scans from the SQLite-backed archive.

## Configuration

Settings live in `config.py` and can be overridden with environment variables. Typical settings include the secret key, server port, maximum upload size, detection threshold (default `0.5`), model path, and database path (`data/gst_reports.db`).

> **TODO:** Replace this paragraph with a table of the exact variable names and defaults from `config.py`.

## Security and Privacy

- **No cloud dependency:** all computation happens on the officer's machine.
- **No paid APIs:** no external service calls.
- **CSRF protection** on the web forms.
- **Security headers** set by the Flask app.
- **Model tamper check:** a SHA-256 manifest verifies the saved model.
- **Local storage only:** taxpayer data stays on the machine.
- **Input validation:** CSV type, size, and required columns are checked before processing.

Local operation alone does not guarantee security. Keep input invoice data, model files, configuration secrets, and generated reports protected.

## Prototype Demo

Sample run: `gst_test_04_circular_shell.csv`

| Metric | Value |
|---|---|
| Transactions | 300 |
| Flagged | 220 (73.3%) |
| High risk | 220 |
| Flagged value | ₹4,336,363 |
| ITC at risk | ₹811,485 |
| Verdict | **CRITICAL** — widespread suspicious activity, escalate for investigation |

Charts generated:

- Risk level split (donut): High 220, Medium 0, Low 80
- Score distribution (histogram, log scale) with threshold 0.50

## Important Notes

> This tool supports review and audit prioritization. A model-generated risk score is not proof of fraud. Verify suspicious invoices and network patterns against source records and applicable procedures before taking action.

- Confirm dependency-version compatibility with your environment before installing exact versions.
- Use the repository's actual filenames when following the installation and usage steps.

## Team

**TELLBYTE HARBINGERS** — HackAthena'26, #hackthedifference 2.0

Built with a focus on explainability, local-first deployment, and audit defensibility.
