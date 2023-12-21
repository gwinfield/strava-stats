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
    new_df['Month'] = new_df['Activity Date'].dt.month_name()
    new_df['Day'] = new_df['Activity Date'].dt.day
    new_df['Year'] = new_df['Activity Date'].dt.year
    new_df = new_df.drop(columns=['Activity Date'])

    #filter data by year
    new_df = new_df.loc[new_df['Year'] == 2023]

    #return transformed df
    return new_df

  activities = transform_data(original_activities)

  tab1, tab2, tab3, tab4 = st.tabs(["Relevent Stats", "Number of Activities by Month", "Time Spent by Month", "Data Preview"])

  st.sidebar.header("Apply filters here")
  activity = st.sidebar.multiselect("Activity Type:", options = activities["Activity Type"].unique(), default = activities["Activity Type"].unique())

  activities_filtered = activities.query("`Activity Type` == @activity")

  with tab1:
    st.header("Relevant Stats")
      
  with tab2:
    st.header("Count by Month")
    month_counts = activities_filtered['Month'].value_counts()
    st.bar_chart(month_counts, color=["#fc4c02"])
     
  with tab3:
    st.header("Time Spent by Month")
    time_by_month = activities_filtered.groupby("Month")["Elapsed Time"].mean()
    st.write(time_by_month.head(5))
    #st.bar_chart(time_by_month, x=["Month"], y=["Elapsed Time"], color=["#fc4c02"])

  with tab4:
    st.header("Data Preview")
    st.write(activities_filtered.head(15))
    
else:
  pass
   
#months_categories = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
  #month_counts['Months'] = pd.Categorical(month_counts['Months'], categories = months_categories)

#pass

#months_categories = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    #month_counts['Months'] = pd.Categorical(month_counts['Months'], categories = months_categories)

#month = st.sidebar.multiselect("Month:", options = activities["Month"].unique(), default = activities["Month"].unique())
  #dotw = st.sidebar.multiselect("Day of the Week:", options = activities["Day of the Week"].unique(), default = activities["Day of the Week"].unique())

# def create_tabs(data):
    #activities_list = data['Activity Type'].unique().tolist()
  #  filtered_activities = {}

 #   for tab in st.tabs(activities_list):
 #     filtered_activities[tab] = data.loc[data['Activity Type'] == tab].copy()
  #    st.dataframe(data=filtered_activities[tab])

  #create_tabs(activities)
      
#for key in filtered_activities.keys():
      #st.tabs([key])

  #tab1, tab2, tab3 = st.tabs(["Bar Graph", "Statistics", "Data"])

  #with tab1:
    #st.header("Count of Activity Types")
    #activity_counts = activities['Activity Type'].value_counts()
    #st.bar_chart(activity_counts)
     
  #with tab2:
    #st.header("Stats")

  #with tab3:
    #st.header("Data Preview")
    #st.write(activities.head(15))

#activity_counts = activities['Activity Type'].value_counts()

#st.bar_chart(activity_counts)


#st.dataframe(data=activities)

#[theme]
#primaryColor = '#fc4c02'
#backgroundColor = '#ffffff'
#textColor = '#OOOO8O'
