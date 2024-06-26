# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your customize smoothie")

# add namebox
name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections = 5
    )
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredient_string = ''
    for fruit_chosen in ingredients_list:
        ingredient_string += fruit_chosen + ' '
    # st.write(ingredient_string)

    if ingredient_string:

        my_insert_stmt = """insert into smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
                    values ('""" + ingredient_string +"""', '"""+name_on_order + """')""" 

        # st.write(my_insert_stmt)
        # st.stop()
        time_to_insert = st.button("Submit Order", type="primary")
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered')
