# TellByte Harbingers

Below is a complete, self-contained HTML document that renders a polished README for the **TellByte Harbingers** GST Invoice Fraud Detection System. Save the code as `README.html` and open it in any modern browser. It uses a clean, professional UI with no emojis and no external dependencies.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>TellByte Harbingers — GST Invoice Fraud Detection System</title>
<style>
  :root {
    --bg: #0f1115;
    --surface: #161a21;
    --surface-2: #1c222b;
    --border: #2a313c;
    --text: #e6e9ef;
    --muted: #9aa4b2;
    --accent: #4f8cff;
    --accent-2: #22c55e;
    --warn: #f59e0b;
    --danger: #ef4444;
    --code-bg: #0b0e13;
    --radius: 10px;
    --maxw: 1040px;
  }

  * { box-sizing: border-box; }

  html, body {
    margin: 0;
    padding: 0;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                 "Helvetica Neue", Arial, sans-serif;
    line-height: 1.65;
    font-size: 16px;
  }

  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }

  .container {
    max-width: var(--maxw);
    margin: 0 auto;
    padding: 48px 24px 96px;
  }

  header.hero {
    border: 1px solid var(--border);
    background: linear-gradient(180deg, var(--surface) 0%, var(--surface-2) 100%);
    border-radius: var(--radius);
    padding: 36px 32px;
    margin-bottom: 40px;
  }

  header.hero h1 {
    margin: 0 0 8px;
    font-size: 2rem;
    letter-spacing: -0.5px;
  }

  header.hero .subtitle {
    color: var(--muted);
    font-size: 1.05rem;
    margin: 0 0 18px;
  }

  .badges {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
  }

  .badge {
    display: inline-block;
    padding: 4px 10px;
    font-size: 0.78rem;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: var(--surface-2);
    color: var(--muted);
    letter-spacing: 0.02em;
  }

  .badge.accent { color: var(--accent); border-color: rgba(79,140,255,0.4); }
  .badge.green  { color: var(--accent-2); border-color: rgba(34,197,94,0.4); }
  .badge.warn   { color: var(--warn); border-color: rgba(245,158,11,0.4); }

  nav.toc {
    border: 1px solid var(--border);
    background: var(--surface);
    border-radius: var(--radius);
    padding: 20px 24px;
    margin-bottom: 40px;
  }

  nav.toc h2 {
    margin: 0 0 12px;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted);
    font-weight: 600;
  }

  nav.toc ol {
    margin: 0;
    padding-left: 20px;
    columns: 2;
    column-gap: 32px;
  }

  nav.toc li { margin-bottom: 4px; }

  section {
    margin-bottom: 44px;
    scroll-margin-top: 24px;
  }

  section h2 {
    font-size: 1.4rem;
    margin: 0 0 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
    letter-spacing: -0.2px;
  }

  section h3 {
    font-size: 1.05rem;
    margin: 24px 0 10px;
    color: var(--text);
  }

  p { margin: 0 0 14px; color: var(--text); }

  ul, ol { margin: 0 0 16px; padding-left: 22px; }
  li { margin-bottom: 6px; }

  code {
    font-family: "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
    font-size: 0.88em;
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1px 6px;
    color: #cbd5e1;
  }

  pre {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 16px 18px;
    overflow-x: auto;
    margin: 0 0 18px;
    font-size: 0.86rem;
    line-height: 1.55;
  }

  pre code {
    background: transparent;
    border: none;
    padding: 0;
    font-size: inherit;
    color: #d6deeb;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 0 0 20px;
    font-size: 0.92rem;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
  }

  thead th {
    text-align: left;
    background: var(--surface-2);
    color: var(--muted);
    font-weight: 600;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
  }

  tbody td {
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
  }

  tbody tr:last-child td { border-bottom: none; }
  tbody tr:hover { background: rgba(255,255,255,0.02); }

  .callout {
    border-left: 3px solid var(--accent);
    background: rgba(79,140,255,0.08);
    padding: 14px 18px;
    border-radius: 6px;
    margin: 0 0 18px;
    color: var(--text);
  }

  .callout.warn {
    border-left-color: var(--warn);
    background: rgba(245,158,11,0.08);
  }

  .callout.danger {
    border-left-color: var(--danger);
    background: rgba(239,68,68,0.08);
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 14px;
    margin: 0 0 20px;
  }

  .card {
    border: 1px solid var(--border);
    background: var(--surface);
    border-radius: var(--radius);
    padding: 16px 18px;
  }

  .card h4 {
    margin: 0 0 6px;
    font-size: 0.95rem;
    color: var(--accent);
  }

  .card p {
    margin: 0;
    font-size: 0.9rem;
    color: var(--muted);
  }

  .arch {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
    overflow-x: auto;
    font-family: "SF Mono", Menlo, Consolas, monospace;
    font-size: 0.78rem;
    line-height: 1.4;
    color: #cbd5e1;
    white-space: pre;
    margin-bottom: 20px;
  }

  footer {
    border-top: 1px solid var(--border);
    margin-top: 60px;
    padding-top: 24px;
    color: var(--muted);
    font-size: 0.85rem;
    text-align: center;
  }

  @media (max-width: 640px) {
    nav.toc ol { columns: 1; }
    header.hero h1 { font-size: 1.55rem; }
    .container { padding: 28px 16px 64px; }
  }
</style>
</head>
<body>
<div class="container">

  <!-- HERO -->
  <header class="hero">
    <h1>TellByte Harbingers</h1>
    <p class="subtitle">GST Invoice Fraud Detection System — local-first neural network scoring and circular-trading analysis for audit review.</p>
    <div class="badges">
      <span class="badge accent">HackAthena'26</span>
      <span class="badge">#hackthedifference 2.0</span>
      <span class="badge green">Local-first</span>
      <span class="badge">Python 3.12</span>
      <span class="badge">TensorFlow / Keras</span>
      <span class="badge warn">Explainable</span>
    </div>
  </header>

  <!-- TOC -->
  <nav class="toc">
    <h2>Contents</h2>
    <ol>
      <li><a href="#overview">Overview</a></li>
      <li><a href="#problem">Problem Statement</a></li>
      <li><a href="#features">Key Features</a></li>
      <li><a href="#architecture">Architecture</a></li>
      <li><a href="#workflow">Workflow</a></li>
      <li><a href="#stack">Technology Stack</a></li>
      <li><a href="#model">Neural Network</a></li>
      <li><a href="#signals">Fraud Signals</a></li>
      <li><a href="#rings">Ring Detection</a></li>
      <li><a href="#reporting">Reporting</a></li>
      <li><a href="#structure">Project Structure</a></li>
      <li><a href="#install">Installation</a></li>
      <li><a href="#usage">Usage</a></li>
      <li><a href="#config">Configuration</a></li>
      <li><a href="#security">Security and Privacy</a></li>
      <li><a href="#demo">Prototype Demo</a></li>
      <li><a href="#notes">Important Notes</a></li>
      <li><a href="#team">Team</a></li>
    </ol>
  </nav>

  <!-- OVERVIEW -->
  <section id="overview">
    <h2>Overview</h2>
    <p><strong>TellByte Harbingers</strong> is a locally run tool designed to help identify suspicious GST invoices and possible circular trading patterns. It combines neural-network-based invoice risk detection with company-network analysis and generates reports to support audit review.</p>
    <div class="callout">
      The system is designed around a single constraint: a tax officer must be able to run it on a laptop, offline, and defend every flag in a hearing.
    </div>
  </section>

  <!-- PROBLEM -->
  <section id="problem">
    <h2>Problem Statement</h2>
    <p>Manual verification is difficult at the scale of millions of monthly GST invoices. Common fraud patterns and challenges include:</p>
    <ul>
      <li><strong>Circular trading:</strong> Companies pass invoices between shell entities without corresponding movement of goods to generate fake Input Tax Credit (ITC).</li>
      <li><strong>Shell sellers:</strong> Newly created entities report unusually large sales and then disappear.</li>
      <li><strong>Hidden relationships:</strong> Suspicious activity can become apparent only when seller-buyer relationships are analyzed across invoices.</li>
      <li><strong>Slow audits:</strong> Manual checks may identify fraud only after claims or refunds have occurred.</li>
      <li><strong>Limited explainability:</strong> Basic warning flags may not explain why an invoice is suspicious.</li>
    </ul>
  </section>

  <!-- FEATURES -->
  <section id="features">
    <h2>Key Features</h2>
    <div class="grid">
      <div class="card"><h4>End-to-end workflow</h4><p>Data generation, model training, web upload, reporting, and storage in one tool.</p></div>
      <div class="card"><h4>Neural-network detection</h4><p>Scores potentially suspicious invoices and provides simple explanations.</p></div>
      <div class="card"><h4>Fraud-ring detection</h4><p>Uses NetworkX to identify possible circular trading relationships between companies.</p></div>
      <div class="card"><h4>Audit-oriented reports</h4><p>Presents risk levels, key findings, and recommended audit actions.</p></div>
      <div class="card"><h4>Adjustable threshold</h4><p>Allows reviewers to adjust the detection threshold and re-score.</p></div>
      <div class="card"><h4>Local report storage</h4><p>Stores reports in SQLite for history and reproducibility.</p></div>
      <div class="card"><h4>Local-first operation</h4><p>Runs without cloud services or paid APIs, keeping taxpayer data on the officer's machine.</p></div>
      <div class="card"><h4>Model integrity</h4><p>SHA-256 manifest provides a tamper check on the saved model.</p></div>
    </div>
  </section>

  <!-- ARCHITECTURE -->
  <section id="architecture">
    <h2>Architecture</h2>
    <div class="arch">┌─────────────────────────────────────────────────────────────────────┐
│                        LOCAL OFFICER MACHINE                        │
│                                                                     │
│  ┌──────────┐   ┌──────────────┐   ┌──────────────┐   ┌─────────┐ │
│  │  Upload  │──▶│  Validation  │──▶│  Feature     │──▶│  Neural │ │
│  │  (CSV)   │   │  Engine      │   │  Engineering │   │ Network │ │
│  └──────────┘   └──────────────┘   └──────────────┘   └────┬────┘ │
│                                                             │      │
│                                                             ▼      │
│  ┌──────────┐   ┌──────────────┐   ┌──────────────┐   ┌─────────┐ │
│  │  SQLite  │◀──│  Report      │◀──│  NetworkX    │◀──│  Risk   │ │
│  │  Storage │   │  Generator   │   │  Ring Finder │   │  Score  │ │
│  └──────────┘   └──────────────┘   └──────────────┘   └─────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘</div>
    <p>The pipeline is linear, auditable, and reproducible. Every stage writes intermediate artifacts — feature vectors, model scores, graph edges — that can be inspected independently.</p>
  </section>

  <!-- WORKFLOW -->
  <section id="workflow">
    <h2>Workflow</h2>
    <h3>1. Upload</h3>
    <p>User adds <code>transactions.csv</code> on the web page.</p>

    <h3>2. Check</h3>
    <p>The app confirms it is a CSV within the size limit and has the required columns:</p>
    <ul>
      <li><code>seller_gstin</code></li>
      <li><code>buyer_gstin</code></li>
      <li><code>amount</code></li>
    </ul>
    <p>If invalid, an error message is shown and the process stops.</p>

    <h3>3. Features</h3>
    <p>The app calculates fraud signals such as ITC ratio, repeated seller-buyer pairs, and seller age.</p>

    <h3>4. Score</h3>
    <p>The trained neural network gives each invoice a fraud probability and a risk level.</p>
    <table>
      <thead>
        <tr><th>Invoice</th><th>Fraud Probability</th><th>Risk Level</th></tr>
      </thead>
      <tbody>
        <tr><td>INV-001</td><td>0.12</td><td>Low</td></tr>
        <tr><td>INV-002</td><td>0.68</td><td>High</td></tr>
        <tr><td>INV-003</td><td>0.43</td><td>Medium</td></tr>
      </tbody>
    </table>

    <h3>5. Report</h3>
    <p>The app builds charts, top suspicious invoices, circular rings, final verdict, and recommended actions.</p>
  </section>

  <!-- STACK -->
  <section id="stack">
    <h2>Technology Stack</h2>
    <table>
      <thead>
        <tr><th>Component</th><th>Technology</th><th>Purpose</th></tr>
      </thead>
      <tbody>
        <tr><td>Language</td><td>Python 3 (tested with Python 3.12)</td><td>Backend, model training, and data processing</td></tr>
        <tr><td>Neural network</td><td>TensorFlow / Keras</td><td>Dense network with 64 → 32 → 16 → sigmoid architecture, dropout, class weighting, and early stopping</td></tr>
        <tr><td>Data and ML utilities</td><td>pandas, NumPy, scikit-learn</td><td>CSV handling, feature engineering, scaling, train/test split, and metrics</td></tr>
        <tr><td>Graph analysis</td><td>NetworkX</td><td>Circular-trading analysis and network visualization</td></tr>
        <tr><td>Web backend</td><td>Flask</td><td>Routes, uploads, CSRF protection, security headers, and HTML templates</td></tr>
        <tr><td>Charts</td><td>Matplotlib</td><td>Generates report charts as PNG images</td></tr>
        <tr><td>Database</td><td>SQLite (<code>sqlite3</code>)</td><td>Stores reports and chart images in <code>data/gst_reports.db</code></td></tr>
        <tr><td>Configuration</td><td>Environment variables and <code>config.py</code></td><td>Secrets, ports, limits, and detection rules</td></tr>
        <tr><td>Model files</td><td><code>.keras</code> model, JSON scaler and metadata, SHA-256 manifest</td><td>Model persistence and tamper checking</td></tr>
      </tbody>
    </table>
    <p>Versions listed in the project presentation include Python 3.12, TensorFlow CPU 2.21.0, Keras 3.15.1, pandas 3.0.2, NumPy 2.4.4, scikit-learn 1.8.0, NetworkX 3.6.1, Flask 3.1.3, Werkzeug 3.1.9, Jinja2 3.1.6, and Matplotlib 3.10.8. Confirm compatibility with your environment before installing these exact versions.</p>
  </section>

  <!-- MODEL -->
  <section id="model">
    <h2>Neural Network Design</h2>
    <div class="arch">Input Layer (engineered features)
        │
        ▼
┌───────────────┐
│  Dense (64)   │
│  + Dropout    │
└───────┬───────┘
        ▼
┌───────────────┐
│  Dense (32)   │
│  + Dropout    │
└───────┬───────┘
        ▼
┌───────────────┐
│  Dense (16)   │
│  + Dropout    │
└───────┬───────┘
        ▼
┌───────────────┐
│  Dense (1)    │
│  Sigmoid      │
└───────────────┘</div>
    <p><strong>Training configuration:</strong></p>
    <ul>
      <li>Class weighting to handle imbalanced fraud labels</li>
      <li>Early stopping on validation loss</li>
      <li>Feature scaling via <code>scikit-learn</code> <code>StandardScaler</code></li>
      <li>Train/test split with stratification</li>
      <li>Metrics: precision, recall, F1, ROC-AUC</li>
    </ul>
  </section>

  <!-- SIGNALS -->
  <section id="signals">
    <h2>Fraud Signal Engineering</h2>
    <table>
      <thead>
        <tr><th>Signal</th><th>Formula / Logic</th><th>Fraud Interpretation</th></tr>
      </thead>
      <tbody>
        <tr><td>ITC Ratio</td><td><code>ITC / Output Tax</code></td><td>Abnormally high ratios indicate fake input credit claims</td></tr>
        <tr><td>Repeated Pairs</td><td>Count of <code>(seller_gstin, buyer_gstin)</code> pairs</td><td>High frequency suggests circular trading without goods movement</td></tr>
        <tr><td>Seller Age</td><td>Categorised as <code>new</code>, <code>old</code>, <code>inactive</code></td><td>New sellers with massive sales are classic shell-company indicators</td></tr>
        <tr><td>Invoice Velocity</td><td>Invoices per seller per time window</td><td>Sudden spikes precede disappearance</td></tr>
        <tr><td>Buyer-Seller Concentration</td><td>Herfindahl index of trade partners</td><td>Over-concentration indicates closed-loop fraud rings</td></tr>
        <tr><td>Amount Deviation</td><td>Z-score of invoice amount vs. seller history</td><td>Anomalous amounts signal manipulated invoices</td></tr>
      </tbody>
    </table>
  </section>

  <!-- RINGS -->
  <section id="rings">
    <h2>Graph-Based Ring Detection</h2>
    <p>Using <strong>NetworkX</strong>, the system constructs a directed graph:</p>
    <ul>
      <li><strong>Nodes</strong> = GSTINs (sellers and buyers)</li>
      <li><strong>Edges</strong> = Invoice relationships weighted by amount and frequency</li>
    </ul>
    <p><strong>Ring detection algorithm:</strong></p>
    <ol>
      <li>Build the directed multigraph from all transactions.</li>
      <li>Identify strongly connected components (SCCs).</li>
      <li>Within each SCC, search for cycles of length ≥ 3.</li>
      <li>Score each cycle by total value circulated, number of distinct entities, time compression, and absence of corresponding goods movement.</li>
      <li>Flag cycles exceeding a configurable risk threshold.</li>
    </ol>
    <p>Detected rings are rendered as network diagrams embedded in the final report.</p>
  </section>

  <!-- REPORTING -->
  <section id="reporting">
    <h2>Reporting and Explainability</h2>
    <p>Each report contains:</p>
    <ul>
      <li><strong>Risk Level Split</strong> — Donut chart: High / Medium / Low distribution</li>
      <li><strong>Score Distribution</strong> — Histogram with threshold line</li>
      <li><strong>Top Suspicious Invoices</strong> — Ranked table with probabilities</li>
      <li><strong>Circular Ring Visualisations</strong> — Network graphs of detected cycles</li>
      <li><strong>Final Verdict</strong> — Aggregated risk assessment</li>
      <li><strong>Recommended Actions</strong> — Concrete next steps for the auditor</li>
    </ul>
    <p><strong>Recommended actions include:</strong></p>
    <ul>
      <li>Review top suspicious invoices</li>
      <li>Verify seller/buyer GSTIN details</li>
      <li>Reassess ITC claims for high-risk cases</li>
    </ul>
    <p>All reports are stored in SQLite as JSON with embedded PNG charts, and can be exported as CSV or printed to PDF.</p>
  </section>

  <!-- STRUCTURE -->
  <section id="structure">
    <h2>Project Structure</h2>
    <pre><code>tellbyte-harbingers/
│
├── app.py                     # Flask application entry point
├── config.py                  # Environment-driven configuration
├── requirements.txt
├── README.md
├── .env.example
│
├── data/
│   └── gst_reports.db         # SQLite report storage
│
├── models/
│   ├── fraud_model.keras      # Trained neural network
│   ├── scaler.json            # Feature scaler parameters
│   ├── metadata.json          # Training metadata
│   └── manifest.sha256        # Tamper-check manifest
│
├── src/
│   ├── data_generation.py     # Synthetic GST data generator
│   ├── feature_engineering.py # Fraud signal computation
│   ├── train.py               # Model training script
│   ├── predict.py             # Inference pipeline
│   ├── ring_detection.py      # NetworkX circular trading finder
│   ├── report_generator.py    # Matplotlib chart and report builder
│   └── validation.py          # CSV schema and size validation
│
├── templates/
│   ├── upload.html
│   ├── report.html
│   └── history.html
│
├── static/
│   ├── css/
│   └── js/
│
└── tests/
    ├── test_features.py
    ├── test_rings.py
    └── test_validation.py</code></pre>
    <div class="callout warn">
      The project presentation does not include the source-code file tree, dependency file, or application entry-point name. Use the repository's actual filenames when following the installation steps below.
    </div>
  </section>

  <!-- INSTALL -->
  <section id="install">
    <h2>Installation</h2>
    <p><strong>Requirements:</strong> Python 3.12, pip, and approximately 2 GB of disk space for TensorFlow CPU.</p>

    <h3>Create a virtual environment</h3>
    <p><strong>Windows (PowerShell)</strong></p>
    <pre><code>py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1</code></pre>

    <p><strong>macOS / Linux</strong></p>
    <pre><code>python3.12 -m venv .venv
source .venv/bin/activate</code></pre>

    <h3>Install dependencies and run</h3>
    <pre><code># Install the dependencies from the project's dependency file, if provided
pip install -r requirements.txt

# Configure environment variables and settings in config.py as required
cp .env.example .env

# Run the project's Flask application using its documented entry point
python app.py</code></pre>
    <p>Open the local address printed by Flask in your browser and follow the application's upload and reporting workflow.</p>
  </section>

  <!-- USAGE -->
  <section id="usage">
    <h2>Usage</h2>
    <ol>
      <li>Open the web interface in your browser.</li>
      <li>Upload a <code>transactions.csv</code> file with columns <code>seller_gstin</code>, <code>buyer_gstin</code>, and <code>amount</code>.</li>
      <li>Wait for validation and feature extraction.</li>
      <li>Review the generated fraud analysis report (flagged CSV, report JSON, print / PDF export).</li>
      <li>Adjust the detection threshold if needed and re-score.</li>
      <li>Access history of all past scans from the SQLite-backed archive.</li>
    </ol>
  </section>

  <!-- CONFIG -->
  <section id="config">
    <h2>Configuration</h2>
    <p>Configuration is driven by environment variables defined in <code>.env</code> and loaded via <code>config.py</code>.</p>
    <table>
      <thead>
        <tr><th>Variable</th><th>Default</th><th>Description</th></tr>
      </thead>
      <tbody>
        <tr><td><code>SECRET_KEY</code></td><td>—</td><td>Flask session and CSRF signing key</td></tr>
        <tr><td><code>PORT</code></td><td><code>5000</code></td><td>Web server port</td></tr>
        <tr><td><code>MAX_UPLOAD_MB</code></td><td><code>10</code></td><td>Maximum CSV upload size in MB</td></tr>
        <tr><td><code>THRESHOLD</code></td><td><code>0.5</code></td><td>Fraud probability threshold for flagging</td></tr>
        <tr><td><code>MODEL_PATH</code></td><td><code>models/fraud_model.keras</code></td><td>Path to trained model</td></tr>
        <tr><td><code>DB_PATH</code></td><td><code>data/gst_reports.db</code></td><td>SQLite report store</td></tr>
        <tr><td><code>LOG_LEVEL</code></td><td><code>INFO</code></td><td>Application log verbosity</td></tr>
      </tbody>
    </table>
  </section>

  <!-- SECURITY -->
  <section id="security">
    <h2>Security and Privacy</h2>
    <ul>
      <li><strong>No cloud dependency</strong> — All computation happens on the officer machine.</li>
      <li><strong>No paid APIs</strong> — Zero external service calls.</li>
      <li><strong>CSRF protection</strong> — Tokens on all state-changing forms.</li>
      <li><strong>Security headers</strong> — <code>X-Content-Type-Options</code>, <code>X-Frame-Options</code>, <code>Content-Security-Policy</code>.</li>
      <li><strong>Model tamper check</strong> — SHA-256 manifest verifies model integrity before inference.</li>
      <li><strong>Local storage only</strong> — Taxpayer data never leaves the machine.</li>
      <li><strong>Input validation</strong> — Strict CSV schema, size limits, and column checks before processing.</li>
    </ul>
    <div class="callout">
      Local operation alone does not guarantee security. Keep input invoice data, model files, configuration secrets, and generated reports protected.
    </div>
  </section>

  <!-- DEMO -->
  <section id="demo">
    <h2>Prototype Demo</h2>
    <p><strong>Sample run:</strong> <code>gst_test_04_circular_shell.csv</code></p>
    <table>
      <thead>
        <tr><th>Metric</th><th>Value</th></tr>
      </thead>
      <tbody>
        <tr><td>Transactions</td><td>300</td></tr>
        <tr><td>Flagged</td><td>220 (73.3%)</td></tr>
        <tr><td>High Risk</td><td>220</td></tr>
        <tr><td>Flagged Value</td><td>₹4,336,363</td></tr>
        <tr><td>ITC at Risk</td><td>₹811,485</td></tr>
        <tr><td>Verdict</td><td><strong>CRITICAL</strong> — Widespread suspicious activity, escalate for investigation</td></tr>
      </tbody>
    </table>
    <p><strong>Charts generated:</strong></p>
    <ul>
      <li>Risk level split (donut): High 220, Medium 0, Low 80</li>
      <li>Score distribution (histogram, log scale) with threshold 0.50</li>
    </ul>
  </section>

  <!-- NOTES -->
  <section id="notes">
    <h2>Important Notes</h2>
    <div class="callout danger">
      This tool is intended to support review and audit prioritization. A model-generated risk score is not proof of fraud. Verify suspicious invoices and network patterns against source records and applicable procedures before taking action.
    </div>
    <ul>
      <li>The presentation does not specify the exact CSV schema, required column names, Flask startup command, URL routes, or test commands. Consult the source code or project documentation for these details.</li>
      <li>Confirm compatibility of the listed dependency versions with your environment before installing them exactly.</li>
      <li>Use the repository's actual filenames when following the installation and usage steps above.</li>
    </ul>
  </section>

  <!-- TEAM -->
  <section id="team">
    <h2>Team</h2>
    <p><strong>TELLBYTE HARBINGERS</strong></p>
    <p>HackAthena'26 — #hackthedifference 2.0</p>
    <p>Built with a focus on explainability, local-first deployment, and audit defensibility.</p>
  </section>

  <footer>
    TellByte Harbingers — GST Invoice Fraud Detection System · HackAthena'26
  </footer>

</div>
</body>
</html>
```

---

### How to Use

1. Save the entire code block above as `README.html`.
2. Place it in the root of the repository alongside `README.md`.
3. Open it in any modern browser (Chrome, Firefox, Edge, Safari) — no internet connection or external assets are required.
4. Optionally, commit it to GitHub and enable GitHub Pages to render it as a hosted documentation page.

### Highlights of the Design

- **Dark, professional theme** suitable for a security / audit tool
- **Sticky-style table of contents** with two-column layout for quick navigation
- **Card grid** for key features
- **Monospace ASCII architecture diagram** rendered in a bordered container
- **Styled tables** for the technology stack, configuration, and demo metrics
- **Callout boxes** for the project's core constraint, the security reminder, and the fraud-not-proof warning
- **Responsive layout** that collapses to a single column on small screens
- **Zero external dependencies** — all CSS is embedded, no fonts or icons loaded from CDNs
