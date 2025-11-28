import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carga de datos
df = pd.read_csv("Fortnite_players_stats.csv")

st.write("""
# STATS FORTNITE PLAYERS.
## Gráficos usando la base de datos estadística de Fortnite.
""")

#-------------- CONFIGURACIÓN --------------#
# 2. Procesar datos: Ordenar por 'Solo minutesPlayed' de mayor a menor
df_sorted = df.sort_values(by='Solo minutesPlayed', ascending=False)

# Widget para controlar cuántos jugadores mostrar
st.sidebar.header("Configuración del Gráfico")
top_n = st.sidebar.slider("Cantidad de jugadores a mostrar (Top N)", min_value=10, max_value=200, value=50)

# Filtramos los top N jugadores según la selección
df_chart = df_sorted.head(top_n).reset_index(drop=True)

# Ajuste para que el ranking empiece en 1
df_chart.index = df_chart.index + 1

#-------------- GRÁFICO 1: HORAS X PARTIDAS GANADAS (LINEAL) --------------#
st.write("### ⏱️ Relación: Minutos Jugados vs Victorias")

# Crear el gráfico con Matplotlib
fig, ax1 = plt.subplots(figsize=(4, 4))

# Eje Y izquierdo: Solo Minutes Played (Línea Azul)
color1 = 'tab:blue'
ax1.set_xlabel('Ranking del Jugador')
ax1.set_ylabel('Minutos Jugados (Solo)', color=color1, fontsize=12)
ax1.plot(df_chart.index, df_chart['Solo minutesPlayed'], color=color1, marker='o', markersize=4, label='Minutos Jugados')
ax1.tick_params(axis='y', labelcolor=color1)

# Configurar las etiquetas del eje X
ax1.set_xticks(df_chart.index)
ax1.set_xticklabels(df_chart['Player'], rotation=90, fontsize=8)

# Eje Y derecho: Solo Top 1 (Línea Roja)
ax2 = ax1.twinx()  
color2 = 'tab:red'
ax2.set_ylabel('Top 1 (Victorias)', color=color2, fontsize=12)
ax2.plot(df_chart.index, df_chart['Solo top1'], color=color2, linestyle='--', marker='x', markersize=4, label='Top 1')
ax2.tick_params(axis='y', labelcolor=color2)

plt.title(f'Top {top_n} Jugadores: Tiempo vs Victorias', fontsize=14)
fig.tight_layout()

# Mostrar gráfico 1
st.pyplot(fig)

st.write("---") # Línea separadora

#-------------- GRÁFICO 2: GRÁFICO DE TORTA (KILLS) --------------#
st.write("### 🍕 Distribución de Kills por Modo de Juego")
st.write(f"Total de muertes acumuladas por los **Top {top_n}** jugadores.")

try:
    # 1. Calculamos la suma total de kills (Ahora sí con TRIOS)
    total_solo = df_chart['Solo kills'].sum()
    total_duo = df_chart['Duos kills'].sum()   # Ojo: En tu archivo es 'Duos', no 'Duo'
    total_trio = df_chart['Trios kills'].sum() # Ojo: En tu archivo es 'Trios', no 'Trio'
    total_squad = df_chart['Squads kills'].sum() # Ojo: En tu archivo es 'Squads'

    # 2. Preparamos los datos para el gráfico
    etiquetas = ['Solo', 'Duos', 'Trios', 'Squads']
    totales = [total_solo, total_duo, total_trio, total_squad]
    colores = ['#ff9999','#66b3ff','#99ff99','#ffcc99'] # Rojo, Azul, Verde, Naranja

    # 3. Creamos el gráfico de torta
    fig2, ax_pie = plt.subplots(figsize=(8, 8))
    
    # autopct='%1.1f%%' muestra el porcentaje con 1 decimal
    ax_pie.pie(totales, labels=etiquetas, colors=colores, autopct='%1.1f%%', startangle=140)
    
    ax_pie.axis('equal')  # Para que salga redondo y no ovalado
    plt.title("Proporción de Kills Totales", fontsize=14)

    # Mostrar gráfico 2
    st.pyplot(fig2)

except KeyError as e:
    st.error(f"⚠️ Error: No se encontró la columna {e} en el archivo CSV. Revisa los nombres exactos.")

#-------------- TABLA DE DATOS --------------#
st.write("---")
if st.checkbox("Mostrar datos en tabla"):
    st.dataframe(df_chart)
