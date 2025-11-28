import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Fortnite Analytics",
    page_icon="🎮",
    layout="wide"
)

# Estilo global para los gráficos (Más limpio y profesional)
plt.style.use('ggplot')

# Carga de datos
try:
    df = pd.read_csv("Fortnite_players_stats.csv")
except FileNotFoundError:
    st.error("⚠️ Falta el archivo 'Fortnite_players_stats.csv'")
    st.stop()

st.write("""
# 🎮 STATS FORTNITE PLAYERS
## Gráficos usando la base de datos estadística de Fortnite.
""")

#-------------- CONFIGURACIÓN (SIDEBAR IZQUIERDA) --------------#
df_sorted = df.sort_values(by='Solo minutesPlayed', ascending=False)

st.sidebar.header("Configuración del Gráfico")
top_n = st.sidebar.slider("Cantidad de jugadores a mostrar (Top N)", min_value=10, max_value=200, value=50)

# Filtrado y ranking
df_chart = df_sorted.head(top_n).reset_index(drop=True)
df_chart.index = df_chart.index + 1

st.write("---")

# ==============================================================================
# DEFINICIÓN DE COLUMNAS
# ==============================================================================
col_main, col_lateral = st.columns([3, 1])

# ------------------------------------------------------------------------------
# PARTE 1: GRÁFICO PRINCIPAL (MEJORADO)
# ------------------------------------------------------------------------------
with col_main:
    st.write("### ⏱️ Relación: Minutos Jugados vs Victorias")

    # Creamos figura
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Fondo transparente para integración
    fig.patch.set_alpha(0)
    ax1.patch.set_alpha(0)

    # --- Eje Izquierdo: Minutos (Azul) ---
    color1 = '#1f77b4' # Azul profesional
    ax1.set_xlabel('Ranking del Jugador', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Minutos Jugados (Solo)', color=color1, fontsize=11, fontweight='bold')
    
    # Línea con relleno (Fill Between) para mejor efecto visual
    ax1.plot(df_chart.index, df_chart['Solo minutesPlayed'], color=color1, marker='o', markersize=4, linewidth=2, label='Minutos')
    ax1.fill_between(df_chart.index, df_chart['Solo minutesPlayed'], color=color1, alpha=0.1) # Relleno suave
    
    ax1.tick_params(axis='y', labelcolor=color1)
    
    # Etiquetas eje X rotadas
    ax1.set_xticks(df_chart.index)
    ax1.set_xticklabels(df_chart['Player'], rotation=90, fontsize=8)
    
    # Grid suave
    ax1.grid(True, linestyle='--', alpha=0.5)

    # --- Eje Derecho: Victorias (Rojo) ---
    ax2 = ax1.twinx()  
    color2 = '#d62728' # Rojo profesional
    ax2.set_ylabel('Top 1 (Victorias)', color=color2, fontsize=11, fontweight='bold')
    ax2.plot(df_chart.index, df_chart['Solo top1'], color=color2, linestyle='--', marker='x', markersize=5, linewidth=2, label='Top 1')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.grid(False) # Quitamos grid del segundo eje para no ensuciar

    plt.title(f'Top {top_n} jugadores: Rendimiento', fontsize=14)
    plt.tight_layout()

    st.pyplot(fig)


# ------------------------------------------------------------------------------
# PARTE 2: GRÁFICO LATERAL (DONA MEJORADA)
# ------------------------------------------------------------------------------
with col_lateral:
    st.write("### 🍕 Kills Totales")
    st.caption("Distribución por modo")

    try:
        # Sumamos las kills
        total_solo = df_chart['Solo kills'].sum()
        total_duo = df_chart['Duos kills'].sum()
        total_squad = df_chart['Squads kills'].sum()
        
        # Lógica para Trios
        if 'Trios kills' in df_chart.columns:
            total_trio = df_chart['Trios kills'].sum()
            etiquetas = ['Solo', 'Duos', 'Trios', 'Squads']
            totales = [total_solo, total_duo, total_trio, total_squad]
            # Tus colores neón (ajustados un poco para contraste)
            colores = ['#FF4B4B', '#1C83E1', '#00D4BB', '#FFBB00'] 
        else:
            etiquetas = ['Solo', 'Duos', 'Squads']
            totales = [total_solo, total_duo, total_squad]
            colores = ['#FF4B4B', '#1C83E1', '#FFBB00']

        # Figura vertical para columna estrecha
        fig2, ax_pie = plt.subplots(figsize=(5, 6))
        
        # Fondo TOTALMENTE transparente
        fig2.patch.set_alpha(0)
        ax_pie.patch.set_alpha(0)

        # Gráfico Donut
        wedges, texts, autotexts = ax_pie.pie(
            totales, 
            colors=colores, 
            autopct='%1.0f%%', 
            startangle=90, 
            pctdistance=0.80, # Porcentajes más al borde
            wedgeprops=dict(width=0.4, edgecolor='white'), # Anillo más fino y bordes blancos
            textprops=dict(color="black", fontsize=10, weight="bold")
        )

        # Leyenda DEBAJO (clave para columnas estrechas)
        ax_pie.legend(
            wedges, 
            etiquetas, 
            loc="upper center", 
            bbox_to_anchor=(0.5, 0.05), # Posición inferior
            ncol=2, # En 2 columnas para ahorrar espacio vertical
            frameon=False, # Sin recuadro
            fontsize=9
        )
        
        ax_pie.axis('equal')
        plt.tight_layout()
        
        st.pyplot(fig2, use_container_width=True)

    except KeyError as e:
        st.error(f"Error datos: {e}")

#-------------- TABLA FINAL --------------#
st.write("---")
if st.checkbox("Mostrar datos en tabla"):
    st.dataframe(df_chart[['Player', 'Solo minutesPlayed', 'Solo top1', 'Solo kills']])
