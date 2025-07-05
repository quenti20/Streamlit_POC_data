import streamlit as st
import json
import pandas as pd

def load_data(json_file="data.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    st.set_page_config(page_title="Modicare Product Search", layout="wide")
    st.title("🔍 Modicare Product Explorer")

    # Load and prepare data
    data = load_data()
    df = pd.DataFrame(data)

    # Filter out non-product rows (sections only)
    product_df = df[df["is_section"] != True].copy()
    product_df = product_df[product_df["Product and Net Content"].notnull()]

    # Calculate Retail Price (40% of DP)
    product_df["Retail Price (RP)"] = pd.to_numeric(product_df["DP(Rs.)"], errors='coerce') * 0.40
    product_df["Retail Price (RP)"] = product_df["Retail Price (RP)"].round(2)

    # Dropdown of product names
    product_names = product_df["Product and Net Content"].tolist()
    selected_product = st.selectbox("🔎 Search for a product", options=product_names)

    if selected_product:
        # Extract the selected product data
        selected_row = product_df[product_df["Product and Net Content"] == selected_product].iloc[0]
        product_details = selected_row.to_dict()

        # Remove 'is_section' if still present (safety check)
        product_details.pop("is_section", None)

        # Display product details
        st.markdown("### 📦 Product Details")
        for key, value in product_details.items():
            st.markdown(f"**{key}**: {value}")

if __name__ == "__main__":
    main()
