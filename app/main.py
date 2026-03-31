from flask import Flask, jsonify, send_file, render_template
import pandas as pd
import os

app = Flask(__name__)

RESULTS = os.path.join(os.path.dirname(__file__), "..", "results")

mapped_df  = pd.read_csv(os.path.join(RESULTS, "mapped_snps.csv"))
top15_df   = pd.read_csv(os.path.join(RESULTS, "top15_SNPs.csv"))

DISPLAY_COLS = ["ID", "CHROM", "POS", "A1", "A2", "BETA", "SE", "PVAL", "GENE", "CONSEQUENCE", "BIOTYPE"]

def clean_df(df):
    df = df[DISPLAY_COLS].copy()
    df["PVAL"] = df["PVAL"].apply(lambda x: f"{x:.2e}")
    df["BETA"] = df["BETA"].round(4)
    df["SE"]   = df["SE"].round(4)
    df["POS"]  = df["POS"].apply(lambda x: f"{int(x):,}")
    return df.fillna("—")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/plots/<name>")
def plot(name):
    allowed = {
        "manhattan":      "manhattan_plot.png",
        "pathway_bubble": "pathway_bubble_plot.png",
        "pathway_bar":    "pathway_enrichment.png",
    }
    if name not in allowed:
        return jsonify({"error": "not found"}), 404
    return send_file(os.path.join(RESULTS, allowed[name]), mimetype="image/png")


@app.route("/api/snps/top15")
def top15_snps():
    return jsonify(clean_df(top15_df).to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True, port=5050)
