#importar librerias
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

#Crear las clases para las ventanas, y generar las dependencias a la primera interfaz
#interfaz 1
class Interfaz1(QMainWindow):
    def __init__(self):
        super(Interfaz1, self).__init__() #asignación de interfaz encargada
        loadUi("interfaz1.ui", self) #cargar la interfaz correspondiente
        self.empezar.clicked.connect(self.abrirInterfaz2) #boton de activación para ir a la siguiente interfaz
        
    def abrirInterfaz2(self):
        self.hide() #esconder la interfaz anterior
        nuevainterfaz = Interfaz2(self) #Asignar una variable para la nueva interfaz
        nuevainterfaz.show()

#Interfaz 2
class Interfaz2(QMainWindow): 
    def __init__(self, parent = None): #herencia de interfaz de una a otra
        super(Interfaz2, self).__init__(parent)
        loadUi("interfaz2.ui", self) #cargar la interfaz correspondiente
        self.estadistica.clicked.connect(self.abrirInterfaz3) #boton de activación para ir a la siguiente interfaz
        self.cargadatos.clicked.connect(self.frame)
        
    def getDataMaquina(self):
        datamaquina = pd.read_excel("DataMaquina.xlsx")
        M = datamaquina.to_numpy
        
        return M

    def getDataEmpaque(self):
        dataempaque = pd.read_excel("DataEmpaque.xlsx")
        E = dataempaque.to_numpy
        
        return E

    def frame(self):
        #Graficación DataFrame DataMaquina
        
        #asignar criterios para los Head Labels
        '''
        Abreviaturas:
        Dia = Dia
        averias equipo = AE
        Preparativos y cambios de referencia = PCR
        Paros perifericos = PP
        Paros menores = PM
        Velocidad reducidad = VR
        Arranque = A
        defectos y reprocesos = DR
        Paros Programados = PPG
        Administrativos = ADM
        Movimientos innecesarios = MI
        Desbalance en linea de producción = DLP
        Inspección y ajuste de calidad = IAC
        Falta de herramientas = FH
        Energía = E
        
        '''
        criterios = ['Dia', 'AE', 'PCR', 'PP', 'PM', 'VR', 'A', 'DR', 'PPG', 'ADM', 'MI', 'DLP', 'IAC', 'FH', 'E']
        
        #()() es para asignar la función y luego el return
        self.maquina.setRowCount(self.getDataMaquina()().shape[0]) #Obtener filas
        self.maquina.setColumnCount(self.getDataMaquina()().shape[1]) #obtener columnas
        #head labels
        self.maquina.setHorizontalHeaderLabels((criterios))
        
        #Ciclo, para tomar todos los valores del archivo
        for i in range(self.getDataMaquina()().shape[0]):
            for j in range(self.getDataMaquina()().shape[1]):
                self.maquina.setItem(i, j, QTableWidgetItem(str(self.getDataMaquina()()[i, j])))
                
        self.maquina.show()
        
        #Graficación DataFrame DataEmpaque
        self.empaque.setRowCount(self.getDataEmpaque()().shape[0])
        self.empaque.setColumnCount(self.getDataEmpaque()().shape[1])
        #Head Labels
        self.empaque.setHorizontalHeaderLabels((criterios))
        
        for i in range(self.getDataEmpaque()().shape[0]):
            for j in range(self.getDataEmpaque()().shape[1]):
                self.empaque.setItem(i, j, QTableWidgetItem(str(self.getDataEmpaque()()[i, j])))
                
        self.empaque.show()

    def abrirInterfaz3(self):
        self.hide() #esconder interfaz anterior
        nuevainterfaz3 = Interfaz3(self) #Asignar una variable para la nueva interfaz
        nuevainterfaz3.show()
        
#Interfaz 3
class Interfaz3(QMainWindow):
    def __init__(self, parent = None): #herencia de interfaz de una a otra
        super(Interfaz3, self).__init__(parent)
        loadUi("interfaz3.ui", self) #cargar la interfaz correspondiente
        self.resumen.clicked.connect(self.abrirInterfaz4) #boton de activación para ir a la siguiente interfaz
        self.graficar.clicked.connect(self.check)
        self.M = self.getDataMaquina()
        self.E = self.getDataEmpaque()
        
    
    #funciones de archivos
    def getDataMaquina(self):
        datamaquina = pd.read_excel("DataMaquina.xlsx")
        M = datamaquina.to_numpy()
        
        return M

    def getDataEmpaque(self):
        dataempaque = pd.read_excel("DataEmpaque.xlsx")
        E = dataempaque.to_numpy()
        
        return E

    def plot(self):
        selected_radio = None
        if self.radiomaquina.isChecked():
            selected_radio = self.radiomaquina
        elif self.radioempaque.isChecked():
            selected_radio = self.radioempaque
            
        if selected_radio is None:
            return

        column_name = self.BoxMaquina.currentText()
        plot_type = self.BoxGrafico.currentText()
        
        data = self.M if selected_radio == self.radiomaquina else self.E
        
        #convertir columnas en indices
        if selected_radio == self.radiomaquina:
            index = pd.read_excel("DataMaquina.xlsx")
        else:
            index = pd.read_excel("DataEmpaque.xlsx")
        
        if column_name in index.columns:
            index_col = index.columns.get_loc(column_name)
            data = data[:, index_col]
        else:
            print(f"La columna '{column_name}' no se encuentra en 'index' ")
            return
        
        df = pd.DataFrame(data, columns = [column_name])
        
        plt.figure(figsize = (8, 6))
        if plot_type ==  "Barras":
            plt.hist(data, bins = 10)
        elif plot_type == "Box Plot":
            plt.boxplot(df)
        elif plot_type == "Histograma":
            plt.bar(df.index.values, df.values[0])
        
        plt.show()
    
    #función error, esto es por si no existe una selección
    def error(self):
        QMessageBox.warning(self, 'Error', 'Seleccione una opción')
    
    #funcion de checkeo de selección
    def check(self):
        #revisar si los combobox tiene una selección
        if self.BoxMaquina.currentIndex() == 0 and self.BoxGrafico.currentIndex() == 0:
            self.error()
            return
        
        #revisar si uno de los dos radio button está seleccionado
        if not (self.radiomaquina.isChecked() or self.radioempaque.isChecked()):
            self.error()
            return 
        
        #si todo sale bien llamamos al metodo de graficación
        self.plot()

    def abrirInterfaz4(self):
        self.hide() #esconder interfaz anterior
        nuevainterfaz4 = Interfaz4(self) #Asignar una variable para la nueva interfaz
        nuevainterfaz4.show()

#Interfaz 4
class Interfaz4(QMainWindow):
    def __init__(self, parent = None): #herencia de interfaz de una a otra
        super(Interfaz4, self).__init__(parent)
        loadUi("interfaz4.ui", self) #cargar la interfaz correspondiente
        self.inicio.clicked.connect(self.abrirInterfaz21) #boton de activación para ir a la siguiente interfaz
        self.datosresumen.clicked.connect(self.cargaresumen)

    def cargaresumen(self):
        #obtener data frames
        dfM = pd.DataFrame(pd.read_excel("DataMaquina.xlsx"))
        dfE = pd.DataFrame(pd.read_excel("DataEmpaque.xlsx"))
        
        #calcular resumen
        resumen_dataM = dfM.describe()
        resumen_dataE = dfE.describe()
        
        #establecer las propiedades de los QTableWidget
        self.rmaquina.setRowCount(len(resumen_dataM))
        self.rmaquina.setColumnCount(len(resumen_dataM.columns))
        self.rempaque.setRowCount(len(resumen_dataE))
        self.rempaque.setColumnCount(len(resumen_dataE.columns))
        
        #ingresar los datos en los QTableWidget
        criterios = ['Conteo', 'promedio', 'desviación estandar', 'valor min', 'Q25%', 'Q50%', 'Q70%', 'valor max']
        keys =  ['Dia', 'AE', 'PCR', 'PP', 'PM', 'VR', 'A', 'DR', 'PPG', 'ADM', 'MI', 'DLP', 'IAC', 'FH', 'E']
        
        for i in range(len(resumen_dataM)):
            for j in range(len(resumen_dataM.columns)):
                self.rmaquina.setItem(i, j, QtWidgets.QTableWidgetItem(str(resumen_dataM.iloc[i,j])))
        self.rmaquina.setVerticalHeaderLabels((criterios))
        self.rmaquina.setHorizontalHeaderLabels((keys))
        
        for i in range(len(resumen_dataE)):
            for j in range(len(resumen_dataE.columns)):
                self.rempaque.setItem(i, j, QtWidgets.QTableWidgetItem(str(resumen_dataE.iloc[i,j])))
        self.rempaque.setVerticalHeaderLabels((criterios))
        self.rempaque.setHorizontalHeaderLabels((keys))

    def abrirInterfaz21(self):
        self.hide() #esconder interfaz anterior
        nuevainterfaz21 = Interfaz2(self) #Asignar una variable para la nueva interfaz
        nuevainterfaz21.show()

##MAIN APERTURA##
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ppal = Interfaz1() #La interfaz que posee el MAIN es la Interfaz1
    ppal.show()
    sys.exit(app.exec_())