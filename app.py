import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file, encoding="latin1")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    return df

st.title("E-Commerce Sales Analysis")
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.write("### Dataset Overview", df.head())
    
    # Plot 1: Top 10 Selling Products
    st.subheader("Top 10 Selling Products")
    top_products = df["Description"].value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=top_products.values, y=top_products.index, palette="viridis", ax=ax)
    ax.set_xlabel("Sales Count")
    ax.set_ylabel("Product Description")
    st.pyplot(fig)
    
    # Plot 2: Sales by Country
    st.subheader("Top 10 Countries by Transactions")
    top_countries = df["Country"].value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=top_countries.values, y=top_countries.index, palette="magma", ax=ax)
    ax.set_xlabel("Number of Transactions")
    ax.set_ylabel("Country")
    st.pyplot(fig)
    
    # Plot 3: Sales Trend Over Time
    st.subheader("Sales Trend Over Time")
    fig, ax = plt.subplots()
    df.resample("M", on="InvoiceDate")["Quantity"].sum().plot(marker="o", color="b", ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales")
    ax.grid(True)
    st.pyplot(fig)
    
    # Plot 4: Unit Price Distribution
    st.subheader("Unit Price Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df["UnitPrice"], bins=50, kde=True, color="g", ax=ax)
    ax.set_xlim(0, df["UnitPrice"].quantile(0.99))
    st.pyplot(fig)
    
    # Plot 5: Top 10 Customers by Purchase Volume
    st.subheader("Top 10 Customers by Purchase Volume")
    top_customers = df.groupby("CustomerID")["Quantity"].sum().nlargest(10)
    fig, ax = plt.subplots()
    sns.barplot(x=top_customers.values, y=top_customers.index, palette="coolwarm", ax=ax)
    ax.set_xlabel("Total Quantity Purchased")
    ax.set_ylabel("Customer ID")
    st.pyplot(fig)
    
    # Plot 6: Monthly Revenue Trend
    st.subheader("Monthly Revenue Trend")
    fig, ax = plt.subplots()
    df.resample("M", on="InvoiceDate")["Revenue"].sum().plot(marker="o", color="r", ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Revenue")
    ax.grid(True)
    st.pyplot(fig)
    
    # Plot 7: Quantity Distribution
    st.subheader("Distribution of Purchase Quantities")
    fig, ax = plt.subplots()
    sns.boxplot(x=df["Quantity"], color="orange", ax=ax)
    ax.set_xlim(df["Quantity"].quantile(0.01), df["Quantity"].quantile(0.99))
    st.pyplot(fig)
else:
    st.warning("Please upload a CSV file to analyze the data.")
