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

def leerDataContador():
    #leer json con el data de estadisticas
    try:
        file = open(archivo_contador,mode='r')
        c = json.loads( str(file.read()))
        #print(c)
        for attrs in c:   
            print ('sitio: \t',attrs['sitio'], '\t numero de consultas :', attrs['contador'])  
        file.close()
        return c
    except:
        print('no hay archivo de contador')
        return []

def addContadorJson(sitio):
#funcion que agrega un usuario 
    CONTADOR.append( {"sitio": sitio, "contador":  0})
    #print(CONTADOR)

def grabarContador():   
# funcion que guarda los usuarios en un archivo de texto json
    print('grabando contador')
    arch = open(archivo_contador, "w")
    arch.write(str(CONTADOR).replace("'",'\"'))
    arch.close()   

def incrementarContador(destino):
#buscamos los usuarios en el archivo cargando el json
    for attrs in CONTADOR:
        if (attrs['sitio'] == destino):
            print('encontrado')
            #encontrado = True
            x = attrs['contador']
            x = x + 1
            attrs['contador']  = x
            break
    print(CONTADOR)

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


def agregarCarretera():
    try:
        origen = str.upper(input('Ingrese sitio origen:'))
        destino = str.upper(input('Ingrese sitio destino:'))
        peso = int(input('Ingrese la distancia en kilometros:'))
        G.add_edge(origen,destino,weight = peso)
        salvarGrafos() 
    except ValueError:
        print("No es un nummero valido")

def agregarCarreteraBandera():
    try:
        origen = str.upper(input('Ingrese sitio origen:'))
        destino = str.upper(input('Ingrese sitio destino:'))
        peso = VALORBANDERA  #int(input('Ingrese la distancia en kilometros:'))
        G.add_edge(origen,destino,weight = peso)    
        salvarGrafos() 
    except ValueError:
        print("No es un nummero valido")


def agregaNodo():
    try:
        etiqueta = str.upper(input('Ingrese Nombre del Sitio Turistico:'))
        G.add_node(etiqueta)
        addContadorJson(etiqueta)
        grabarContador()
    except ValueError:
        print("No es un dato valido")
        salvarLog(usr,'error: ha ingresado un dato no valido.')

def rutaMasCorta():
    origen = str.upper(input('Ingrese  lugar de partida Origen:'))
    destino = str.upper(input('Ingrese lugar de Destino:'))
    incrementarContador(destino)
    try:  # esta es una excepcion por si la ruta no existe, o el nodo no tiene carretera
        path = nx.shortest_path(G, source=origen, target=destino, weight=None, method='dijkstra')
        print ('ruta mas corta: ',path,' con un total de sitios a recorrer: ', len(path))
        salvarLog(usr,'info: se ha mostrado la ruta mas corta.')
        kms = 0
        G2 = nx.Graph()
        alerta = False;
        for x in range(len(path)-1):
            if (G[path[x]][path[x + 1]]["weight"] == VALORBANDERA):
                print('*****************************')
                print('en esta ruta hay una alerta')
                print('ruta: ',path[x], path[x + 1],' kilometros: ' ,G[path[x]][path[x + 1]]["weight"])
                print('*****************************')
            print('ruta: ',path[x], path[x + 1],' kilometros: ' ,G[path[x]][path[x + 1]]["weight"])
            kms = kms + G[path[x]][path[x + 1]]["weight"]
        #sumamos los kilometros con la ruta total
            G2.add_edge(path[x],path[x + 1],weight = G[path[x]][path[x + 1]]["weight"])
        print('kilometros totales a recorrer: ',kms)
        salvarLog(usr,'info: se han mostrado los kilometros a recorrer.')
        #mostramos la ruta mas corta 
        nx.draw(G2,with_labels=True)
        plt.savefig("graph2.png")
        plt.show() 
    except  nx.exception.NetworkXNoPath:
        print('no existe ruta entre: ', origen, ' ',destino)
        
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
