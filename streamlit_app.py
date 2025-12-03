# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session # 修正: get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """ Choose the fruits you want in your custom Smoothie:
    """)

# 修正: スペル修正
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# 修正: セッション取得とDataFrame作成
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')) # 修正: table, FRUIT_NAME, 閉じ括弧

# DataFrameをPythonリストに変換 (multiselectに渡すため)
# Snowpark DataFrameをStreamlitのウィジェットに直接渡すことはできないため、リスト化が必要です。
ingredients_options = my_dataframe.to_pandas()['FRUIT_NAME'].tolist()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,ingredients_options # 修正: リストを渡す
    ,max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
    values ('""" + ingredients_string + """ ',' """ +name_on_order + """ ')"""
