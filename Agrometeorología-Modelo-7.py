#!/usr/bin/python3
from tkinter import ttk, messagebox
import tkinter as tk
import pandas as pd
import os
from datetime import datetime, timedelta

def text(texto):
    return texto.get('1.0', 'end')[:-1]


def interruption(mensaje):
    return messagebox.showinfo(message=mensaje, title="Resultado")

def guardar(df_salida,cultivo, estacion):
    ext = '.xlsx'
    if cultivo != '\n':
        nombre_fichero = f"M7_[{estacion}]_[{cultivo}]_[{datetime.strftime(datetime.now(),'%Y-%m-%d]_[%H-%M-%S')}]{ext}"
    else:
        nombre_fichero = f"M7_[{estacion}]_[{datetime.strftime(datetime.now(),'%Y-%m-%d_%H-%M-%S')}]{ext}"
    df_salida.to_excel(nombre_fichero)

def ejecution(root, frame1, self, text1, text2, text21, text3,text4):
    text1 = text(text1)
    text2 = text(text2)
    text21 = text(text21)
    text3 = text(text3)
    text4 = text(text4)
    direccion = os.path.join(text1,text2)
    cond = True
    while cond:
        if os.path.exists(text1):
            if os.path.isdir(text1):
                if os.path.isfile(direccion):
                    if text2.endswith('.csv'):
                        if text21.isdigit():
                            cond = False
                        else:
                            return interruption('Ingrese el número de la estación')
                    else:
                        return interruption('El fichero no es un .csv')
                else:
                    if os.path.exists(f'{direccion}.csv'):
                        direccion += '.csv'
                        if text21.isdigit():
                            cond = False
                        else:
                            return interruption('Ingrese el número de la estación')
                    else:
                        if text2 == '':
                            return interruption('Inserte un texto')
                        else:
                            return interruption('El fichero no es un .csv')
            else:
                if text1.endswith('.csv'):
                    direccion = text1
                    if text21.isdigit():
                        cond = False
                    else:
                        return interruption('Ingrese el número de la estación')
        else:
            if text1 == '':
                return interruption('Inserte un texto')
            else:
                return interruption('Ruta no válida')
        
    #---------------------------
    
    lista = text3[:-1].replace('\t','-').split('\n')
    dcRr = []
    sRr = []
    sT = []
    sHr = []
    Fecha_inicial = []
    Fecha_final = []
    Cantidad_de_dias = []
    df1 = pd.DataFrame()
    contador = -1
    estacion = int(text21)
    df = pd.read_csv(direccion)
    df = df.loc[:,'Estacion':'Granizo']
    df['Fecha'] = df['Fecha'].apply(lambda x:datetime.strptime(x,'%Y-%m-%d'))
    for ii in range(len(lista)):
        if ii < len(lista)-1:
            F1 = datetime.strptime(lista[ii], '%d-%m-%Y')
            df2 = pd.DataFrame()
            contador += 1
            d = lista[ii+1]
            F2 = datetime.strptime(d, '%d-%m-%Y') - timedelta(days = 1)
            d = int((F2 - F1).days)
            Cantidad_de_dias.append(d)
            F2 = F1 + timedelta(days = d)
            sub_df = df[(df['Estacion'] == estacion) &(df['Fecha'] >= F1) & (df['Fecha'] <= F2)]
            df2['F1'] = pd.Series(F1)
            df2['F2'] = pd.Series(F2)
            df2['No. de días'] = pd.Series(d) + 1
            try:
                dcRr = sub_df['r 24h'].count() - sub_df['r 24h'].value_counts()[0]
            except KeyError:
                dcRr = sub_df['r 24h'].count()
            df2['Días con precipitación'] = pd.Series(dcRr)
            
            for ii in sub_df.columns:
                if sub_df[ii].dtype == 'float64' or sub_df[ii].dtype == 'int64':
                    df2['s' + ii] = sub_df[ii].sum()
                    
                    
            F1 = F2 + timedelta(days = 1)

            df1 = df1.append(df2)
    df_salida = df1.loc[:,['F1', 'F2', 'No. de días', 'Días con precipitación', 'sr 24h', 'sT med', 'sDef med', 'sHr med']]
    df_salida['F1'] = df_salida['F1'].apply(lambda x:x.date())
    df_salida['F2'] = df_salida['F2'].apply(lambda x:x.date())
    df_salida['Estación'] = int(text21)
    df_salida.set_index('Estación', inplace=True)
    guardar(df_salida,text4, text21)
    messagebox.showinfo(message="Ejecución exitosa", title="Resultado")


class NewprojectApp:
    def __init__(self, master=None):
        # build ui
        frame1 = ttk.Frame(master)
        frame1.configure(height=200, width=200)
        label1 = ttk.Label(frame1)
        label1.configure(takefocus=False, text="Modelo 7")
        label1.pack(side="top")
        label2 = ttk.Label(frame1)
        label2.configure(text="Inserte la ruta del fichero csv")
        label2.pack(side="top")
        text1 = tk.Text(frame1)
        text1.configure(height=2, width=50)
        text1.pack(side="top")
        label3 = ttk.Label(frame1)
        label3.configure(text="Inserte el nombre csv de Datos Diarios")
        label3.pack(side="top")
        text2 = tk.Text(frame1)
        text2.configure(height=1, width=50)
        text2.pack(side="top")
        label31 = ttk.Label(frame1)
        label31.configure(text="Inserte el número de la estación (5 dígitos)")
        label31.pack(side="top")
        text21 = tk.Text(frame1)
        text21.configure(height=1, width=8)
        text21.pack(side="top")
        label4 = ttk.Label(frame1)
        label4.configure(text="Inserte las fechas")
        label4.pack(side="top")
        text3 = tk.Text(frame1)
        text3.configure(height=10, width=50)
        text3.pack(side="top")
        self.Label5 = ttk.Label(frame1)
        self.Label5.configure(text="Nombre del cultivo")
        self.Label5.pack(side="top")
        text4 = tk.Text(frame1)
        text4.configure(height=1, width=50)
        text4.pack(side="top")
        button1 = ttk.Button(frame1, comman = lambda:ejecution(root, frame1, self, text1, text2, text21,text3,text4))
        button1.configure(text="Ejecutar")
        button1.pack(side="top")
        frame1.pack(side="top")

        # Main widget
        self.mainwindow = frame1

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title('CMPSS AGROMETEOROLOGÍA MODELO 7')
    app = NewprojectApp(root)
    app.run()
