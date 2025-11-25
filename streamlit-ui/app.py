
import streamlit as st
import subprocess

st.title("Distributed Big Data Pipeline")

if st.button("Run Distributed Stock Prediction Pipeline"):
    subprocess.Popen(["python", "../spark-job/advanced_stock_pipeline.py"], shell=True)
    st.success("Distributed pipeline started!\nCheck Spark UI at http://localhost:8080")

