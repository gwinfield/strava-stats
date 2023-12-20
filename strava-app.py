import streamlit as st
import pandas as pd

st.title("2023 Strava Statistics:bike:")

file = st.fileuploader("Upload your Strava data is a .csv format!", key="loader", type="csv")

if file != None:
  df = pd.read_csv(file)
  st.write(df)

#[theme]
#primaryColor = '#fc4c02'
#backgroundColor = '#ffffff'
#textColor = '#OOOO8O'
