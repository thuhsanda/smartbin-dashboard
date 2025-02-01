import streamlit as st
import boto3
import pandas as pd

# AWS DynamoDB Client
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table('SmartBinData')

# Function to Fetch Data from DynamoDB
def get_bins():
    response = table.scan()
    return response['Items']

# Streamlit App
st.title("🗑️ SmartBin Dashboard")

# Fetch Bin Data
bins = get_bins()

# Convert to Pandas DataFrame for Display
df = pd.DataFrame(bins)

# Sort by Fill Level (Descending)
df = df.sort_values(by="fill_level", ascending=False)

# Display Table
st.dataframe(df)

# Highlight Bins Needing Collection
st.subheader("⚠️ Bins That Need Collection")
bins_full = df[df['fill_level'] >= 80]

if bins_full.empty:
    st.success("✅ No bins need collection right now!")
else:
    st.warning(f"🚨 {len(bins_full)} bins need immediate collection!")
    st.dataframe(bins_full)

# Live Updates (Auto Refresh)
st.button("🔄 Refresh Data", on_click=st.experimental_rerun)
 