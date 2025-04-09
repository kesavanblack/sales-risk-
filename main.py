import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import BytesIO

def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file, encoding="latin1")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    return df

def download_report(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sales Report', index=False)
    output.seek(0)
    return output

st.set_page_config(page_title="E-Commerce Sales Analysis", layout="wide")
st.title("📊 E-Commerce Sales Analysis")

uploaded_file = st.sidebar.file_uploader("📂 Upload CSV File", type=["csv"])

df = None
if uploaded_file is not None:
    df = load_data(uploaded_file)
    min_date, max_date = df["InvoiceDate"].min(), df["InvoiceDate"].max()
    date_range = st.sidebar.date_input("📅 Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
    df = df[(df["InvoiceDate"] >= pd.Timestamp(date_range[0])) & (df["InvoiceDate"] <= pd.Timestamp(date_range[1]))]
    
    menu = st.sidebar.radio("🔍 Select Analysis Section", ["Overview", "Product Analysis", "Customer Analysis", "Time Analysis", "Download Report"])
    
    if menu == "Overview":
        st.subheader("📌 Sales Overview")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("💰 Total Revenue", f"${df['Revenue'].sum():,.2f}")
        col2.metric("🛒 Total Orders", df['InvoiceNo'].nunique())
        col3.metric("👥 Unique Customers", df['CustomerID'].nunique())
        col4.metric("🌍 Unique Countries", df['Country'].nunique())
        col5.metric("💲 Average Unit Price", f"${df['UnitPrice'].mean():,.2f}")
        col6.metric("📦 Total Quantity Sold", df['Quantity'].sum())
    
    elif menu == "Product Analysis":
        st.subheader("🔥 Top 10 Selling Products")
        top_products = df["Description"].value_counts().head(10)
        fig = px.bar(top_products, x=top_products.values, y=top_products.index, orientation='h', title="Top Selling Products", labels={"x":"Sales Count", "y":"Product Description"})
        st.plotly_chart(fig)
        
        st.subheader("💰 Revenue by Product")
        revenue_products = df.groupby("Description")["Revenue"].sum().nlargest(10)
        fig = px.bar(revenue_products, x=revenue_products.values, y=revenue_products.index, orientation='h', title="Top Revenue Generating Products", labels={"x":"Total Revenue", "y":"Product Description"})
        st.plotly_chart(fig)
        
        st.subheader("📏 Average Order Value per Product")
        avg_order_value = df.groupby("Description")["UnitPrice"].mean().nlargest(10)
        fig = px.bar(avg_order_value, x=avg_order_value.values, y=avg_order_value.index, orientation='h', title="Average Order Value by Product", labels={"x":"Average Price", "y":"Product Description"})
        st.plotly_chart(fig)
        
        st.subheader("📦 Stock Availability vs. Sales")
        if "Stock" in df.columns:
            stock_vs_sales = df.groupby("Description")["Quantity"].sum().nlargest(10)
            fig = px.bar(stock_vs_sales, x=stock_vs_sales.values, y=stock_vs_sales.index, orientation='h', title="Stock vs Sales", labels={"x":"Total Sales Quantity", "y":"Product Description"})
            st.plotly_chart(fig)
        else:
            st.warning("⚠️ Stock data not available in the dataset.")
    
    elif menu == "Customer Analysis":
        st.subheader("🏆 Top 10 Returning Customers")
        top_customers = df.groupby("CustomerID")["Quantity"].sum().nlargest(10)
        fig = px.bar(top_customers, x=top_customers.index, y=top_customers.values, title="Top Returning Customers", labels={"x":"Customer ID", "y":"Total Quantity Purchased"})
        st.plotly_chart(fig)
    
    elif menu == "Time Analysis":
        st.subheader("📅 Sales Trend Over Time")
        df_monthly = df.resample("M", on="InvoiceDate")["Revenue"].sum()
        fig = px.line(df_monthly, x=df_monthly.index, y=df_monthly.values, title="Monthly Revenue Trend", labels={"x":"Month", "y":"Total Revenue"})
        st.plotly_chart(fig)
        
        st.subheader("⏳ Sales Heatmap")
        df['Hour'] = df["InvoiceDate"].dt.hour
        df['Day'] = df["InvoiceDate"].dt.dayofweek
        heatmap_data = df.pivot_table(index='Day', columns='Hour', values='Quantity', aggfunc='sum').fillna(0)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='.0f', linewidths=.5)
        st.pyplot(fig)
    
    elif menu == "Download Report":
        st.subheader("📥 Download Sales Report")
        output = download_report(df)
        st.download_button(label="Download Excel Report", data=output, file_name="sales_report.xlsx", mime="application/vnd.ms-excel")
else:
    st.warning("⚠️ Please upload a CSV file to analyze the data.")
