import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
from data_handler import parse_uploaded_file, load_internal_datasets, build_inventory_summary
from prompt_engine import SYSTEM_PROMPT, build_user_prompt
from glm_client import get_strategy

app = Flask(__name__)
app.secret_key = "resa-strategist-secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DATASETS_FOLDER = os.path.join(BASE_DIR, "datasets")
ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATASETS_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[-1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyse", methods=["POST"])
def analyse():
    business_name = request.form.get("business_name", "").strip()
    business_type = request.form.get("business_type", "").strip()
    business_context = request.form.get("business_context", "").strip()

    item_names = request.form.getlist("item_name[]")
    cost_prices = request.form.getlist("cost_price[]")
    sell_prices = request.form.getlist("sell_price[]")
    stock_qtys = request.form.getlist("stock_qty[]")
    units_solds = request.form.getlist("units_sold[]")

    inventory_items = []
    for name, cp, sp, sq, us in zip(item_names, cost_prices, sell_prices, stock_qtys, units_solds):
        if name.strip():
            inventory_items.append({
                "name": name.strip(),
                "cost_price": float(cp) if cp else 0,
                "sell_price": float(sp) if sp else 0,
                "stock_qty": int(sq) if sq else 0,
                "units_sold": int(us) if us else 0,
            })

    inventory_summary = build_inventory_summary(inventory_items)
    internal_market_context = load_internal_datasets()

    uploaded_data_summary = None
    if "file" in request.files:
        file = request.files["file"]
        if file and file.filename and file.filename.strip() != "":
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                try:
                    parsed = parse_uploaded_file(filepath)
                    uploaded_data_summary = (
                        f"File: {filename}\n{parsed['summary']}\nSample:\n{parsed['sample']}"
                    )
                finally:
                    if os.path.exists(filepath):
                        os.remove(filepath)

    user_prompt = build_user_prompt(
        business_name,
        business_type,
        business_context,
        inventory_summary,
        uploaded_data_summary,
        internal_market_context,
    )

    strategy = get_strategy(SYSTEM_PROMPT, user_prompt)

    return render_template(
        "result.html",
        strategy=strategy,
        business_name=business_name,
        business_type=business_type,
        inventory_items=inventory_items,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
