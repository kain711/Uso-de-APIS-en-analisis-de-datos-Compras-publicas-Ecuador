import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#Configuracion de la pagina
st.set_page_config(
    page_title="Contrataciones Abiertas Ecuador-ODS",
    layout="wide",
    initial_sidebar_state="collapsed"
)
#Aplicar estilos personalizados
st.markdown("""
            <style>
            .main{
                padding-top: 2rem;
                padding-bottom: 2rem;
                padding-left:2rem;
                padding-right:2rem;
            }
           .title {
        font-size: 2.5rem;
        font-weight: 400;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 1rem;
    }
            .subtitle {
        font-size: 1 rem;
        font-weight: 400;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 2rem;
    }
    stSelectbox {
        background-color: #f5f5f5;
        border-radius: 5px;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0.5rem;
        width: 100%;
        
    }
    body{
        padding:0;
        margin:0;
        background-color: #1E1E1E;
        width:100%
    }
    graficos{
        display: flex;
        flex-direction:column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        bachground-color: #1E1E1E;
        border-radius: 10px;
        box-shadow:0 4px 8px rgba(0,0,0,0.1);
        color: #FFFFFF;
        
        
    }
    
            </style>
            """,unsafe_allow_html=True)
#crear divisiones para el titulo y el cuerpo 
st.markdown('<div class="main"></div>', unsafe_allow_html=True)
# crear la division cuerppo con sus configuraciones
st.markdown("""<div class=cuerpo>
            <style>
            .cuerpo{
                padding: 2rem;
                bachground-color: #1E1E1E;
                border-radius: 10px;
                box-shadow:0 4px 8px rgba(0,0,0,0.1);
                color: #FFFFFF;
                width: 100%;
                display: flex;
                flex-direction:column;
                align-items: center;
                justify-content: center;
            }
            </style>
            </div>""",unsafe_allow_html=True)



#Titulo y subtitulo
st.markdown('<div class="title">Contrataciones Abiertas Ecuador-ODS</div>',unsafe_allow_html=True)
st.markdown('<div class="subtitle">Puedes seleccionar las opciones deseadas para filtar los datos</div>',unsafe_allow_html=True)
#crear un cuadro de busqueda para palabras clave
palabra=st.text_input("Buscar palabra clave",placeholder="Palabra clave",label_visibility="collapsed")

#crear 4 columnas para los selectores
col1,col2,col3,col4=st.columns(4)
#opciones para los selectores
anios= ["2015","2016","2017","2018","2019","2020","2021","2022","2023","2024","2025","Todos los años"]

provincias = ["Todos"] + [
    "AZUAY", "BOLIVAR", "CAÑAR", "CARCHI", "CHIMBORAZO", "COTOPAXI", "EL ORO",
    "ESMERALDAS", "GALAPAGOS", "GUAYAS", "IMBABURA", "LOJA", "LOS RIOS",
    "MANABI", "MORONA SANTIAGO", "NAPO", "ORELLANA", "PASTAZA", "PICHINCHA",
    "SANTA ELENA", "SANTO DOMINGO DE LOS TSACHILAS", "SUCUMBIOS", "TUNGURAHUA",
    "ZAMORA CHINCHIPE"
]

tipos_contratacion = [
    "Todos",
    "Subasta Inversa Electrónica",
    "Obra artística, científica o literaria",
    "Menor Cuantía",
    "Lista corta",
    "Cotización",
    "Contratacion directa",
    "Catálogo electrónico - Mejor oferta",
    "Catálogo electrónico - Gran compra mejor oferta",
    "Catálogo electrónico - Compra directa",
    "Repuestos o Accesorios",
    "Licitación de Seguros",
    "Licitación",
    "Contratos entre Entidades Públicas o sus subsidiarias",
    "Comunicación Social-Contratación Directa",
    "Catálogo electrónico - Gran compra puja",
    "Bienes y Servicios únicos",
    "Transporte de correo interno o internacional",
    "Asesoría y Patrocinio-Jurídico"
]
#selectores en cada columna
with col1:
    st.text("Año")
    anio_seleccionado = st.selectbox("", anios, label_visibility="collapsed")

with col2:
    st.text("Provincia")
    provincia_seleccionada=st.selectbox("",provincias,label_visibility="collapsed")
    
with col3:
    st.text("Tipo de contratacion")
    tipo=st.selectbox("",tipos_contratacion,label_visibility="collapsed")
#url base de la API

url_base="https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api/get_analysis"


#se debe concatenar la url base con los parametros seleccionados solo si son seleccionados
if anio_seleccionado!="Todos los años":
    params={"year":anio_seleccionado}
    if provincia_seleccionada!="Todos":
        params["region"]=provincia_seleccionada
    if tipo!="Todos":
        params["type"]=tipo

        
        
    try:
        response = requests.get(url_base,params=params)
        data=response.json()
        if isinstance(data,list)and len(data)>0:
            df=pd.DataFrame(data) 
        else:
            st.write("No se encontraron datos para la palabra clave proporcionada.")
        if palabra!="Palabra clave":
            #buscar en el dataframe la palabra clave en el campo internal_type
            df=df[df['internal_type'].str.contains(palabra,case=False,na=False)]
                

    
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la API: {e}")
    st.write(df)
    #------------Crear una columna con los nombres de los meses---------------
    month_mapping={
        1:"Enero",
        2:"Febrero",
        3:"Marzo",
        4:"Abril",
        5:"Mayo",
        6:"Junio",
        7:"Julio",
        8:"Agosto",
        9:"Septiembre",
        10:"Octubre",   
        11:"Noviembre",
        12:"Diciembre"
        
    }


    #-------------------------Implementacion de los graficos resumen-----------------------------------------
    st.markdown('<div class="">Graficos</div>', unsafe_allow_html=True)
    #Crear pestanias para interactuar con los datos
    tab1,tab2,tab3,tab4=st.tabs(["Monto total por tipo de contratacion","Monto total por mes y tipo de contratacion","Monto vs cantidad de contratos","Distribucion de tipo de contratos realizados"])
    #preprocesamiento de datos
    if not df.empty and 'month' in df.columns and 'internal_type' in df.columns and 'total' in df.columns:
        #converir la columna total a numerico
        df['total']=pd.to_numeric(df['total'],errors='coerce')
        df['total']=df['total']/1000000
        #st.write(df.isnull().sum())
        df['month']=df['month'].astype(int)
        #reemplazar los numeros de mes por los nombres de los meses
        df['month']=df['month'].map(month_mapping).sort_index()
        #ordenar los meses
        df['month']=pd.Categorical(df['month'],categories=month_mapping.values(),ordered=True)
        df.dropna(subset=['internal_type','total'],inplace=True)

        #crear un grafico de linea temporal de los tipos de conttratos vs el monto total
        with tab1:
            #nombrar los tabs para una mejor presentacion
            st.markdown('<div class="title">Total por Tipo de contrataccion</div>',unsafe_allow_html=True)
            #st.markdown('<div class="subtitle">Total por Tipo de contrataccion</div>',unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 4))
            x = df['internal_type'].unique()
            #mostrar el monto total invertido con formato de moneda
            st.write("Monto total invertido:")  
          
    
            ax.bar(x, df.groupby('internal_type')['total'].sum().sort_index(), width=0.8)
            ax.set_xticks(x)
            ax.set_xticklabels(df['internal_type'].unique(), rotation=90)
            ax.set_xlabel('Tipo de Contratación')
            ax.set_ylabel('Monto Total (En millones USD)')
            #ax.set_title('Total por Tipo de Contratación')
            st.pyplot(fig)
            
            #crear un grafico temporal de los timpos de contratos vs el monto total y por mes
        with tab2:
            val=df.groupby(['month','internal_type'])['total'].sum()
            st.write(df.columns)        
                    #crear el grafico temporal
            fig2=px.line(val,x=val.index.get_level_values('month'),y=val.values,color=val.index.get_level_values('internal_type'),title="Monto por Mes y tipo de contratación",labels=({"x":"Mes","y":"Monto(USD)"}))
                    #actualizar el layout del grafico
            fig2.update_layout(title="Total por Tipo de contrataccion")
            st.plotly_chart(fig2,use_container_width=True)
        with tab3:
            #crear un grafico de dispersion de monto total vs cantidad de contratos
            st.markdown('<div class="title">Total por Tipo de contrataccion</div>',unsafe_allow_html=True)
            fig3,ax3=plt.subplots(figsize=(8,4))
            ax3.scatter(df['internal_type'],df['total'],alpha=0.5)
            ax3.set_xlabel('Tipo de Contratación')
            ax3.set_ylabel('Monto Total (USD)')
            ax3.set_title('Total por Tipo de Contratación')
            ax3.set_xticklabels(df['internal_type'].unique(),rotation=90)
            st.pyplot(fig3)
        with tab4:
            #crear un grafico de torta de la distribucion de tipos de contratos con plotly
            st.markdown('<div class="title">Total por Tipo de contrataccion</div>',unsafe_allow_html=True)
            dfpie=df['internal_type'].value_counts().reset_index()
            dfpie.columns=['internal_type','count']
            fig4=px.pie(dfpie,values='count',names='internal_type',title='Distribucion de tipos de contratos')
            st.plotly_chart(fig4,use_container_width=True)
else:
    #Graficos de resumen anuales
    data_anual = []
    for year in range(2015, 2026):
        url_anual = f"https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api/get_analysis?local=1&year={year}"
        try:
            resp = requests.get(url_anual)
            if resp.status_code == 200:
                datos = resp.json()
                if isinstance(datos, list):
                    for item in datos:
                        item["year"] = year
                        data_anual.append(item)
        except Exception as e:
            st.warning(f"Error al obtener datos del año {year}: {e}")

    if data_anual:
        df_anual = pd.DataFrame(data_anual)
        
        df_anual['total'] = pd.to_numeric(df_anual['total'], errors='coerce')
        df_anual['total'] = df_anual['total']/1000000
        #agrupamos los datos por anio y por total
        df_grouped=df_anual.groupby('year')['total'].sum().reset_index()
        #creamos el grafio de barras
        fig1=px.bar(df_grouped,x='year',y='total',title="Evolucion del monto total de contratos por año",
                    labels={'year':'Año','total':'Monto Total (Millones de USD)'},
                    color='total',
                    color_continuous_scale='Viridis'
                        )
        #Formatear el eje x para que se muestren todas las etiquetas de los anios
        fig1.update_layout(
        xaxis=dict(
        title="Año",
        tickmode='linear',    # Modo lineal
        dtick=1,             # Intervalo de 1 año
        tickangle=0,         # Ángulo de las etiquetas (0 = horizontal)
        tickfont=dict(size=12)
        ))
        #agregar valor del monto total sobre las barras para una mejor visualizacion
        fig1.update_traces(
        texttemplate='%{y:.1f}M',
        textposition='outside',
        textfont_size=10)
        #mostramos el grafico de barras
        st.plotly_chart(fig1,use_container_width=True)
        #----------------------------------------Comparativa de tipo de contratacion por anio----------------------------------------------
        #preparar los datos
        df_clean=df_anual.copy()
        #eliminar filas con valores nulos
        df_clean = df_clean.dropna(subset=['total', 'internal_type'])
        #agrupar los datos por anio y tipo de contratacion
        df_contra=df_clean.groupby(['year','internal_type'])['total'].sum().reset_index()
        #crear el grafico de lineas
        fig2=px.line(
            df_contra,
            x='year',
            y='total',
            color='internal_type',
            title="Comparativa de tipo de contratacion por año",
            labels={'year':'Año','total':'Monto Total (USD)','internal_type':'Tipo de Contratacion'}
        )
        st.plotly_chart(fig2,use_container_width=True)
    #relacion entre monto total y cantidad de contratos
    #grafico scatter
    #contar los contratos
    df_contratos=df_clean.copy()
    #contar la cantidad de contratos y sumar el monto de cada tipo
    df_contratos=df_contratos.groupby('internal_type')['total'].agg(['count','sum']).reset_index()
    #crear el grafico de dispersion
    fig3=px.scatter(
        df_contratos,
        x='count',
        y='sum',
        color='internal_type',      
        title="Relacion entre monto total y cantidad de contratos",
        
    )
    #agregar etiquetas a los puntos
    fig3.update_traces(textposition='top center')
    #cambiar el nombre a los ejes
    fig3.update_layout(
        xaxis_title="Cantidad de contratos",
        yaxis_title="Monto total (USD)" 
    )
    #mostrar el grafico 
    st.plotly_chart(fig3,use_container_width=True)  
