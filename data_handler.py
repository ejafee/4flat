import os
import pandas as pd


def parse_uploaded_file(filepath):
    ext = filepath.rsplit(".", 1)[-1].lower()

    if ext == "csv":
        df = pd.read_csv(filepath)
    elif ext in ("xlsx", "xls"):
        df = pd.read_excel(filepath, engine="openpyxl" if ext == "xlsx" else None)
    else:
        raise ValueError(f"Unsupported file type: .{ext}")

    df.columns = [col.strip().lower() for col in df.columns]
    df = df.dropna(how="all")

    return {
        "columns": df.columns.tolist(),
        "row_count": len(df),
        "sample": df.head(5).to_string(),
        "summary": f"{len(df)} rows, columns: {', '.join(df.columns.tolist())}",
    }


def load_internal_datasets():
    datasets_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "datasets"
    )

    if not os.path.isdir(datasets_dir):
        return "No internal datasets loaded."

    valid_ext = {"csv", "xlsx", "xls"}
    summaries = []

    for filename in sorted(os.listdir(datasets_dir)):
        ext = filename.rsplit(".", 1)[-1].lower()
        if ext not in valid_ext:
            continue

        filepath = os.path.join(datasets_dir, filename)
        try:
            if ext == "csv":
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath, engine="openpyxl" if ext == "xlsx" else None)

            df.columns = [col.strip().lower() for col in df.columns]
            df = df.dropna(how="all")

            head = df.head(5).to_string()
            cols = ", ".join(df.columns.tolist())
            summaries.append(
                f"[Dataset: {filename}] — {len(df)} rows | Columns: {cols}\nSample:\n{head}"
            )
        except Exception:
            continue

    if not summaries:
        return "No internal datasets loaded."

    return "\n\n".join(summaries)


def build_inventory_summary(inventory_items):
    if not inventory_items:
        return "No inventory items provided."

    header = "| Item | Cost (RM) | Sell (RM) | Margin % | Stock Qty | Units Sold | Est. Revenue (RM) | Stock Value (RM) |"
    separator = "|------|-----------|-----------|----------|-----------|------------|-------------------|------------------|"
    rows = []
    total_stock_value = 0
    total_est_revenue = 0

    for item in inventory_items:
        cost = item["cost_price"]
        sell = item["sell_price"]
        stock = item["stock_qty"]
        sold = item["units_sold"]

        profit_margin = ((sell - cost) / sell) * 100 if sell > 0 else 0
        est_revenue = sell * sold
        stock_value = cost * stock

        total_stock_value += stock_value
        total_est_revenue += est_revenue

        rows.append(
            f"| {item['name']} | {cost:.2f} | {sell:.2f} | {profit_margin:.1f} | {stock} | {sold} | {est_revenue:.2f} | {stock_value:.2f} |"
        )

    total_row = f"| **TOTALS** | | | | | | **{total_est_revenue:.2f}** | **{total_stock_value:.2f}** |"

    return "\n".join([header, separator] + rows + [total_row])
