"""Matplotlib charts -> base64 PNG strings (embedded straight into the HTML report)."""
import base64, io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    import networkx as nx
except Exception:
    nx = None

RED, AMB, GRN, BLU, GRY = "#d93a3a", "#e59a17", "#1f9d63", "#2557d6", "#9aa5b8"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titleweight": "bold", "axes.titlesize": 11, "figure.dpi": 110})


def _b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


def _empty(title, msg="Nothing to show"):
    fig, ax = plt.subplots(figsize=(5, 3.2))
    ax.axis("off"); ax.set_title(title); ax.text(.5, .5, msg, ha="center", color=GRY)
    return _b64(fig)


def risk_donut(s):
    vals = [s["high"], s["medium"], s["low"]]
    fig, ax = plt.subplots(figsize=(4.6, 3.6))
    if sum(vals) == 0:
        return _empty("Risk levels")
    ax.pie(vals, colors=[RED, AMB, GRN], startangle=90, wedgeprops=dict(width=.42, edgecolor="white"))
    ax.legend([f"{n}: {v:,}" for n, v in zip(["High", "Medium", "Low"], vals)], loc="center left",
              bbox_to_anchor=(1, .5), frameon=False)
    ax.text(0, 0, f"{s['flag_rate']}%\nflagged", ha="center", va="center", fontweight="bold")
    ax.set_title("Risk level split")
    return _b64(fig)


def prob_hist(res, thr):
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    ax.hist(res["fraud_probability"], bins=30, color=BLU, alpha=.85)
    ax.axvline(thr, color=RED, ls="--", lw=1.5, label=f"threshold {thr:.2f}")
    ax.set_yscale("log"); ax.set_xlabel("Fraud probability"); ax.set_ylabel("Transactions (log)")
    ax.set_title("Score distribution"); ax.legend(frameon=False)
    return _b64(fig)


def amount_scatter(res):
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    d = res.sample(min(len(res), 4000), random_state=1)
    col = np.where(d["risk_level"] == "High", RED, np.where(d["risk_level"] == "Medium", AMB, GRY))
    ax.scatter(d["amount"].clip(lower=1), d["fraud_probability"], c=col, s=9, alpha=.6, linewidths=0)
    ax.set_xscale("log"); ax.set_xlabel("Invoice amount (Rs, log)"); ax.set_ylabel("Fraud probability")
    ax.set_title("Amount vs risk")
    return _b64(fig)


def type_bar(types):
    if not types:
        return _empty("Suspicious patterns", "No patterns among flagged invoices")
    names = list(types.keys())[::-1]; vals = [types[n] for n in names]
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    bars = ax.barh(names, vals, color=[RED, AMB, BLU, "#7a52c7", GRN][:len(names)][::-1] or BLU)
    ax.bar_label(bars, padding=3); ax.set_xlabel("Flagged invoices")
    ax.set_title("Suspicious patterns found")
    return _b64(fig)


def seller_bar(sellers):
    if not sellers:
        return _empty("Top flagged sellers")
    d = sellers[:8][::-1]
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    bars = ax.barh([x["gstin"] for x in d], [x["flagged"] for x in d], color=RED)
    ax.bar_label(bars, padding=3); ax.set_xlabel("Flagged invoices")
    ax.set_title("Top flagged sellers")
    return _b64(fig)


def monthly_trend(res):
    if "invoice_date" not in res.columns:
        return _empty("Monthly trend", "No invoice_date column")
    d = pd.to_datetime(res["invoice_date"], errors="coerce")
    if d.notna().sum() == 0:
        return _empty("Monthly trend", "Dates could not be read")
    m = pd.DataFrame({"m": d.dt.to_period("M").astype(str), "f": res["flagged"]}).dropna()
    g = m.groupby("m")["f"].agg(["sum", "count"])
    fig, ax = plt.subplots(figsize=(5.2, 3.4)); ax2 = ax.twinx()
    ax.bar(g.index, g["count"], color="#dbe3f5", label="All")
    ax.bar(g.index, g["sum"], color=RED, label="Flagged")
    ax2.plot(g.index, 100 * g["sum"] / g["count"], color=AMB, marker="o", lw=1.6)
    ax2.set_ylabel("Flag rate %"); ax2.spines["right"].set_visible(True)
    ax.set_ylabel("Invoices"); ax.set_title("Monthly volume and flag rate")
    ax.tick_params(axis="x", rotation=60); ax.legend(frameon=False, loc="upper left")
    return _b64(fig)


def network_graph(res, rings=None):
    if nx is None:
        return _empty("Suspicious network", "networkx not installed")
    f = res[res["flagged"] == 1]
    if f.empty:
        return _empty("Suspicious network", "No flagged invoices")
    e = f.groupby(["seller_gstin", "buyer_gstin"]).agg(n=("amount", "size")).reset_index()
    ring_edges, ring_nodes = set(), set()
    for g in (rings or [])[:6]:
        ents = g["entities"]
        for i in range(len(ents)):
            ring_edges.add((ents[i], ents[(i + 1) % len(ents)]))
        ring_nodes.update(ents)
    keep = e[e.apply(lambda r: (r.seller_gstin, r.buyer_gstin) in ring_edges, axis=1)]
    rest = e[~e.index.isin(keep.index)].sort_values("n", ascending=False).head(max(0, 30 - len(keep)))
    e = pd.concat([keep, rest])
    G = nx.DiGraph()
    for r in e.itertuples():
        G.add_edge(r.seller_gstin, r.buyer_gstin, n=int(r.n))
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    pos = nx.spring_layout(G, seed=5, k=1.1, iterations=150)
    other = [(u, v) for u, v in G.edges if (u, v) not in ring_edges]
    nx.draw_networkx_edges(G, pos, edgelist=other, width=.7, alpha=.35, edge_color=GRY, arrowsize=7, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=[x for x in G.edges if x in ring_edges], width=2, alpha=.9,
                           edge_color=RED, arrowsize=12, ax=ax, connectionstyle="arc3,rad=0.12")
    nodes_r = [n for n in G if n in ring_nodes]; nodes_o = [n for n in G if n not in ring_nodes]
    nx.draw_networkx_nodes(G, pos, nodelist=nodes_o, node_size=40, node_color=GRY, ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=nodes_r, node_size=130, node_color=RED, ax=ax)
    nx.draw_networkx_labels(G, pos, labels={n: n[-7:] for n in nodes_r}, font_size=6.5, ax=ax)
    ax.axis("off")
    ax.set_title("Flagged trading network (red = circular trading rings)" if nodes_r else "Flagged trading network")
    return _b64(fig)


def confusion(meta):
    c = meta["confusion"]
    m = np.array([[c["tn"], c["fp"]], [c["fn"], c["tp"]]])
    fig, ax = plt.subplots(figsize=(3.9, 3.4))
    share = m / m.sum(axis=1, keepdims=True)
    ax.imshow(share, cmap="Blues", vmin=0, vmax=1)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{m[i, j]:,}", ha="center", va="center",
                    color="white" if share[i, j] > .5 else "black", fontweight="bold")
    ax.set_xticks([0, 1], ["Normal", "Fraud"]); ax.set_yticks([0, 1], ["Normal", "Fraud"])
    ax.set_xlabel("Predicted"); ax.set_ylabel("Actual"); ax.set_title("Confusion matrix (test)")
    for s in ax.spines.values(): s.set_visible(False)
    return _b64(fig)


def roc_and_loss(meta):
    fig, (a, b) = plt.subplots(1, 2, figsize=(8.4, 3.3))
    a.plot(meta["roc"]["fpr"], meta["roc"]["tpr"], color=BLU, lw=2)
    a.plot([0, 1], [0, 1], ls="--", color=GRY)
    a.set_xlabel("False positive rate"); a.set_ylabel("True positive rate")
    a.set_title(f"ROC curve (AUC {meta['roc_auc']})")
    b.plot(meta["history"]["loss"], label="train", color=BLU)
    b.plot(meta["history"]["val_loss"], label="validation", color=RED)
    b.set_xlabel("Epoch"); b.set_ylabel("Loss"); b.set_title("Training curve"); b.legend(frameon=False)
    return _b64(fig)


def importance(meta):
    d = meta["feature_importance"][:8][::-1]
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    ax.barh([x["feature"] for x in d], [x["auc_drop"] for x in d], color=BLU)
    ax.set_xlabel("Drop in AUC when shuffled"); ax.set_title("What the network relies on")
    return _b64(fig)


def make_all(res, report, meta, thr):
    return {
        "risk_donut": risk_donut(report["summary"]),
        "prob_hist": prob_hist(res, thr),
        "amount_scatter": amount_scatter(res),
        "type_bar": type_bar(report["fraud_types"]),
        "seller_bar": seller_bar(report["sellers"]),
        "monthly": monthly_trend(res),
        "network": network_graph(res, report["rings"]),
        "confusion": confusion(meta),
        "roc_loss": roc_and_loss(meta),
        "importance": importance(meta),
    }
