import sqlite3
import pandas as pd
import openpyxl
import streamlit as st
import base64
from io import StringIO, BytesIO
def generate_excel_download_link(df4):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    df3.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)

st.set_page_config(page_title='History')
st.title('Вскрываем историю браузера')
st.subheader('Добавьте ваш файл')

uploaded_file = st.file_uploader('ВЫБИРИТЕ СВОЙ ФАЙЛ')
if uploaded_file:
#     con = sqlite3.connect(uploaded_file)
#     cur = con.cursor()

# df = cur.execute('''SELECT name from sqlite_master where type= "table"''')

# print(df.fetchall())


    df1 = pd.read_sql_query("""SELECT url, title, visit_count,
    datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime')
    FROM urls
    """, uploaded_file)
    # print(df1)

    df2 = pd.DataFrame(df1)
    df3 = df2.rename(columns={"datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime')": "Дата",
                              "url": "Адрес",
                              "title": "Имя запроса",
                              "visit_count": "Посещений страницы"
                              })
    df3['Месяц'] = df3['Дата'].dt.month
    df3['Год'] = df3['Дата'].dt.year
if st.checkbox('Сформировать файл для скачивания'):
    df4 = st.dataframe(df3)
    # df3.to_excel('Ваш файл.xlsx')

if st.checkbox('Сформировать ссылку для скачивания'):

    st.subheader('СКАЧАТЬ ФАЙЛ')
    generate_excel_download_link(df4)
