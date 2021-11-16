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

def verGrafo():
    print(G.nodes())
    print(G.edges(data=True))
    print(labels)
    nx.draw(G,with_labels=True)
    plt.savefig("graph.png")
    plt.show()


def borrarCarretera():
    try:
        origen = str.upper(input('Ingrese Nodo Origen:'))
        destino = str.upper(input('Ingrese Nodo Destino:'))
      #  peso = int(input('Ingrese peso del kilometros:'))  no se necesita el peso para eliminar la arista
        #solamente se quita la arista pero no el nodo porque puede tener dependencia o otras carreteras. 
        G.remove_edge(origen,destino)
        salvarGrafos()
    except ValueError:
        print("No es un nummero valido")
        salvarLog(usr,'error: ha ingresado un dato no valido.')


def salvarGrafos():
    print('salvando grafos')
    g = G.edges(data=True)
    #print(g)
    arch = open(archivo_grafos, "w")
    for n in g:
        origen = n[0]
        destino = n[1]
        peso = n[2]['weight']
        arch.write(origen + ',' + destino + ',' + str(peso) + '\n')
    arch.close()     

def cargaArchivoGrafos():
    try:
        file1 = open(archivo_grafos, 'r')
        Lines = file1.readlines()
        for line in Lines:
            x = line.replace('\n','').split(',')
            print(x)
            if (len(x)>0):
                #print(line,x[0],x[1],x[2])
                G.add_edge(x[0],x[1],weight = int(x[2]))
    except:
        print('hay un problema con el archivo de grafos')

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