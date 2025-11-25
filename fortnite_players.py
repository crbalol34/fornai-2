import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Fortnite_players_stats.csv")

st.write("""
# STATS FORTNITE PLAYERS.
## Gráficos usando la base de datos estadística de Fortnite.
""")

solos_top10 = df[['Player','Solo score']].sort_values('Solo score',ascending=False).head(20)

#df1 = df[['Solo score']]
#df1 = df1.sort_values(by='Solo score', ascending=False).head(10)


fig, ax = plt.subplots(figsize=(12, 6)) 


ax.bar(solos_top10.index.astype(str), solos_top10['Solo score'], color='#3498db') 


ax.set_title('Top 10 Solo Scores')
ax.set_xlabel('Índice / Jugador')
ax.set_ylabel('Score')
plt.xticks(rotation=90, fontsize=8) # Rotamos etiquetas del eje X si son nombres largos


#--------------------- nuevo codigo ------------


# 2. Configurar el fondo y la rejilla (Estilo Plotly)
ax.set_facecolor('#E5ECF6')            # Fondo gris azulado interno
fig.patch.set_facecolor('white')       # Fondo blanco externo
ax.grid(axis='y', color='white', linewidth=1) # Rejilla blanca
ax.set_axisbelow(True)                 # Rejilla detrás de las barras

# 3. Quitar los bordes negros (Spines)
for spine in ax.spines.values():
    spine.set_visible(False)


max_val = solos_top10['Solo score'].max()
# Definimos el paso: cada 1 millón (1,000,000)
step = 1_000_000


yticks_values = range(0, int(max_val) + step, step)


yticks_labels = [f'{int(y/1_000_000)}M' if y > 0 else '0' for y in yticks_values]

# Aplicamos las marcas y las etiquetas manualmente
ax.set_yticks(yticks_values)
ax.set_yticklabels(yticks_labels)

# 4. Ajustes del Eje X
plt.xticks(rotation=-90, fontsize=9)
plt.xlim(-0.6, len(solos_top10) - 0.4)

# --- Mostrar en Streamlit ---
plt.tight_layout()
st.pyplot(fig)

# Using object notation
with st.expander("Ver tabla filtrada"):
    st.dataframe(df_filtrado[["Jugador", "Puntaje solitario", "", "Age", "Pclass", "Fare", "Survived"]])
#add_selectbox = st.sidebar.selectbox(
 #   "¿Qué te gustaría saber?",
  #  ("Player", "Top  1 solitario", "Puntaje solitario", )
#)


