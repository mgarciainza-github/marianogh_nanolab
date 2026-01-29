'''
vdata1A25 = VG
idata1B25 = ID


Algoritmo:
1- cargar archivo a df
2- tomar una curva
3- ajustar y tomar pendiente
4- generalizar para varias curvas
5- automatizar: hacer todo desde el mismo df
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


ruta_base = './'
nombre_archivo_entrada = 'iv_measurements_subdataset.csv' 

df = pd.read_csv(ruta_base + nombre_archivo_entrada)

df.rename(columns={'idata1B25':'ID','vdata1A25':'VG', 'wafer':'w','device':'dev'}, inplace=True)

df['lnID']= np.log(np.abs(df['ID']))
df['-VG'] = (-1)*df['VG'] 

df.to_csv( ruta_base + nombre_archivo_entrada + 'out.csv')

df['curve_num'] = 0

df_w19 = df.loc[df['w'] == 19]
df_w21 = df.loc[df['w'] == 21]
df_w21 = df_w21.reset_index(drop=True)

# Cantidad de curvas para cada dispo:

curve_num = 0
for i in range(len(df_w21.index)-1):
    df_w21.at[i,'curve_num'] = curve_num
    delta_t = df_w21.at[i+1,'t_1'] - df_w21.at[i,'t_1']
    if delta_t != 0: curve_num += 1
df_w21.at[i+1,'curve_num'] = curve_num

curve_num = 0
for i in range(len(df_w19.index)-1):
    df_w19.at[i,'curve_num'] = curve_num
    delta_t = df_w19.at[i+1,'t_1'] - df_w19.at[i,'t_1']
    if delta_t != 0: curve_num += 1
df_w19.at[i+1,'curve_num'] = curve_num

# Graficos curvas:

plt.subplots()
#print(df_w19.at[df_w19.index[-1],'curve_num'])
for i in range(df_w19.at[df_w19.index[-1],'curve_num']):
    x_data = df_w19.loc[df_w19['curve_num'] == i, ['-VG']]
    y_data = df_w19.loc[df_w19['curve_num'] == i, ['lnID']]
    plt.plot(x_data,y_data,'.-',label=i)
plt.legend(fontsize='xx-small', ncol=3)
plt.xlabel('- VG(V)')
plt.ylabel('ln(ID)')
plt.title('w_19')
plt.show(block=False)

plt.subplots()
for i in range(curve_num):
    x_data = df_w21.loc[df_w21['curve_num'] == i, ['-VG']]
    y_data = df_w21.loc[df_w21['curve_num'] == i, ['lnID']]
    plt.plot(x_data,y_data,'.-', label=i)
plt.legend(fontsize='xx-small', ncol=3)
plt.xlabel('- VG(V)')
plt.ylabel('ln(ID)')
plt.title('w_21')
plt.show(block=False)


# grafico dlnID/dVG:
'''
VG =   df_w21.loc[df_w21['curve_num'] == 0, ['VG']].to_numpy()
lnID = df_w21.loc[df_w21['curve_num'] == 0, ['lnID']].to_numpy()
print(VG)
print('-')
print(VG[0])
dVG=[]
dlnID=[]
dlnID_over_dVG_list =[]
for i in range(len(VG)-1):
    dVG.append(VG[i+1] - VG [i])
    dlnID.append(lnID[i+1] - lnID[i])
    dlnID_over_dVG_list.append( dlnID[i] / dVG[i])
dlnID_over_dVG_list.append( dlnID_over_dVG_list[-1])
dlnID_over_dVG = dlnID_over_dVG_list[:][0]
print(dlnID_over_dVG)
#print(VG)
plt.subplots()
plt.plot(VG,dlnID_over_dVG_list,'*-')
plt.title('dlnID/dVG w21 curve num 0')
plt.show(block=False)
'''


# Ajustes:

from scipy.optimize import curve_fit

def func_lin(x,a,b):
    return a*x+b

plt.subplots()
slope19=[]
for i in range(curve_num):

    df_data_to_adjust=df_w19.loc[(df_w19['-VG'] < 0.11) & ((df_w19['-VG'] > -0.01)) & (df_w19['curve_num'] == i), ['-VG', 'lnID']]

    # Borrar df:
    #df_data_to_adjust = df_data_to_adjust.iloc[0:0]

    popt, pcov = curve_fit(func_lin, df_data_to_adjust['-VG'], df_data_to_adjust['lnID'])
    slope19.append(popt[0])

    x_data = df_w19.loc[df_w19['curve_num'] == i, ['-VG']]
    y_data = df_w19.loc[df_w19['curve_num'] == i, ['lnID']]
    plt.plot(x_data,y_data,'.', label=i)
    plt.plot(df_data_to_adjust['-VG'],func_lin(df_data_to_adjust['-VG'],*popt),'--')
plt.legend(fontsize='xx-small', ncol=3)
plt.title('w19 and linear fit')
plt.xlabel('- VG')
plt.ylabel('ln(ID)')
plt.show(block=False)



plt.subplots()
slope21=[]
for i in range(curve_num):

    df_data_to_adjust=df_w21.loc[(df_w21['-VG'] < 0.11) & ((df_w21['-VG'] > -0.01)) & (df_w21['curve_num'] == i), ['-VG', 'lnID']]

    # Borrar df:
    #df_data_to_adjust = df_data_to_adjust.iloc[0:0]

    popt, pcov = curve_fit(func_lin, df_data_to_adjust['-VG'], df_data_to_adjust['lnID'])
    slope21.append(popt[0])

    x_data = df_w21.loc[df_w21['curve_num'] == i, ['-VG']]
    y_data = df_w21.loc[df_w21['curve_num'] == i, ['lnID']]
    plt.plot(x_data,y_data,'.')
    plt.plot(df_data_to_adjust['-VG'],func_lin(df_data_to_adjust['-VG'],*popt),'--', label=i)


plt.legend(fontsize='xx-small', ncol=3)
plt.title('w21 and linear fit')
plt.xlabel('- VG')
plt.ylabel('ln(ID)')
plt.show(block=False)

plt.subplots()
plt.plot(slope19,'s--', label='w19')
plt.plot(slope21,'s--', label='w21')
plt.legend()
plt.title('Subthreshold slope evolution')
plt.xlabel('Stress cycle number')
plt.ylabel('dln(ID)/dVG')
plt.show(block=False)

input()