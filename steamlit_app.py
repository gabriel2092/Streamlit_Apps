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
    
#streamlit.write('The user entered ', fruit_choice)

#new section to display API response

#streamlit.text(fruityvice_response)


#streamlit.header("The fruit load contains:")
#Snowflake-related functions


def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")   
        return my_cur.fetchall()

#Add a button to load the fruit

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values (' " + new_fruit + " ')")
        return 'Thanks for adding ' + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like information about?')
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows=get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

#streamlit.text("The fruit load list contains:")
#streamlit.dataframe(my_data_row)

streamlit.stop()





