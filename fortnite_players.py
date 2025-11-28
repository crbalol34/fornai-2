import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Fortnite Analytics",
    page_icon="🎮",
    layout="wide"
)

# --- CARGA DE DATOS ---
try:
    df = pd.read_csv("Fortnite_players_stats.csv")
except FileNotFoundError:
    st.error("⚠️ Error: No se encontró el archivo 'Fortnite_players_stats.csv'.")
    st.stop()

# --- TÍTULO ---
st.write("""
# 🎮 Dashboard de Estadísticas de Fortnite
## Análisis de rendimiento (Versión Matplotlib)
""")
st.write("---")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuración")
    top_n = st.slider("🏆 Cantidad de jugadores (Top N):", 10, 100, 20)
    mostrar_raw = st.checkbox("Mostrar tabla completa", value=False)
    st.info("Modo sin librería Plotly activado.")

# --- PROCESAMIENTO DE DATOS (IMPORTANTE: Esto define df_sorted) ---
# 1. Ordenar y filtrar
df_sorted = df.sort_values(by='Solo minutesPlayed', ascending=False).head(top_n).reset_index(drop=True)

# 2. Ajustar índice (Empieza en 1)
df_sorted.index = df_sorted.index + 1

# 3. Crear columna nueva (KPI de eficiencia)
df_sorted['WinsPerHour'] = df_sorted['Solo top1'] / (df_sorted['Solo minutesPlayed'] / 60)

# --- KPIs ---
col1, col2, col3 = st.columns(3)
promedio_mins = df_sorted['Solo minutesPlayed'].mean()
total_wins = df_sorted['Solo top1'].sum()
total_kills_global = df_sorted['Solo kills'].sum()

col1.metric("⏱️ Promedio Minutos", f"{promedio_mins:,.0f} min")
col2.metric("🏆 Total Victorias Solo", f"{total_wins}")
col3.metric("💀 Total Kills Solo", f"{total_kills_global}")

st.write("---")

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Tiempo vs Victorias", 
    "🚀 Eficiencia", 
    "🍕 Distribución de Kills", 
    "📋 Datos"
])

# --- TAB 1: GRÁFICO DUAL (Matplotlib) ---
with tab1:
    st.subheader("Relación: Tiempo invertido vs Victorias")
    plt.style.use('ggplot') 
    
    fig, ax1 = plt.subplots(figsize=(14, 7))

    color1 = 'tab:blue'
    ax1.set_xlabel('Ranking del Jugador', fontsize=12)
    ax1.set_ylabel('Minutos Jugados', color=color1, fontsize=14)
    ax1.bar(df_sorted.index, df_sorted['Solo minutesPlayed'], color=color1, alpha=0.6, label='Minutos')
    ax1.tick_params(axis='y', labelcolor=color1)
    
    ax1.set_xticks(df_sorted.index)
    ax1.set_xticklabels(df_sorted['Player'], rotation=45, ha="right", fontsize=9)

    ax2 = ax1.twinx()  
    color2 = 'tab:red'
    ax2.set_ylabel('Victorias (Top 1)', color=color2, fontsize=14)
    ax2.plot(df_sorted.index, df_sorted['Solo top1'], color=color2, linewidth=3, marker='o', label='Victorias')
    ax2.tick_params(axis='y', labelcolor=color2)

    plt.title(f"Comparativa Top {top_n} Jugadores", fontsize=16)
    fig.tight_layout()
    st.pyplot(fig)

# --- TAB 2: SCATTER (Matplotlib) ---
with tab2:
    st.subheader("Análisis de Eficiencia")
    
    fig2, ax = plt.subplots(figsize=(10, 6))
    
    # Creamos el scatter plot
    scatter = ax.scatter(
        df_sorted["Solo minutesPlayed"], 
        df_sorted["Solo top1"], 
        s=df_sorted["WinsPerHour"] * 200, 
        c=df_sorted["WinsPerHour"], 
        cmap="viridis", 
        alpha=0.7,
        edgecolors="black"
    )
    
    ax.set_xlabel("Minutos Jugados")
    ax.set_ylabel("Victorias (Top 1)")
    ax.set_title("Eficiencia: Minutos vs Victorias (Tamaño = Eficiencia)")
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Victorias por Hora')
    
    st.pyplot(fig2)

# --- TAB 3: GRÁFICO DE TORTA (Matplotlib) ---
with tab3:
    st.subheader("Distribución de Kills por Modo de Juego")
    
    try:
        # 1. Calcular totales
        total_solo = df_sorted['Solo kills'].sum()
        total_duo = df_sorted['Duo kills'].sum()
        total_trio = df_sorted['Trio kills'].sum()
        total_squad = df_sorted['Squad kills'].sum()
        
        # 2. Preparar datos
        labels = ['Solo', 'Duo', 'Trio', 'Squad']
        sizes = [total_solo, total_duo, total_trio, total_squad]
        
        # Colores personalizados
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
        
        # 3. Crear gráfico
        fig3, ax3 = plt.subplots(figsize=(8, 8))
        
        ax3.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                startangle=90, pctdistance=0.85, explode=(0.05, 0, 0, 0))
        
        # Círculo blanco para efecto "Dona"
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig3.gca().add_artist(centre_circle)
        
        ax3.axis('equal') 
        plt.title(f"Total de Kills (Top {top_n} jugadores)", fontsize=14)
        
        st.pyplot(fig3)
        
    except KeyError:
         st.error("⚠️ Error: Faltan columnas de Kills en el CSV.")

# --- TAB 4: DATOS ---
with tab4:
    st.subheader("Tabla de Datos Detallada")
    st.dataframe(df_sorted)

if mostrar_raw:
    st.write("---")
    st.write("### Dataset Completo")
    st.write(df)
