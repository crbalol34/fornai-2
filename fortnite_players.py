import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("Fortnite_players_stats.csv")

st.write("""
# STATS FORTNITE PLAYERS.
## Gráficos usando la base de datos estadística de Fortnite.
""")

#--------------grafico de horas x partidas ganadas --------------#


# 2. Procesar datos: Ordenar por 'Solo minutesPlayed' de mayor a menor
df_sorted = df.sort_values(by='Solo minutesPlayed', ascending=False)

# Widget para controlar cuántos jugadores mostrar (para que el gráfico sea legible)
st.sidebar.header("Configuración del Gráfico")
top_n = st.sidebar.slider("Cantidad de jugadores a mostrar (Top N)", min_value=10, max_value=200, value=50)

# Filtramos los top N jugadores según la selección
df_chart = df_sorted.head(top_n).reset_index(drop=True)

#para que parta de 1 en teoría
df_chart.index = df_chart.index + 1

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
