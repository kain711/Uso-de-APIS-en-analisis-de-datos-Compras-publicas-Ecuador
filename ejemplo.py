import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import plotly.express as px
def obtener_analizar_datos():

    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)

    if response.status_code == 200:
        users = response.json()
    else:
        #st.warning("Error al obtener los datos de la API")
        #st.print("Error al consumir la API")
        st.error("Error al obtener los datos de la API")

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        username TEXT,
        email TEXT,
        phone TEXT,
        website TEXT
    )
    ''')
    for user in users:
        cursor.execute('''
        INSERT OR REPLACE INTO users (id, name, username, email, phone, website)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user['id'],
            user['name'],
            user['username'],
            user['email'],
            user['phone'],
            user['website']
        ))
    conn.commit()
    conn.close()
    st.success("Datos obtenidos y guardados exitosamente.")
    
    st.header("Inicio del analisis de datos")
    conn = sqlite3.connect('usuarios.db')
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()

    st.write(df)

    
    df['name_length'] = df['name'].apply(len)
    st.write("Longitud de los nombres de los usuarios: ")
    
    st.write(df.name_length.head())
    
    st.subheader('Longitud de los nombres de los usuarios')
    frecuencia=df['name_length'].value_counts().reset_index()
    frecuencia.columns=['Cantidad de caracteres','Frecuencia']
    st.bar_chart(frecuencia.set_index('Cantidad de caracteres'),y='Frecuencia')
    
    st.subheader('Distribucion de los dominos de correo')
    #crear un grafico de barras inteactivo con plotly
    df['email_domain'] = df['email'].apply(lambda x: x.split('@')[-1])
    dominios=df['email_domain'].value_counts().reset_index()
    dominios.columns=['Dominio','Cantidad']
    
    fig=px.bar(dominios,x='Dominio',y='Cantidad',color='Dominio',title='Cantidad de usuarios por dominio de correo')
    st.plotly_chart(fig,use_container_width=True)
   
    
    

st.title("Analisis de Usuarios")
st.write("Obtener datos desde una API y analizarlos 🧮")
st.subheader("Para empezar presiona el boton de abajo 👇")
if st.button("Obtener y analizar datos" ):
    obtener_analizar_datos()
    st.success("Datos obtenidos y analizados exitosamente.")