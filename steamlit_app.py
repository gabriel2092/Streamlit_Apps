import snowflake.connector
import streamlit
import pandas
import requests
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner')

streamlit.header('🐔Breakfast Menu')
streamlit.text('🥣Omega 3 and Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🍞Hard Boiled Egg')
streamlit.text('🥑Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#need to correct indez 
my_fruit_list = my_fruit_list.set_index('Fruit')

#Put in a multiselect to pick the fruit
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

#Header Fruit Advice
streamlit.header("Fruityvice Fruit Advice!")

try:  
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())#create function to normalize json
    # Creates dataframe of normalized fruit.
    streamlit.dataframe(fruityvice_normalized)
except URLERROR as e:
  streamlit.error()
    
streamlit.write('The user entered ', fruit_choice)

#new section to display API response

#streamlit.text(fruityvice_response)

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contains:")
streamlit.dataframe(my_data_row)

fruit_choice = streamlit.text_input('What fruit would you like information about?','jackfruit')
streamlit.write('Thanks for adding ', fruit_choice)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")


