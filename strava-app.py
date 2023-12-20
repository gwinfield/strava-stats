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
  original_activities = pd.read_csv(file)
  st.write(original_activities)

st.subheader("See your stats!")
  
def transform_data(data):
  new_df = data[['Activity Date', 'Activity Type', 'Elapsed Time', 'Distance', 'Moving Time']]
  return new_df.head()

def km_to_mi(km):
  return km*0.621371

def sec_to_min(sec):
  return sec/60
  
def conversions(data):
  data['Distance'] = data['Distance'].apply(km_to_mi)
  data['Elapsed Time'] = data['Elapsed Time'].apply(sec_to_min)
  data['Moving Time'] = data['Moving Time'].apply(sec_to_min)
  return data

activities = transform_data(original_activities)

st.dataframe(data=activities)

#[theme]
#primaryColor = '#fc4c02'
#backgroundColor = '#ffffff'
#textColor = '#OOOO8O'
