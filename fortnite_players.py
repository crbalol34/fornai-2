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

# Widget para controlar cuántos jugadores mostrar (para que el gráfico sea legible)
st.sidebar.header("Configuración del Gráfico")
top_n = st.sidebar.slider("Cantidad de jugadores a mostrar (Top N)", min_value=10, max_value=200, value=50)

# Filtramos los top N jugadores según la selección
df_chart = df_sorted.head(top_n).reset_index(drop=True)

# 3. Crear el gráfico con Matplotlib
fig, ax1 = plt.subplots(figsize=(12, 6))

# Eje Y izquierdo: Solo Minutes Played (Línea Azul)
color1 = 'tab:blue'
ax1.set_xlabel('Jugador')
ax1.set_ylabel('Minutos Jugados (Solo)', color=color1, fontsize=12)
ax1.plot(df_chart.index, df_chart['Solo minutesPlayed'], color=color1, marker='o', markersize=4, label='Minutos Jugados')
ax1.tick_params(axis='y', labelcolor=color1)

# Configurar las etiquetas del eje X para mostrar los nombres de los jugadores
ax1.set_xticks(df_chart.index)
ax1.set_xticklabels(df_chart['Player'], rotation=90, fontsize=8)

# Eje Y derecho: Solo Top 1 (Línea Roja)
ax2 = ax1.twinx()  
color2 = 'tab:red'
ax2.set_ylabel('Top 1 (Victorias)', color=color2, fontsize=12)
ax2.plot(df_chart.index, df_chart['Solo top1'], color=color2, linestyle='--', marker='x', markersize=4, label='Top 1')
ax2.tick_params(axis='y', labelcolor=color2)

# Título y ajustes
plt.title(f'Relacion: Minutos Jugados vs Victorias (Top {top_n} jugadores)', fontsize=14)
fig.tight_layout()

# 4. Mostrar en Streamlit
st.pyplot(fig)

# Mostrar tabla de datos opcional
if st.checkbox("Mostrar datos en tabla"):
	st.dataframe(df_chart[['Player', 'Solo minutesPlayed', 'Solo top1']])

#-------------- GRÁFICO 2: GRÁFICO DE TORTA (ESTILO DONA PRO) --------------#
st.write("### 🍕 Distribución de Kills por Modo de Juego")
st.write(f"Total de muertes acumuladas por los **Top {top_n}** jugadores.")

try:
    # 1. Calculamos los datos
    total_solo = df_chart['Solo kills'].sum()
    total_duo = df_chart['Duos kills'].sum()
    total_trio = df_chart['Trios kills'].sum()
    total_squad = df_chart['Squads kills'].sum()

    etiquetas = ['Solo', 'Duos', 'Trios', 'Squads']
    totales = [total_solo, total_duo, total_trio, total_squad]
    # Colores más suaves y profesionales
    colores = ['#F52C05', '#FFF93D', '#05EDF5', '#4AFF08']

    # 2. Configuración de la Figura (Más ancha para que quepa la leyenda)
    fig2, ax_pie = plt.subplots(figsize=(10, 4))

    # 3. Creamos el gráfico SIN LABELS (para que no se amontonen)
    # 'wedges' son los trozos, 'texts' los textos autogenerados
    wedges, texts, autotexts = ax_pie.pie(
        totales, 
        colors=colores, 
        autopct='%1.1f%%', # Formato del porcentaje
        startangle=90, 
        pctdistance=0.85, # Mueve los porcentajes hacia el borde
        textprops=dict(color="black") # Color del texto de porcentaje
    )

    # 4. TRUCO DE LA DONA: Círculo blanco en el centro
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    fig2.gca().add_artist(centre_circle)

    # 5. LEYENDA LATERAL (Aquí está la magia para que no se vea horrible)
    ax_pie.legend(
        wedges, 
        etiquetas,
        title="Modos de Juego",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1) # Esto saca la leyenda fuera del gráfico
    )

    ax_pie.axis('equal')  
    plt.title("Proporción de Kills Totales", fontsize=16)
    plt.tight_layout()

    # Mostrar gráfico
    st.pyplot(fig2)

except KeyError as e:
    st.error(f"⚠️ Error: Falta la columna {e}. Revisa el archivo.")
