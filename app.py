import streamlit as st
import pandas as pd
from docutils.nodes import figure
from nltk.sem.chat80 import country
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

import preprocessor,helper
from helper import most_successful

@st.cache_data
def load_data():
    df = pd.read_csv('athlete_events.csv')
    regions_df = pd.read_csv('noc_regions.csv')
    df = preprocessor.preprocess(df, regions_df)
    return df, regions_df

with st.spinner("Loading and processing data... Please wait ⏳"):
    df, regions_df = load_data()

st.sidebar.title('120 Years Of Olympics Data Analysis')
st.sidebar.image('https://th.bing.com/th/id/OIP.GuVnTPFoeSDsU9CScE-oxAHaDt?rs=1&pid=ImgDetMain')
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis','Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.Country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Years', years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fatch_medal_tally(df, selected_year, selected_country)
    if selected_year =='Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally In " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall Performance ")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)

elif user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title(" Top Statistics ")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time= helper.data_overtime(df,'region')
    fig = px.line(nations_over_time, x= 'Year', y= 'region')
    st.title("Participating Nations Over The Years")
    st.plotly_chart(fig)

    events_over_time= helper.data_overtime(df,'Event')
    fig = px.line(events_over_time, x= 'Year', y= 'Event')
    st.title("Events Over The Years")
    st.plotly_chart(fig)

    athletes_over_time= helper.data_overtime(df,'Name')
    fig = px.line(athletes_over_time, x= 'Year', y= 'Name')
    st.title("Athletes Over The Years")
    st.plotly_chart(fig)

    st.title("No. of Events Overtime (Every Sport)")
    fig,ax = plt.subplots(figsize = (12,12))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot= True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].dropna().unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

elif user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country-wise Analysis")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country= st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + " Medal Tally Over The Years")
    st.plotly_chart(fig)

    st.title(selected_country + " Excels In The Following Sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(12,12))
    ax = sns.heatmap(pt,annot= True)
    st.pyplot(fig)

    st.title("Top 10 Athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

elif user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width= 1200, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1200, height=600)
    st.title("Distribution of Age With Respect To Sports (Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].dropna().unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title("Height vs Weight")
    selected_sport = st.selectbox('Select a Sport', sport_list, key='selected_sport')
    temp_df = helper.wight_vs_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(data=temp_df, x='Weight', y='Height', hue= temp_df['Medal'],style=temp_df['Sex'])
    st.pyplot(fig)

    st.title("Men vs Women Participation Over The Years")
    final = helper.Men_vs_Women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1200, height=600)
    st.plotly_chart(fig)


