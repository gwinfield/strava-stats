#import libraries
import streamlit as st
import pandas as pd

#configure streamlit app
st.set_page_config(
  page_title = "Strava Stats",
  page_icon = ":bike:",
  layout = "wide",
)

#create title & inital note
st.title("2023 Strava Statistics:athletic_shoe:")
st.write("Welcome to your (unofficial form of) Strava Wrapped. Please enjoy your personalized dashboard! Any questions or bugs? Email me at gwinfield@utexas.edu!")
st.markdown("""---""")

#give user place to upload their activity data & explain the process
st.subheader("Upload your activity data")

web_url = "https://www.strava.com"
help_url = "https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export"

st.markdown("To obtain your Strava data, follow these tabs on the [Strava](%s) website:" %web_url)
st.write("My Account :arrow_forward: Delete or download your account :arrow_forward: Get started :arrow_forward: Request your archive") 
st.write("Once you've received the zip file via email, extract all files and upload the activities.csv file onto this page!")
st.markdown("Questions? Click [here](%s) to learn more." % help_url)

file = st.file_uploader(" ", key="loader", type='csv')

#once uploaded, this is where the magic happens
if file != None:
  
  original_activities = pd.read_csv(file)
  #st.write(original_activities)
  
  st.markdown("""---""")
  st.subheader("See your stats!")

  def km_to_mi(km):
    return km*0.621371

  def sec_to_min(sec):
      return sec / 60
  
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
    new_df['Month'] = new_df['Activity Date'].dt.month_name()
    new_df['Day'] = new_df['Activity Date'].dt.day
    new_df['Year'] = new_df['Activity Date'].dt.year
    new_df = new_df.drop(columns=['Activity Date'])

    #filter data by year
    new_df = new_df.loc[new_df['Year'] == 2023]

    #return transformed df
    return new_df

  activities = transform_data(original_activities)

  def avg_session(data):
    sessions = len(data.index)
    total_time = data["Elapsed Time"].sum() / 60
    avg_session = total_time / sessions
    minutes = int((avg_session % 1) * 60)
    if avg_session < 1:
      return st.write(f"Average Session Length: {minutes} minutes")
    else:
      sess_hrs = int(avg_session // 1)
      return st.write(f"Average Session Length: {hrs} hours and {minutes} minutes")
      
  def total_sessions(data):
    sessions = len(data.index)
    return st.write(f"Number of Sessions: {sessions}")

  def total_time(data):
    total_time = data["Elapsed Time"].sum() / 60
    return st.write(f"Total Time: {round(total_time, 2)} hours")

  activities_list = activities['Activity Type'].unique().tolist()
  activities_list.insert(0, "Overview")
  activity_tabs = st.tabs(activities_list)
  filtered_activities = {}
  
  for activity, tab in zip(activities_list, activity_tabs):
    with tab:
      if activity != "Overview":
        filtered_activities[activity] = activities.loc[activities['Activity Type'] == activity].copy()
        st.header("Relevant Statsitics")

      avg_session(filtered_activities[activity])
      
      if "Ride" in activity:
        avg_pace = filtered_activities[activity]["Distance"].sum() / filtered_activities[activity]["Moving Time"].sum()
        st.write(f"Average Pace: {round(avg_pace*60, 2)} mph")
      
      if "Run" in activity:
        avg_mile_time = filtered_activities[activity]["Moving Time"].sum() / filtered_activities[activity]["Distance"].sum()
        run_min = int(avg_mile_time // 1)
        run_sec = int((avg_mile_time % 1) * 60)
        st.write(f"Average Mile Time: {run_min}:{run_sec:02d}")
      
      st.markdown("""---""")
      
      col1, col2 = st.columns(2)
      
      with col1:
        #time per month graph
        st.subheader("Time (in hrs) Spent by Month")
        filtered_activities[activity]["Elapsed Time"] = filtered_activities[activity]["Elapsed Time"]
        time_by_month = filtered_activities[activity].groupby("Month")["Elapsed Time"].sum()
        st.bar_chart(time_by_month, color=["#fc4c02"])

        total_time(filtered_activities[activity])
        
      with col2:
        #count per month graph
        st.subheader("Count by Month")
        month_counts = filtered_activities[activity]['Month'].value_counts()
        st.bar_chart(month_counts, color=["#1ebbd7"])

        total_sessions(filtered_activities[activity])

  else:
    col1, col2 = st.columns(2)
      
    with col1:
      #time per month graph
      st.subheader("Time (in hrs) Spent by Month")
      activities["Elapsed Time"] = activities["Elapsed Time"]
      time_by_month = activities.groupby("Month")["Elapsed Time"].sum()
      st.bar_chart(time_by_month, color=["#fc4c02"])

      total_time(activities)
        
    with col2:
      #count per month graph
      st.subheader("Count by Month")
      month_counts = activities['Month'].value_counts()
      st.bar_chart(month_counts, color=["#1ebbd7"])

      total_sessions(activities)
      
else:
  pass

#pass

#months_categories = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    #month_counts['Months'] = pd.Categorical(month_counts['Months'], categories = months_categories)

#month = st.sidebar.multiselect("Month:", options = activities["Month"].unique(), default = activities["Month"].unique())
  #dotw = st.sidebar.multiselect("Day of the Week:", options = activities["Day of the Week"].unique(), default = activities["Day of the Week"].unique())


#for key in filtered_activities.keys():
      #st.tabs([key])

 
