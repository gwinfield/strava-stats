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

st.subheader("See your stats!")

if file != None:
  original_activities = pd.read_csv(file)
  #st.write(original_activities)

  def km_to_mi(km):
    return km*0.621371

  def sec_to_min(sec):
    return sec/60
  
  def transform_data(data):
    #filter data for relevant columns
    new_df = data[['Activity Date', 'Activity Type', 'Elapsed Time', 'Distance', 'Moving Time']]
  
    #apply conversion functions
    new_df['Distance'] = new_df['Distance'].apply(km_to_mi)
    new_df['Elapsed Time'] = new_df['Elapsed Time'].apply(sec_to_min)
    new_df['Moving Time'] = new_df['Moving Time'].apply(sec_to_min)

    #create date/time related columns
    new_df['Activity Date'] = new_df['Activity Date'].astype(str)
    new_df['Activity Date'] = pd.to_datetime(new_df['Activity Date'], format='%b %d, %Y, %I:%M:%S %p')
    new_df['Day of the Week'] = new_df['Activity Date'].dt.day_name()
    new_df['Month'] = new_df['Activity Date'].dt.month
    new_df['Day'] = new_df['Activity Date'].dt.day
    new_df['Year'] = new_df['Activity Date'].dt.year
    new_df['Hour'] = new_df['Activity Date'].dt.hour
    new_df = new_df.drop(columns=['Activity Date'])

    #filter data by year
    new_df = new_df.loc[new_df['Year'] == 2023]

    #return transformed df
    return new_df

  activities = transform_data(original_activities)

  tab1, tab2, tab3 = st.tabs(["Bar Graph", "Statistics", "Data"])

  with tab1:
    st.header("Count of Activity Types")
    activity_counts = activities['Activity Type'].value_counts()
    st.bar_chart(activity_counts)
     
  with tab2:
    st.header("Stats")

  with tab3:
    st.header("Data Preview")
    st.write(activities.head())
    
else:
  pass

#activity_counts = activities['Activity Type'].value_counts()

#st.bar_chart(activity_counts)


#st.dataframe(data=activities)

#[theme]
#primaryColor = '#fc4c02'
#backgroundColor = '#ffffff'
#textColor = '#OOOO8O'
