import streamlit as st
import json
import pandas as pd
import time

def load_data(json_file="data.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    st.set_page_config(page_title="🧴 Modicare Product Explorer", layout="wide")

    # --- 💅 Custom Styling ---
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to right, #0f0c29, #302b63, #24243e);
            color: #f5f5f5;
        }
        .stSelectbox > div > div {
            background-color: #1f1f2e;
            color: #ffffff;
            border-radius: 10px;
            border: 1px solid #444;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 25px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            margin-top: 20px;
        }
        .product-title {
            font-size: 26px;
            font-weight: 700;
            color: #8efff4;
            margin-bottom: 20px;
        }
        .product-row {
            margin-bottom: 12px;
        }
        .product-key {
            font-weight: 600;
            color: #c0c0ff;
        }
        .product-value {
            color: #ffffff;
        }
        .loading-text {
            font-size: 22px;
            font-weight: 500;
            color: #ff69b4;
            animation: blink 1.2s infinite;
            text-align: center;
            margin-top: 40px;
        }
        @keyframes blink {
            0% {opacity: 0.2;}
            50% {opacity: 1;}
            100% {opacity: 0.2;}
        }
        .formula-box {
            font-size: 14px;
            margin-top: 15px;
            background: rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.15);
            color: #ddddff;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='color:#8efff4;'>🧴 Modicare Product Explorer</h1>", unsafe_allow_html=True)

    # --- 📥 Load Data ---
    data = load_data()
    df = pd.DataFrame(data)
    product_df = df[df["is_section"] != True].copy()
    product_df = product_df[product_df["Product and Net Content"].notnull()]

    # 💸 Convert MRP and DP to numeric for calculation
    product_df["MRP(Rs.)"] = pd.to_numeric(product_df["MRP(Rs.)"], errors="coerce")
    product_df["DP(Rs.)"] = pd.to_numeric(product_df["DP(Rs.)"], errors="coerce")

    # 🧠 Search Dropdown
    product_names = product_df["Product and Net Content"].dropna().unique().tolist()
    selected_product = st.selectbox(
        "🔎 Type and select a product",
        options=[""] + product_names,
        index=0,
        placeholder="Start typing to search..."
    )

    # 🌀 Product display
    if selected_product:
        with st.spinner("Fetching product info..."):
            time.sleep(0.6)

            row = product_df[product_df["Product and Net Content"] == selected_product].iloc[0]
            result = row.to_dict()
            result.pop("is_section", None)

            # 💡 Calculate new values
            mrp = row["MRP(Rs.)"]
            dp = row["DP(Rs.)"]
            loyalty_discount = 25.00  # %
            price_diff = round(mrp - dp, 2)
            percent_reduction = round((price_diff / mrp) * 100, 2)
            total_discount = round(loyalty_discount + percent_reduction, 2)
            selling_price = round(mrp * (1 - total_discount / 100), 2)

            # 🧾 Styled card
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="product-title">{result.get("Product and Net Content", "Unnamed Product")}</div>', unsafe_allow_html=True)

            for key, value in result.items():
                if key != "Product and Net Content":
                    st.markdown(
                        f'<div class="product-row"><span class="product-key">{key}:</span> '
                        f'<span class="product-value">{value}</span></div>',
                        unsafe_allow_html=True
                    )

            # --- 🧮 Show Calculated Fields ---
            st.markdown('<hr style="border: 1px solid #8efff4;">', unsafe_allow_html=True)
            st.markdown('<div class="product-title">💰 Pricing Insights</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="product-row"><span class="product-key">Price Difference:</span> <span class="product-value">₹ {price_diff:.2f}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="product-row"><span class="product-key">Discount from MRP (%):</span> <span class="product-value">{percent_reduction:.2f}%</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="product-row"><span class="product-key">Loyalty Discount:</span> <span class="product-value">25.00%</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="product-row"><span class="product-key">Total Discount %:</span> <span class="product-value">{total_discount:.2f}%</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="product-row"><span class="product-key">Selling Price (SP):</span> <span class="product-value">₹ {selling_price:.2f}</span></div>', unsafe_allow_html=True)

            # --- 📘 Formula Display ---
            st.markdown("""
                <div class="formula-box">
                <strong>🧮 Formulae Used:</strong><br>
                Price Difference = MRP - DP<br>
                % Reduction = (Price Difference / MRP) * 100<br>
                Loyalty Discount = 25%<br>
                Total Discount = % Reduction + Loyalty Discount<br>
                Selling Price (SP) = MRP × (1 - Total Discount / 100)
                </div>
            """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown('<div class="loading-text">🧠 Start typing above to explore products!</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
