#import libraries
import streamlit as st
import pandas as pd
import altair as alt

#configure streamlit app
st.set_page_config(
  page_title = "Strava Stats",
  page_icon = ":bicyclist:",
  layout = "wide",
)

#create title & inital note
st.title("2023 Strava Statistics:athletic_shoe:")
st.write("Welcome to your (unofficial form of) Strava Wrapped. Please enjoy your personalized dashboard! Any questions or bugs? Text me or email me at gwinfield@utexas.edu.")
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
    total_time = data["Elapsed Time"].sum()/60
    avg_session = total_time / sessions
    minutes = int((avg_session % 1) * 60)
    
    if avg_session < 1:
      return st.write(f"Average Session Length: {minutes} minutes")
    else:
      hrs = int(avg_session // 1)
      return st.write(f"Average Session Length: {hrs} hours and {minutes} minutes")
      
  def total_sessions(data):
    sessions = len(data.index)
    return st.write(f"Number of Sessions: {sessions}")

  def total_time(data):
    data["Elapsed Time"] = data["Elapsed Time"]
    total_time = data["Elapsed Time"].sum() #in min
    return st.write(f"Total Time: {round(total_time/60, 2)} hours")

#def graph_by_month(data):
    #chart = alt.Chart(data).mark_bar().encode(
        #x=alt.X('month:N', sort=months_order),
        #y='count'
   # )
    #return st.altair_chart(chart, use_container_width=True)
  
  def time_per_month_graph(data):
    st.subheader("Time (in hrs) Spent by Month")
    time_by_month = data.groupby("Month")["Elapsed Time"].sum().reset_index()
    #return st.bar_chart(time_by_month, color=["#fc4c02"])
    time_by_month["Elapsed Time (hrs)"] = time_by_month["Elapsed Time"] / 60
    return st.bar_chart(time_by_month.set_index("Month")["Elapsed Time (hrs)"], color="#fc4c02")
    #st.write(time_by_month.head())

  months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
  
  def sessions_per_month_graph(data):
    st.subheader("Count by Month")
    month_counts = data['Month'].value_counts()
    chart = alt.Chart(month_counts).mark_bar().encode(
      x=alt.X('Month:N', sort=months_order),
      y='count:Q'
    )
    return st.altair_chart(chart, use_container_width=True)
    #return st.write(month_counts.head())
    
    #st.bar_chart(month_counts, color=["#1ebbd7"])


  activities_list = activities['Activity Type'].unique().tolist()
  activities_list.insert(0, "All Activities")
  activity_tabs = st.tabs(activities_list)
  filtered_activities = {}
  
  for activity, tab in zip(activities_list, activity_tabs):
    with tab:
      if activity != "All Activities":
        filtered_activities[activity] = activities.loc[activities['Activity Type'] == activity].copy()
        st.header("Relevant Statsitics")

        avg_session(filtered_activities[activity])
      
        if "Ride" in activity or "Run" in activity or "Walk" in activity or "Hike" in activity:
          total_distance = filtered_activities[activity]["Distance"].sum()
          st.write(f"Total Distance: {round(total_distance,2)} miles")
          longest_distance = filtered_activities[activity]["Distance"].max()
          st.write(f"Longest Distance: {round(longest_distance,2)} miles")
          
          if "Ride" in activity:
            avg_pace = total_distance / filtered_activities[activity]["Moving Time"].sum()
            st.write(f"Average Pace: {round(avg_pace*60, 2)} mph")
      
          elif "Run" in activity:
            avg_mile_time = filtered_activities[activity]["Moving Time"].sum() / total_distance
            run_min = int(avg_mile_time // 1)
            run_sec = int((avg_mile_time % 1) * 60)
            st.write(f"Average Mile Time: {run_min}:{run_sec:02d}")

          else:
            pass
      
        st.markdown("""---""")
      
        col1, col2 = st.columns(2)
      
        with col1:
          #time per month graph
          time_per_month_graph(filtered_activities[activity])
          total_time(filtered_activities[activity])
        
        with col2:
          #count per month graph
          sessions_per_month_graph(filtered_activities[activity])
          total_sessions(filtered_activities[activity])

      else:
        st.header("Way to go!")
        st.write(f"- You worked out an average of {round(len(activities.index)/365*7, 1)} days a week")
        
        act_count = activities["Activity Type"].value_counts()
        st.write(f"- Your top activity was {act_count.idxmax()}")

        month_count = activities["Month"].value_counts()
        st.write(f"- Your most active month was {month_count.idxmax()} with {month_count.max()} activities")
        
        st.markdown("""---""")
        
        col1, col2 = st.columns(2)
      
        with col1:
          #time per month graph
          time_per_month_graph(activities)
          total_time(activities)
        
        with col2:
          #count per month graph
          sessions_per_month_graph(activities)
          total_sessions(activities)
      
else:
  pass
 
