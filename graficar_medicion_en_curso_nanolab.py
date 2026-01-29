import numpy as np
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt

ruta_archivo_fecha="/home/mariano/docs/Nanolab/medicion_en_curso.txt" 

try:
    with open(ruta_archivo_fecha) as f:
        fecha = f.readline().strip()
except:
    print("Error")
    fecha = ""

carpeta_medicion = "/home/mariano/docs/Nanolab/mediciones/" + fecha

print(carpeta_medicion)

archivos_csv = glob.glob(os.path.join(carpeta_medicion, '*.csv'))

'''
print("------------")
print(archivos_csv)
print("------------")
print(max(archivos_csv))
'''

#Hay que seleccionar el último archivo:
#archivo_csv = archivos_csv[0]
archivo_csv = max(archivos_csv)

nombre_archivo = os.path.basename(archivo_csv)

print("------------")
print('Nombre del archivo: ',nombre_archivo)

df_medicion = pd.read_csv(archivo_csv)

print("------------")
print(df_medicion.head())

# Obtener nombres de columnas por posición
nombre_col1 = df_medicion.columns[0]  # Primera columna (eje X)
nombre_col2 = df_medicion.columns[1]  # Segunda columna
nombre_col3 = df_medicion.columns[2]  # Tercera columna

# Crear el gráfico
plt.figure(figsize=(10, 6))

# Graficar columna 2 vs columna 1
plt.plot(df_medicion[nombre_col1], df_medicion[nombre_col2], label=nombre_col2, marker='o', linestyle='-', linewidth=1)

# Graficar columna 3 vs columna 1
plt.plot(df_medicion[nombre_col1], df_medicion[nombre_col3], label=nombre_col3, marker='s', linestyle='--', linewidth=1)

# Cometar para auto escala:
y_min=-2.6e-6
y_max=-2.0e-6
plt.ylim(y_min, y_max)

# Personalizar el gráfico
plt.xlabel(nombre_col1 + ' (s)', fontsize=12)
plt.ylabel('Current (A)', fontsize=12)
plt.title(f'{nombre_col2} y {nombre_col3} vs {nombre_col1}', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Mostrar el gráfico
plt.show(block=False)

# Grafico en escala log:
plt.figure(figsize=(10, 6))

# Graficar columna 2 vs columna 1
plt.loglog(df_medicion[nombre_col1], abs(df_medicion[nombre_col2]), label=nombre_col2, marker='o', linestyle='-', linewidth=1)


# Graficar columna 3 vs columna 1
plt.loglog(df_medicion[nombre_col1], abs(df_medicion[nombre_col3]), label=nombre_col3, marker='s', linestyle='--', linewidth=1)

plt.grid(True, which="major", linestyle='-', linewidth=0.5)
plt.grid(True, which="minor", linestyle=':', linewidth=0.3, alpha=0.5)

# Personalizar el gráfico
plt.xlabel(nombre_col1 + ' (s)', fontsize=12)
plt.ylabel('Current (A)', fontsize=12)
plt.title(f'{nombre_col2} y {nombre_col3} vs {nombre_col1}', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Mostrar el gráfico
plt.show()