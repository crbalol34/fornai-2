import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. CONFIGURACIÓN DE PÁGINA (Importante para que quepan las columnas)
st.set_page_config(layout="wide")

# Carga de datos
try:
    df = pd.read_csv("Fortnite_players_stats.csv")
except FileNotFoundError:
    st.error("⚠️ Falta el archivo 'Fortnite_players_stats.csv'")
    st.stop()

st.write("""
# STATS FORTNITE PLAYERS
## Gráficos usando la base de datos estadística de Fortnite.
""")

#-------------- CONFIGURACIÓN (SIDEBAR IZQUIERDA) --------------#
# 2. Procesar datos: Ordenar por 'Solo minutesPlayed' de mayor a menor
df_sorted = df.sort_values(by='Solo minutesPlayed', ascending=False)

# Widget para controlar cuántos jugadores mostrar
st.sidebar.header("Configuración del Gráfico")
top_n = st.sidebar.slider("Cantidad de jugadores a mostrar (Top N)", min_value=10, max_value=200, value=50)

# Filtramos los top N jugadores según la selección
df_chart = df_sorted.head(top_n).reset_index(drop=True)

# Ajuste ranking (para que empiece en 1)
df_chart.index = df_chart.index + 1

st.write("---")

# ==============================================================================
# AQUÍ ES DONDE DEFINIMOS LAS COLUMNAS: IZQUIERDA (GRANDE) Y DERECHA (CHICA)
# ==============================================================================
col_main, col_lateral = st.columns([3, 1])


# ------------------------------------------------------------------------------
# PARTE 1: TU GRÁFICO ORIGINAL (LO MOVEMOS A LA COLUMNA PRINCIPAL)
# ------------------------------------------------------------------------------
with col_main:
    st.write("### ⏱️ Relación: Minutos Jugados vs Victorias")

    # 3. Crear el gráfico con Matplotlib
    fig, ax1 = plt.subplots(figsize=(10, 6)) # Ajusté un poco el tamaño

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

    # Título y ajustes
    plt.title(f'Top {top_n} jugadores', fontsize=14)
    plt.tight_layout()

    # 4. Mostrar en Streamlit
    st.pyplot(fig)


# ------------------------------------------------------------------------------
# PARTE 2: EL CÓDIGO NUEVO (LO MOVEMOS A LA COLUMNA LATERAL)
# ------------------------------------------------------------------------------
with col_lateral:
    st.write("### 🍕 Kills Totales")
    st.caption("Distribución por modo")

    try:
        # Sumamos las kills (Incluyendo Trios si existe)
        total_solo = df_chart['Solo kills'].sum()
        total_duo = df_chart['Duos kills'].sum()
        total_squad = df_chart['Squads kills'].sum()
        
        # Intentamos buscar trios para evitar errores si no existe la columna
        if 'Trios kills' in df_chart.columns:
            total_trio = df_chart['Trios kills'].sum()
            etiquetas = ['Solo', 'Duos', 'Trios', 'Squads']
            totales = [total_solo, total_duo, total_trio, total_squad]
            colores = ['#F52C05', '#FFF93D', '#05EDF5', '#4AFF08'] # Tus colores personalizados
        else:
            etiquetas = ['Solo', 'Duos', 'Squads']
            totales = [total_solo, total_duo, total_squad]
            colores = ['#F52C05', '#FFF93D', '#4AFF08']

        # Creamos gráfico vertical (más alto que ancho)
        fig2, ax_pie = plt.subplots(figsize=(4, 5))
        
        # Fondo transparente
        fig2.patch.set_alpha(0)

        # Gráfico estilo Dona
        wedges, texts, autotexts = ax_pie.pie(
            totales, 
            colors=colores, 
            autopct='%1.0f%%', 
            startangle=90, 
            pctdistance=0.85,
            textprops=dict(color="black", fontsize=9, weight="bold")
        )

        centre_circle = plt.Circle((0,0), 0.70, fc='white')
        fig2.gca().add_artist(centre_circle)

        # Leyenda abajo
        ax_pie.legend(wedges, etiquetas, loc="upper center", bbox_to_anchor=(0.5, 0), fontsize=9)
        
        ax_pie.axis('equal')
        plt.tight_layout()
        
        # Mostramos el gráfico
        st.pyplot(fig2, use_container_width=True)

    except KeyError as e:
        st.error(f"Error datos: {e}")

#-------------- TABLA FINAL (FUERA DE LAS COLUMNAS) --------------#
st.write("---")
if st.checkbox("Mostrar datos en tabla"):
    st.dataframe(df_chart[['Player', 'Solo minutesPlayed', 'Solo top1', 'Solo kills']])
except KeyError as e:
    st.error(f"⚠️ Error: Falta la columna {e}. Revisa el archivo.")
