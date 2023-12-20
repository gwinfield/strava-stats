import streamlit as st
import pandas as pd

st.set_page_config(
  page_title = "Strava Stats",
  page_icon = ":bike:",
)

st.title("2023 Strava Statistics:athletic_shoe:")
st.write("Welcome to (an unofficial form of) Strava Wrapped for 2023! Please enjoy your personalized dashboard.")

st.subheader("File Upload")
st.write("Click here to learn how to download your data.\nOnce you've downloaded gthe zip file, download the "activities.csv" file.")

file = st.file_uploader("Upload your Strava data!", key="loader", type='csv')

if file != None:
  df = pd.read_csv(file)
  st.write(df)



#[theme]
#primaryColor = '#fc4c02'
#backgroundColor = '#ffffff'
#textColor = '#OOOO8O'
