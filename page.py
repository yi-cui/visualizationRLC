# Your Name
# si649f20

# imports we will use
import altair as alt
import pandas as pd
import streamlit as st
import pprint
from vega_datasets import data

#Import all data

df = pd.read_csv('economics.csv')
df2 = pd.read_csv('educationall.csv')
df3 = pd.read_csv('educationrlc.csv')
df['id'] = pd.to_numeric(df['id'])
dfprefer = pd.read_csv('preference.csv')
dflo = pd.read_csv('uscounties.csv')
dfall = dfprefer.merge(dflo, how='inner', on='id')
df_c = alt.pd.DataFrame([
      {
        "Educationlevel": "Less than high school",
        "Year": "1970",
        "Percent": 0.60,
      },
      {
        "Educationlevel": "High school",
        "Year": "1970",
        "Percent": 0.242,
      },
      {
        "Educationlevel": "Some college",
        "Year": "1970",
        "Percent": 0.095,
      },
      {
        "Educationlevel": "College or higher",
        "Year": "1970",
        "Percent": 0.063,
      },
      {
        "Educationlevel": "Less than high school",
        "Year": "1980",
        "Percent": 0.454,
      },
      {
        "Educationlevel": "High school",
        "Year": "1980",
        "Percent": 0.364,
      },
      {
        "Educationlevel": "Some college",
        "Year": "1980",
        "Percent": 0.112,
      },
      {
        "Educationlevel": "College or higher",
        "Year": "1980",
        "Percent": 0.07,
      },
      {
        "Educationlevel": "Less than high school",
        "Year": "1990",
        "Percent": 0.357,
      },
      {
        "Educationlevel": "High school",
        "Year": "1990",
        "Percent": 0.324,
      },
      {
        "Educationlevel": "Some college",
        "Year": "1990",
        "Percent": 0.226,
      },
      {
        "Educationlevel": "College or higher",
        "Year": "1990",
        "Percent": 0.093,
      },
      {
        "Educationlevel": "Less than high school",
        "Year": "2000",
        "Percent": 0.212,
      },
      {
        "Educationlevel": "High school",
        "Year": "2000",
        "Percent": 0.382,
      },
      {
        "Educationlevel": "Some college",
        "Year": "2000",
        "Percent": 0.298,
      },
      {
        "Educationlevel": "College or higher",
        "Year": "2000",
        "Percent": 0.107,
      },{
        "Educationlevel": "Less than high school",
        "Year": "2015",
        "Percent": 0.074,
      },
      {
        "Educationlevel": "High school",
        "Year": "2015",
        "Percent": 0.375,
      },
      {
        "Educationlevel": "Some college",
        "Year": "2015",
        "Percent": 0.39,
      },
      {
        "Educationlevel": "College or higher",
        "Year": "2015",
        "Percent": 0.162,
      }])

#First Visualization
#Title
st.header("Economy")

#Selector
base = alt.Chart(df).properties(height = 300, width = 300)
selection1 = alt.selection_multi(fields=['Area'], bind='legend')
brush1 = alt.selection_interval(encodings = ['x','y'])
brush2 = alt.selection_interval(encodings=["x"])
opacity=alt.condition(selection1, alt.value(0.4), alt.value(0.05))

#Plot
redlake = pd.DataFrame({
    'x': [6],
    'y': [9.7],
    'Area':['Red Lake County']
})

plot = base.mark_point(opacity=0.4,filled = True,size = 10).encode(
    alt.X('Unemployrate:Q',axis=alt.Axis(title='unemployment rate(%)')),
    alt.Y('propertyrate:Q',axis=alt.Axis(title='poverty rate(%)')),
    color=alt.condition(brush1, 'Area:N', alt.value('lightgray')),
    opacity=opacity,
    tooltip = "County:N",
).add_selection(brush1).add_selection(selection1).transform_filter(brush2)


point = alt.Chart(redlake).mark_point(color='black', size = 80,filled = True).encode(
    alt.X('x:Q'),
    alt.Y('y:Q'),
    alt.Color('Area:N',sort=['Red Lake County','West','South','Midwest','Northeast'])
)

histogram = base.mark_bar().encode(
    alt.X('medianIncome:Q',
         bin=alt.Bin(step=5000),
         axis = alt.Axis(title = 'median income')),
    alt.Y('count(medianIncome):Q'),
    color = alt.Color('Area:N'),
    tooltip= 'Area:N'
).add_selection(brush2).transform_filter(selection1).transform_filter(brush1)

line1 = alt.Chart(pd.DataFrame({'x': [50332],'y':['Red lake county']})).mark_rule(color = 'red',size = 3).encode(
    x='x')

line2 = base.mark_rule(color = 'black',size = 3).encode(
    x = 'median(medianIncome):Q',
).transform_filter(selection1).transform_filter(brush1).transform_filter(brush2)

line3 = base.mark_rule(color = 'black',size = 2).encode(
    x = 'median(Unemployrate):Q'
).transform_filter(selection1).transform_filter(brush1).transform_filter(brush2)

line4 = base.mark_rule(color = 'black',size = 2).encode(
    y = 'median(propertyrate):Q'
).transform_filter(selection1).transform_filter(brush1).transform_filter(brush2)

#Combination
vis1 = ((histogram+line1+line2) | (plot+point+line3+line4))

# Show vis
st.markdown("The visualization below shows the overall economic situation as well as the Red Lake County's level in 2015. The black lines in both graph show the median level of selected variable, the red line and red dot represent the Red Lake County. ")
vis1





#Second Visualization
#Title
st.header("Education")

#Data wrangling
education_long = pd.wide_to_long(df2, ["low", "high"], i=['FIPS Code','State','Area name'], j="Year")
education_long = education_long.reset_index()
df4 = df3.pivot(index='Year', columns='education', values='Percent')
educationrcl = df4.reset_index()
alt.data_transformers.disable_max_rows()

#Selector
selection2 = alt.selection_single(fields=['Year'])
color_scale = alt.Scale(
    domain=["Less than high school","High school","Some college","College or higher"]
)


#Plot
base2 = alt.Chart(education_long)
rect = base2.mark_rect().encode(
    alt.X('low:Q', bin=True , sort = 'descending', axis = alt.Axis(title = 'less than high school education(%)')),
    alt.Y('high:Q', bin=True,axis = alt.Axis(title = 'college education or higher(%)')),
    alt.Color('count()',
        scale=alt.Scale(scheme='greenblue'),
        legend=alt.Legend(title='Total Records')
)).transform_filter(selection2).properties(
    width=250,
    height=250
)

circ2 = alt.Chart(pd.DataFrame({'x': [60,45.4,35.7,21.2,7.4],'y':[6.3,7.0,9.3,10.7,16.2],'Year':[1970,1980,1990,2000,2015]})).mark_point(filled = True,size = 300).encode(
    x='x',
    y = 'y',
    color = alt.Color('Year:N',scale=alt.Scale(scheme='reds'))
).transform_filter(selection2)


# bar = alt.Chart(df_c).mark_bar().transform_calculate(
#     order="{'Less than high school':3, 'High school': 2, 'Some college': 1, 'College or higher': 0}[datum.Educationlevel]"  
# ).encode(
#     x='Year:N',
#     y=alt.Y('Percent:Q', scale = alt.Scale(domain = (0,1))),
#     color=alt.Color(
#         'Education level:N',
#         scale=color_scale, 
#         sort=["Less than high school","High school","Some college","College or higher"]),
#     order='order:O',
#     opacity = alt.condition(selection2, alt.value(1), alt.value(0.3))
# ).add_selection(selection2).properties(width = 250, height = 250)

bar = alt.Chart(df3).mark_bar().transform_calculate(
    order="{'Less than high school':0, 'High school': 1, 'Some college': 2, 'College or higher': 3}[datum.education]"  
).encode(
    x=alt.X('Year:N'),
    y=alt.Y('Percent:Q'),
    color=alt.Color(
        'education:N',
        scale=color_scale, 
        sort=["Less than high school","High school","Some college","College or higher"]),
        order='order:O', 
        opacity = alt.condition(selection2, alt.value(1), alt.value(0.3))
).add_selection(selection2).properties(
    width=250,
    height=250
)

#Combination
vis2 =(bar |rect + circ2).resolve_legend(
    color="independent")

#Show vis
st.markdown('The visualization on the left shows the change in education level in Red Lake County over years. The red dots in the heatmap represents the education level in Red Lake County, it shows the level of education in Red Lake County compared to other counties in the specific year.')
vis2


#Title
st.header("Select your preference for living:")
#set value
valuenature = st.slider('Select your value for the natural amenties of a place.', 1.0, 100.0, (20.0))

valuesincome = st.slider('Select your value for the median income of a place', 1.0, 100.0, (20.0))

valueexpense = st.slider('Select your value for living expense of a place', 1.0, 100.0, (20.0))

valuepop = st.slider("Select your prefrence for population. (<0 means you prefer less people, >0 means you prefer more people. Otherwise, you don't care about that", -50.0, 50.0, (0.0))

#select
selection3 = alt.selection_single(fields=['County'], on = 'mouseover',empty = 'none')
selection4 = alt.selection_single(fields=['County'], on = 'mouseover', empty = 'none')
colorCondition2 = alt.condition(selection4, alt.value('darkred'),alt.value('#ed8181'))
colorCondition = alt.condition(selection3, alt.value('#273C7C'),alt.value('#5a8ac4'))

#Chart
base3 = alt.Chart(dfall).transform_calculate(
    score = alt.datum.median_income * valuesincome + alt.datum.rating * valuenature - alt.datum.livingExpense * valueexpense + alt.datum.Population * valuepop
).transform_window(
    sort = [alt.SortField('score',order = 'descending')],
    toprank = 'rank(*)'
).transform_window(
    sort = [alt.SortField('score',order = 'ascending')],
    bottomrank = 'rank(*)'
)

barchartblue = base3.mark_bar().encode(
    alt.X('score:Q'),
    alt.Y('County:N',sort='-x'),
    tooltip = 'County:N',
    opacity = alt.condition(selection3,alt.value(1.0),alt.value(0.7))
).transform_filter( 
    alt.datum.toprank < 11
).add_selection(selection3)

barchartred = base3.mark_bar(color = 'darkred').encode(
    alt.X('score:Q'),
    alt.Y('County:N',sort='-x'),
    tooltip = 'County:N',
    opacity = alt.condition(selection4,alt.value(1.0),alt.value(0.7))
).transform_filter( 
    alt.datum.bottomrank < 11
).add_selection(selection4)

vis3 = (barchartblue + barchartred).resolve_scale(y='shared').properties(title = 'Top & Bottom 10 Counties according to your preference', width = 300,height = 300)


states = alt.topo_feature(data.us_10m.url, feature='counties')
# US states background
background = alt.Chart(states).mark_geoshape(
    fill='lightgray',
    stroke='white'
).properties(
    width=500,
    height=300
).project('albersUsa')

pointsblue = base3.mark_circle(size = 200).encode(
    longitude='lng:Q',
    latitude='lat:Q',
    tooltip = 'County:N',
    color = colorCondition
).transform_filter(
    alt.datum.toprank < 11
)

pointsred = base3.mark_circle(size = 200).encode(
    longitude='lng:Q',
    latitude='lat:Q',
    tooltip = ['County:N','score:Q'],
    color = colorCondition2
).transform_filter(
    alt.datum.bottomrank < 11
).properties(
    title='Location of the your best & worst counties'
)



vis4 =  vis3 | (background + pointsred + pointsblue)
# airport positions on background
vis4