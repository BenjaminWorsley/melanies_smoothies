# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import when_matched

# Write directly to the app
st.title(f":cup_with_straw:  Pending Smoothie Orders: :cup_with_straw: {st.__version__}")
st.write(
  """Orders to be filled.
  """
)


from snowflake.snowpark.functions import col


import streamlit as st

#st.write("You selected:", options)
session = get_active_session()


my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#st.dataframe(data=my_dataframe, use_container_width=True)

if my_dataframe:
#st.write("You selected:", option, f":{option.lower()}:")
#my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order,ORDER_FILLED)
 #   values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
        
    if submitted:
        editable_df = st.data_editor(my_dataframe)
        #session.sql(my_insert_stmt).collect()
        st.success('Someone clicked the button', icon = '👍')
        
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        og_dataset.merge(edited_dataset
                         , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
else:
    st.success('No pending orders', icon = '👍')


#my_dataframe[0]
#st.write("You selected:", option, f":{option.lower()}:")
#options = st.multiselect(
#    "What are your favorite colors?",
#    list(my_dataframe)
#    default=["Yellow", "Red"],
#)


#if ingredients_list

