#si se trabaja en windows hay que instalar los headers y compiladores de c y c++ desde este link Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
# luego se instalan las librerias usando pip como se muestra en la descripcion de las librerias. 
# codigo de las librerias usadas en los grafos para documentacion: https://networkx.org/documentation/networkx-1.10/_modules/networkx/algorithms/shortest_paths/weighted.html#dijkstra_path
import json
from typing import Any
import networkx as nx #pip install networkx
import matplotlib.pyplot as plt #pip install matplotlib
from datetime import datetime
import math
usuarioAdmin = 'root'
passwordAdmin = 'toor'

archivo_usuarios = 'usuarios.json'
archivo_grafos = 'grafos.csv'
archivo_contador = 'contador.json'

#objeto grafo
G = nx.Graph()
labels = {}

VALORBANDERA = 1000000
CONTADOR = []


#void main()
if __name__ == '__main__':
    print("starting")
    usuarios = leerDataUsr() #cargamos usuarios
    CONTADOR = leerDataContador()
    cargaArchivoGrafos()#cargamos grafos
    usr = str(input('Ingrese usuario:'))
    pwd = str(input('Ingrese password:'))
    if ((usr == usuarioAdmin) and (pwd == passwordAdmin)):
        menuAdmin()
    else:
        if (buscaUsuario(usr,pwd)):
            menu()
        else:
            print('usuario o password no valido')
    #print(CONTADOR)    
    grabarContador()