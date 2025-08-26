# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw:  Customize Your Smoothie!: :cup_with_straw: {st.__version__}")
st.write(
  """Choose what fruits you want in your Custom Smoothie.
  """
)

cnx = st.connection("snowflake")
session = cnx.session()


name_on_order = st.text_input("Name of Smoothie")
st.write("The Name of the smoothie will be", name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
#st.stop()


#st.write("You selected:", option, f":{option.lower()}:")
ingredient_list = st.multiselect(
    "Choose 5 ingredients",
    my_dataframe,
    max_selections =5
)



if ingredient_list:


    
    st.write(ingredient_list)
    st.text(ingredient_list)
    
    ingredients_string = ''

    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on.lower())
        st.subheader("Nuttritional Information " + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")





