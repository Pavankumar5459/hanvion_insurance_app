import streamlit as st
import pandas as pd

@st.cache_data
def load_cms_data():
    try:
        df = pd.read_csv("data/cms_procedures.csv")
        df["price_spread"] = df["max_price"] - df["min_price"]
        df["variation_ratio"] = (df["max_price"] / df["min_price"]).round(1)
        return df
    except Exception as e:
        st.error(f"Unable to load CMS procedures dataset: {e}")
        return None


def page_cms_costs():
    df = load_cms_data()
    if df is None or df.empty:
        st.markdown("<h2>CMS Cost Viewer</h2><p>No data available.</p>", unsafe_allow_html=True)
        return

    # Header
    st.markdown("""
        <h1 style="font-size: 36px; font-weight: 700;">Procedure Cost Explorer</h1>
        <p style="font-size: 17px; max-width: 780px; color: #555;">
            Explore benchmark prices for common medical procedures, based on national 
            price transparency patterns. These values are educational and not quotes 
            from any specific hospital or payer.
        </p>
        <br>
    """, unsafe_allow_html=True)

    # Filter card
    st.markdown("""
        <div style="background:#ffffff; padding:24px; border-radius:10px;
                    border:1px solid #eee; box-shadow:0px 4px 10px rgba(0,0,0,0.05);">
            <h4 style="margin-top:0;">Search Procedures</h4>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        search_text = st.text_input("Search by name or code (e.g., 99213, MRI, blood)")
    with col2:
        setting = st.selectbox(
            "Setting",
            ["All"] + sorted(df["setting"].unique().tolist())
        )

    filtered = df.copy()

    if search_text:
        s = search_text.lower()
        filtered = filtered[
            filtered["description"].str.lower().str.contains(s)
            | filtered["code"].astype(str).str.contains(s)
        ]

    if setting != "All":
        filtered = filtered[filtered["setting"] == setting]

    if filtered.empty:
        st.warning("No procedures found with the current filters.")
        return

    # Select one procedure
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-weight:700;'>Summary</h3>", unsafe_allow_html=True)

    proc_list = filtered["code"].astype(str) + " – " + filtered["description"]
    selected_label = st.selectbox("Select a procedure", proc_list)

    selected_code = selected_label.split(" – ")[0]
    row = filtered[filtered["code"].astype(str) == selected_code].iloc[0]

    # Summary cards
    st.markdown("""
        <div style="display:flex; gap:25px; flex-wrap:wrap; margin-top:10px;">
    """, unsafe_allow_html=True)

    # Median price
    st.markdown(f"""
        <div style="
            flex:1; min-width:240px; background:#ffffff; padding:22px;
            border-radius:12px; border:1px solid #eee;
            box-shadow:0px 4px 12px rgba(0,0,0,0.05);">
            <h4 style="margin-top:0;">Median Price</h4>
            <p style="font-size:30px; font-weight:700; margin:6px 0;">
                ${int(row['median_price'])}
            </p>
            <p style="font-size:13px; color:#777;">
                Typical negotiated rate across reporting providers.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Min–Max
    st.markdown(f"""
        <div style="
            flex:1; min-width:240px; background:#ffffff; padding:22px;
            border-radius:12px; border:1px solid #eee;
            box-shadow:0px 4px 12px rgba(0,0,0,0.05);">
            <h4 style="margin-top:0;">Price Range</h4>
            <p style="font-size:18px; margin:6px 0;">
                Minimum: <b>${int(row['min_price'])}</b><br>
                Maximum: <b>${int(row['max_price'])}</b>
            </p>
            <p style="font-size:13px; color:#777;">
                Spread: ${int(row['price_spread'])} 
                (variation ratio: {row['variation_ratio']}×).
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Sample size
    st.markdown(f"""
        <div style="
            flex:1; min-width:240px; background:#ffffff; padding:22px;
            border-radius:12px; border:1px solid #eee;
            box-shadow:0px 4px 12px rgba(0,0,0,0.05);">
            <h4 style="margin-top:0;">Data Coverage</h4>
            <p style="font-size:26px; font-weight:700; margin:6px 0;">
                {int(row['sample_size'])} providers
            </p>
            <p style="font-size:13px; color:#777;">
                Number of facilities used to derive these benchmarks.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Detailed info card
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background:#f8f9ff; padding:22px; border-radius:10px;
                    border:1px solid #e0e3ff;">
            <h4 style="margin-top:0;">Procedure Details</h4>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<p><b>Code:</b> {row['code']}<br>"
        f"<b>Description:</b> {row['description']}<br>"
        f"<b>Setting:</b> {row['setting']}</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='font-size:13px; color:#777;'>These benchmarks are derived from "
        "price transparency style data and are intended for education, not billing.</p>",
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Table of filtered procedures
    st.markdown("<br><h3 style='font-weight:700;'>All Matching Procedures</h3>", unsafe_allow_html=True)
    show_cols = ["code", "description", "setting", "median_price", "min_price", "max_price", "sample_size", "variation_ratio"]
    st.dataframe(filtered[show_cols].sort_values("median_price"), use_container_width=True)
