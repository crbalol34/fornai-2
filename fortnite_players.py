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
fig, ax1 = plt.subplots(figsize=(12, 6))

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
    colores = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99']

    # 2. Configuración de la Figura (Más ancha para que quepa la leyenda)
    fig2, ax_pie = plt.subplots(figsize=(10, 6))

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
