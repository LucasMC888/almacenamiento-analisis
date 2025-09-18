import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Título y descripción
st.title("Comparación de Tecnologías de Almacenamiento")
st.write("Este dashboard compara HDD, SSD, Cinta y Nube según velocidad, costo, fiabilidad, seguridad y escalabilidad.")

# --- Datos base
data = {
    "Tecnología": ["HDD", "SSD", "Cinta", "Nube"],
    "Velocidad Lectura (MB/s)": [200, 3000, 300, 300],  # valores de referencia
    "Velocidad Escritura (MB/s)": [150, 2500, 150, 200],
    "Costo por GB (USD)": [0.03, 0.1, 0.007, 0.02],
    "Fiabilidad (MTBF horas)": [1200000, 2000000, 2500000, np.nan],
    "Seguridad (1-5)": [3, 4, 2, 5],
    "Escalabilidad (1-5)": [3, 2, 2, 5]
}
df = pd.DataFrame(data)

# --- Mostrar tabla
st.subheader("Tabla comparativa")
st.dataframe(df)

# --- Gráfico de barras (Velocidades)
st.subheader("Velocidades de Lectura y Escritura")
fig, ax = plt.subplots()
x = np.arange(len(df["Tecnología"]))
ax.bar(x - 0.2, df["Velocidad Lectura (MB/s)"], width=0.4, label="Lectura")
ax.bar(x + 0.2, df["Velocidad Escritura (MB/s)"], width=0.4, label="Escritura")
ax.set_xticks(x)
ax.set_xticklabels(df["Tecnología"])
ax.set_ylabel("MB/s")
ax.legend()
st.pyplot(fig)

# --- Gráfico de barras (Costo por GB)
st.subheader("Costo por GB")
fig2, ax2 = plt.subplots()
ax2.bar(df["Tecnología"], df["Costo por GB (USD)"])
ax2.set_ylabel("USD por GB")
st.pyplot(fig2)

# --- Gráfico Radar (Fiabilidad, Seguridad, Escalabilidad)
st.subheader("Comparación cualitativa (Radar)")

# Normalizar fiabilidad en escala 1-5
def mtbf_to_scale(mtbf):
    if pd.isna(mtbf):
        return 3
    elif mtbf < 1_000_000:
        return 2
    elif mtbf < 2_000_000:
        return 3
    elif mtbf < 3_000_000:
        return 4
    else:
        return 5

df["Fiabilidad (1-5)"] = df["Fiabilidad (MTBF horas)"].apply(mtbf_to_scale)

categories = ["Fiabilidad (1-5)", "Seguridad (1-5)", "Escalabilidad (1-5)"]
N = len(categories)

angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles += angles[:1]  # cerrar círculo

fig3, ax3 = plt.subplots(subplot_kw=dict(polar=True))

for i, row in df.iterrows():
    values = row[categories].tolist()
    values += values[:1]
    ax3.plot(angles, values, linewidth=1, linestyle='solid', label=row["Tecnología"])
    ax3.fill(angles, values, alpha=0.1)

ax3.set_xticks(angles[:-1])
ax3.set_xticklabels(categories)
ax3.set_yticks([1,2,3,4,5])
ax3.set_yticklabels(["1","2","3","4","5"])
ax3.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))
st.pyplot(fig3)
