import streamlit as st
import pandas as pd

st.set_page_config(
  page_title = "Strava Stats",
  page_icon = ":bike:",
  layout = "wide",
)

st.title("2023 Strava Statistics:athletic_shoe:")
st.write("Welcome to (an unofficial form of) Strava Wrapped. Please enjoy your personalized dashboard.\n")

st.subheader("Upload your activity data here!")

url = "https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export"
st.markdown("Click [here](%s) to learn how to download your data.\nOnce you've downloaded the zip file, download the activities.csv file." % url)

file = st.file_uploader("Drop your activities file in a csv format", key="loader", type='csv')

if file != None:
  activities = pd.read_csv(file)
  st.write(activities)
else:
  activities = pd.Data_Frame()

st.subheader("See your stats!")

#[theme]
#primaryColor = '#fc4c02'
#backgroundColor = '#ffffff'
#textColor = '#OOOO8O'
