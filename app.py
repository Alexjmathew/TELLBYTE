"""Flask app: upload transactions.csv -> neural network scores it -> HTML report with charts.
Every report is saved as JSON in SQLite (data/gst_reports.db)."""
import hashlib, hmac, itertools, json, os, re, secrets, uuid
from datetime import datetime
import numpy as np
import pandas as pd
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
from tensorflow import keras
from flask import (Flask, render_template, request, send_file, redirect, session,
                   url_for, flash, abort, jsonify, Response)
from werkzeug.utils import secure_filename
import config, db, charts
from features import build_features, FEATURE_NAMES

try:
    import networkx as nx
except Exception:
    nx = None

app = Flask(__name__)
app.secret_key = config.SECRET_KEY or secrets.token_hex(32)
app.config["MAX_CONTENT_LENGTH"] = config.MAX_UPLOAD_MB * 1024 * 1024
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")
UPLOAD_DIR = config.UPLOAD_DIR
os.makedirs(UPLOAD_DIR, exist_ok=True)
db.init_db()
RID_RE = re.compile(r"^[0-9a-f]{12}$")


def _purge():
    if config.RETENTION_DAYS > 0:
        for rid in db.purge_older_than(config.RETENTION_DAYS):
            for suffix in (".csv", "_flagged.csv"):
                try:
                    os.remove(os.path.join(UPLOAD_DIR, rid + suffix))
                except OSError:
                    pass


_purge()


def _load_model():
    """Load the NN only if the files match the hashes written at training time (tamper check).
    The scaler is plain JSON - no pickle, so loading it cannot run code."""
    for p in (config.MODEL_FILE, config.SCALER_FILE, config.META_FILE, config.MANIFEST_FILE):
        if not os.path.exists(p):
            raise SystemExit("Model not found. Run:  python generate_dataset.py  then  python train_model.py")
    manifest = json.load(open(config.MANIFEST_FILE))
    for path, want in manifest.items():
        got = hashlib.sha256(open(path, "rb").read()).hexdigest()
        if not hmac.compare_digest(got, want):
            raise SystemExit(f"Integrity check FAILED for {path}. Retrain with: python train_model.py")
    model = keras.models.load_model(config.MODEL_FILE, safe_mode=True)
    sc = json.load(open(config.SCALER_FILE))
    return model, np.array(sc["center"]), np.array(sc["scale"]), json.load(open(config.META_FILE))


MODEL, SC_CENTER, SC_SCALE, META = _load_model()


def scale(X):
    return (np.asarray(X, dtype=float) - SC_CENTER) / np.where(SC_SCALE == 0, 1, SC_SCALE)


# ---------------------------------------------------------------- security
@app.before_request
def guard():
    # optional login (set APP_USER and APP_PASSWORD)
    if config.APP_USER and config.APP_PASSWORD:
        a = request.authorization
        ok = (a and hmac.compare_digest(a.username or "", config.APP_USER)
              and hmac.compare_digest(a.password or "", config.APP_PASSWORD))
        if not ok:
            return Response("Login required", 401, {"WWW-Authenticate": 'Basic realm="GST Fraud"'})
    # CSRF: every state-changing request must carry the session token
    if request.method == "POST":
        tok = session.get("csrf")
        if not tok or not hmac.compare_digest(tok, request.form.get("csrf", "")):
            abort(400, "Invalid or missing CSRF token")


@app.after_request
def headers(resp):
    resp.headers["Content-Security-Policy"] = ("default-src 'self'; img-src 'self' data:; style-src 'self'; "
                                               "script-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'none'")
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "no-referrer"
    resp.headers["Cache-Control"] = "no-store"
    return resp


@app.context_processor
def inject_csrf():
    if "csrf" not in session:
        session["csrf"] = secrets.token_hex(16)
    return {"csrf_token": session["csrf"]}


def csv_safe(df):
    """Neutralise spreadsheet formula injection (cells starting with = + - @) in exported CSVs."""
    out = df.copy()
    for col in out.select_dtypes(include="object").columns:
        out[col] = out[col].map(lambda v: "'" + v if isinstance(v, str) and v[:1] in ("=", "+", "-", "@", "\t", "\r") else v)
    return out


@app.errorhandler(413)
def too_large(_):
    flash(f"File too large (limit {config.MAX_UPLOAD_MB} MB).")
    return redirect(url_for("index"))


TYPE_ACTIONS = {
    "ITC inflation": "Reconcile claimed ITC against supplier returns (GSTR-2B) and hold refunds on mismatches.",
    "Threshold avoidance": "Review invoices sitting just under approval limits for splitting or under-reporting.",
    "Circular trading": "Trace the repeating seller-buyer links and check for real goods movement (e-way bills).",
    "New high-volume seller": "Run a physical/KYC verification of recently registered sellers with large volume.",
    "Concentrated buyers": "Check whether sellers with very few buyers are fronts for a single party.",
}


def indicator_list(r):
    """Return list of (type, plain-English text) for one row of the feature frame."""
    out = []
    if r.itc_ratio > config.ITC_RATIO_ALERT:
        out.append(("ITC inflation", f"ITC claimed is {r.itc_ratio:.1f}x the tax payable"))
    if r.near_threshold:
        out.append(("Threshold avoidance", "Amount just below an approval threshold"))
    if r.pair_txn_count >= config.REPEAT_PAIR_MIN:
        out.append(("Circular trading", f"Same seller-buyer pair trades repeatedly ({int(r.pair_txn_count)} invoices)"))
    if r.seller_age_days < config.NEW_SELLER_DAYS and r.log_seller_volume > np.log1p(config.NEW_SELLER_VOLUME):
        out.append(("New high-volume seller", f"Seller only {int(r.seller_age_days)} days old with high volume"))
    if r.seller_unique_buyers <= config.FEW_BUYERS_MAX and r.log_seller_volume > np.log1p(config.FEW_BUYERS_VOLUME):
        out.append(("Concentrated buyers", "Large volume sold to very few buyers"))
    return out


def level(p, thr):
    return "High" if p >= max(config.HIGH_RISK_PROB, thr) else "Medium" if p >= thr else "Low"


def score(df, thr):
    feats = build_features(df)
    probs = MODEL.predict(scale(feats[FEATURE_NAMES].values), verbose=0).ravel()
    res = df.copy()
    res["fraud_probability"] = probs.round(4)
    res["risk_level"] = [level(p, thr) for p in probs]
    res["flagged"] = (probs >= thr).astype(int)
    inds = [indicator_list(r) for r in feats.itertuples()]
    res["indicators"] = [" | ".join(t for _, t in i) or "Pattern flagged by neural network" for i in inds]
    res["pattern_types"] = [" | ".join(sorted({k for k, _ in i})) for i in inds]
    return res


def find_rings(res, limit=10):
    if nx is None:
        return []
    f = res[res.flagged == 1]
    if f.empty:
        return []
    e = f.groupby(["seller_gstin", "buyer_gstin"]).agg(n=("amount", "size"), v=("amount", "sum")).reset_index()
    G = nx.DiGraph()
    for r in e.itertuples():
        G.add_edge(r.seller_gstin, r.buyer_gstin, n=int(r.n), v=float(r.v))
    rings = []
    try:
        for cyc in itertools.islice(nx.simple_cycles(G, length_bound=config.MAX_RING_LENGTH), config.RING_SCAN_LIMIT):
            if len(cyc) < 2:
                continue
            legs = [(cyc[i], cyc[(i + 1) % len(cyc)]) for i in range(len(cyc))]
            rings.append({"entities": cyc, "length": len(cyc),
                          "volume": round(sum(G[a][b]["v"] for a, b in legs), 2),
                          "invoices": sum(G[a][b]["n"] for a, b in legs)})
    except Exception:
        return []
    rings.sort(key=lambda x: x["volume"], reverse=True)
    return rings[:limit]


def make_verdict(s, types, sellers, rings):
    rate = s["flag_rate"]
    rating = ("CRITICAL" if rate >= config.VERDICT_CRITICAL else "HIGH" if rate >= config.VERDICT_HIGH
              else "MODERATE" if rate >= config.VERDICT_MODERATE else "LOW")
    headline = {
        "CRITICAL": "Widespread suspicious activity - escalate for investigation.",
        "HIGH": "A significant share of invoices look suspicious - audit recommended.",
        "MODERATE": "Some invoices look suspicious - targeted review recommended.",
        "LOW": "Few or no suspicious invoices - routine monitoring is enough.",
    }[rating]
    findings = [f"{s['flagged']:,} of {s['total']:,} invoices ({rate}%) were flagged; {s['high']:,} are high risk."]
    if s["flagged"]:
        findings.append(f"Flagged invoices carry Rs {s['flagged_amount']:,.0f} of value and Rs {s['itc_at_risk']:,.0f} of ITC.")
    if types:
        t, n = next(iter(types.items()))
        findings.append(f"Most common pattern: {t} ({n:,} flagged invoices).")
    if rings:
        findings.append(f"{len(rings)} circular trading ring(s) found; the largest moves Rs {rings[0]['volume']:,.0f}.")
    if sellers:
        findings.append(f"Seller {sellers[0]['gstin']} has the most flagged invoices ({sellers[0]['flagged']}).")
    actions = [TYPE_ACTIONS[t] for t in types if t in TYPE_ACTIONS][:4]
    if rings:
        actions.append("Cross-check every entity in the listed rings for common owners, address or bank accounts.")
    if not actions:
        actions = ["No special action needed. Keep monitoring future filings."]
    return {"rating": rating, "headline": headline, "findings": findings, "actions": actions}


def build_report(res, filename, thr):
    amt = pd.to_numeric(res["amount"], errors="coerce").fillna(0)
    fl = res[res.flagged == 1]
    itc = float(pd.to_numeric(fl["itc_amount"], errors="coerce").fillna(0).sum()) if "itc_amount" in res.columns else 0.0
    n = len(res)
    s = {"total": n, "flagged": int(res.flagged.sum()), "flag_rate": round(100 * res.flagged.mean(), 1),
         "high": int((res.risk_level == "High").sum()), "medium": int((res.risk_level == "Medium").sum()),
         "low": int((res.risk_level == "Low").sum()),
         "flagged_amount": float(amt[res.flagged == 1].sum()), "total_amount": float(amt.sum()),
         "itc_at_risk": itc, "avg_flagged_prob": round(float(fl.fraud_probability.mean()) * 100, 1) if len(fl) else 0.0}

    counts = {}
    for v in fl["pattern_types"]:
        for t in filter(None, v.split(" | ")):
            counts[t] = counts.get(t, 0) + 1
    types = dict(sorted(counts.items(), key=lambda kv: kv[1], reverse=True))

    id_col = "invoice_id" if "invoice_id" in res.columns else None
    top = []
    for i, r in res.sort_values("fraud_probability", ascending=False).head(25).iterrows():
        top.append({"id": str(r[id_col]) if id_col else f"row {i}", "seller": r["seller_gstin"], "buyer": r["buyer_gstin"],
                    "amount": float(r["amount"]), "pct": round(float(r["fraud_probability"]) * 100, 1),
                    "level": r["risk_level"], "indicators": r["indicators"].split(" | ")})

    sellers = []
    if len(fl):
        g = (fl.groupby("seller_gstin").agg(flagged=("flagged", "sum"), avg=("fraud_probability", "mean"), amount=("amount", "sum"))
               .sort_values(["flagged", "amount"], ascending=False).head(10).reset_index())
        tot = res.groupby("seller_gstin").size()
        sellers = [{"gstin": r.seller_gstin, "flagged": int(r.flagged), "total": int(tot[r.seller_gstin]),
                    "avg": round(float(r.avg) * 100, 1), "amount": float(r.amount)} for r in g.itertuples()]

    rings = find_rings(res)
    check = None
    for c in ("is_fraud_label", "is_fraud", "label"):
        if c in res.columns:
            y = pd.to_numeric(res[c], errors="coerce").fillna(0).astype(int)
            tp = int(((res.flagged == 1) & (y == 1)).sum()); fp = int(((res.flagged == 1) & (y == 0)).sum())
            fn = int(((res.flagged == 0) & (y == 1)).sum()); tn = int(((res.flagged == 0) & (y == 0)).sum())
            check = {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "acc": round(100 * (tp + tn) / n, 2),
                     "prec": round(100 * tp / max(tp + fp, 1), 1), "rec": round(100 * tp / max(tp + fn, 1), 1)}
            break

    return {"filename": filename, "scanned_at": datetime.now().isoformat(timespec="seconds"), "threshold": thr,
            "summary": s, "fraud_types": types, "top": top, "sellers": sellers, "rings": rings, "check": check,
            "model": {k: META[k] for k in ("architecture", "precision", "recall", "f1", "roc_auc", "pr_auc", "confusion")},
            "verdict": make_verdict(s, types, sellers, rings)}


@app.route("/")
def index():
    return render_template("index.html", meta=META, thr=config.DEFAULT_THRESHOLD)


@app.route("/sample")
def sample():
    return send_file(config.SAMPLE_CSV, as_attachment=True)


@app.route("/analyze", methods=["POST"])
def do_analyze():
    f = request.files.get("file")
    if not f or not f.filename.lower().endswith(".csv"):
        flash("Please choose a .csv file.")
        return redirect(url_for("index"))
    try:
        thr = min(max(float(request.form.get("threshold", config.DEFAULT_THRESHOLD)),
                      config.THRESHOLD_MIN), config.THRESHOLD_MAX)
    except ValueError:
        thr = config.DEFAULT_THRESHOLD
    fname = secure_filename(f.filename)[:80] or "upload.csv"
    try:
        df = pd.read_csv(f, nrows=config.MAX_ROWS + 1)
        if df.empty:
            raise ValueError("the file has no rows")
        if len(df) > config.MAX_ROWS:
            raise ValueError(f"too many rows (limit {config.MAX_ROWS:,})")
        res = score(df, thr)
        report = build_report(res, fname, thr)
        imgs = charts.make_all(res, report, META, thr)
    except Exception as e:
        flash("Could not process file: " + str(e)[:200])
        return redirect(url_for("index"))
    rid = uuid.uuid4().hex[:12]
    res.to_csv(os.path.join(UPLOAD_DIR, f"{rid}.csv"), index=False)
    db.save_report(rid, fname, report, imgs)
    return redirect(url_for("view_report", rid=rid))


@app.route("/report/<rid>")
def view_report(rid):
    r = db.get_report(rid) if RID_RE.match(rid) else None
    if not r:
        abort(404)
    return render_template("report.html", r=r["report"], c=r["charts"], rid=rid, meta=META)


@app.route("/api/report/<rid>")
def api_report(rid):
    r = db.get_report(rid) if RID_RE.match(rid) else None
    if not r:
        abort(404)
    resp = jsonify(r["report"])
    if request.args.get("download"):
        resp.headers["Content-Disposition"] = f"attachment; filename=report_{rid}.json"
    return resp


@app.route("/history")
def history():
    return render_template("history.html", rows=db.list_reports())


@app.route("/delete/<rid>", methods=["POST"])
def delete(rid):
    if RID_RE.match(rid):
        db.delete_report(rid)
        for p in (f"{rid}.csv", f"{rid}_flagged.csv"):
            try:
                os.remove(os.path.join(UPLOAD_DIR, p))
            except OSError:
                pass
    return redirect(url_for("history"))


@app.route("/download/<rid>")
def download(rid):
    p = os.path.join(UPLOAD_DIR, f"{rid}.csv")
    if not RID_RE.match(rid) or not os.path.exists(p):
        abort(404)
    df = pd.read_csv(p)
    out = os.path.join(UPLOAD_DIR, f"{rid}_flagged.csv")
    csv_safe(df[df.flagged == 1].sort_values("fraud_probability", ascending=False)).to_csv(out, index=False)
    return send_file(out, as_attachment=True, download_name="flagged_transactions.csv")


@app.template_filter("inr")
def inr(v):
    return "₹{:,.0f}".format(v)


@app.template_filter("nice_date")
def nice_date(v):
    try:
        return datetime.fromisoformat(v).strftime("%d %b %Y, %H:%M")
    except Exception:
        return v


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=False)
