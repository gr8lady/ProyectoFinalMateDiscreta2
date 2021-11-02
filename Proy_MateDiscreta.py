#si se trabaja en windows hay que instalar los headers y compiladores de c y c++ desde este link Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
# luego se instalan las librerias usando pip como se muestra en la descripcion de las librerias. 
import json
import networkx as nx #pip install networkx
import matplotlib.pyplot as plt #pip install matplotlib
from datetime import datetime


usuarioAdmin = 'root'
passwordAdmin = 'toor'

archivo_usuarios = 'usuarios.json'
archivo_grafos = 'grafos.csv'

#objeto grafo
G = nx.Graph()
labels = {}

#JSON USER EXAMPLE
#[{"usuario": "root","password":"toor","tipo":"0"},{"usuario": "User","password":"password","tipo":"1"}]

#archivo grafos
#nombre_origen,nombre_destino,kms
def salvarLog(usuario,mensajeLog):
    now = datetime.now()
    arch = open('log.csv', "a")
    arch.write(usuario + ',' + mensajeLog + ',' + str(now) + '\n')
    arch.close()

#PROCESOS DE USUARIOS
def leerDataUsr():
    #leer json con usuarios
    try:
        file = open(archivo_usuarios,mode='r')
        usuarios = json.loads( str(file.read()))
      #  print (usuarios)  
        file.close()
        return usuarios
    except:
        print('no hay archivo de usuarios o usuarios todavia')
        salvarLog(usuarioAdmin,'error: no hay usuarios creados o el archivo esta vacio.')
        return []


def addUserJson():
#funcion que agrega un usuario 
    usr = str(input('Ingrese nonbre del usuario:'))
    pwd = str(input('Ingrese password:'))
    usuarios.append( {"usuario": usr, "password": pwd, "tipo": "1"})
    print(usuarios)
    if ( buscaUsuario(usr,pwd) == False ):
        grabarUsuarios()
        salvarLog(usuarioAdmin,'info: el usuario ha sido creado.')
    else:
        print('usuario ya existe')
        salvarLog(usuarioAdmin,'warn: el usuario ya existe.')


def grabarUsuarios():
# funcion que guarda los usuarios en un archivo de texto json
    print('grabando usuarios cuando hay algun cambio')
    print(str(usuarios))
    arch = open(archivo_usuarios, "w")
    arch.write(str(usuarios).replace("'",'\"'))
    arch.close()    


def buscaUsuario(usr,pwd):
#buscamos los usuarios en el archivo cargando el json
    encontrado = False;
    for attrs in usuarios:
        if (attrs['usuario'] == usr and attrs['password'] == pwd):
            print('encontrado')
            encontrado = True
            break
    else:
        print('El usuario no se ha encontrado')
        salvarLog(usuarioAdmin, usr +'error: no se ha encontrado el usuario.')
    return encontrado

#PROCESOS MENU    
def menuAdmin():
    opcion = 0
    while (opcion != 10):
        print('1. crear usuario')
        print('2. Agregar sitio turistico')
        print('3. Agregar carreteras')
        print('4. remover carretera')
        print('5. agregar alertas')
        print('6. Log de actividad')
        print('7. ver sitios y carreteras ingresados ')
        print('8. ruta mas corta')
        print('10. salir')

        try:
            opcion = int(input('Ingrese Opcion:'))
        except ValueError:
            print("No es un nummero valido")

        if (opcion == 1):
            addUserJson()
        if (opcion == 2):
            agregaNodo()
        if (opcion == 3):
            agregarCarretera()
        if (opcion == 4):
            borrarCarretera()
        if (opcion == 7):
            verGrafo()
        if (opcion ==8):
            rutaMasCorta()
        salvarGrafos()            

def menu():
# este es el menu del usuario que no es admin 
    opcion = 0
    while (opcion != 5):
        print('1. ingresar sitio turistico a visitar')
        print('2. obtener ruta mas corta')
        print('3. mostrar cantidad de kms')
        print('4. ver alertas')
        print('5. salir')
        try:
            opcion = int(input('Ingrese Opcion:'))
        except ValueError:
            print("No es un nummero valido")
        if (opcion == 1):
            rutaMasCorta()
       

#PROCESOS GRAFOS

def rutaMasCorta():
    origen = str(input('Ingrese Nodo Origen:'))
    destino = str(input('Ingrese Nodo Destino:'))
    path = nx.shortest_path(G, source=origen, target=destino, weight=None, method='dijkstra')
    print ('ruta mas corta: ',path,' con un total de sitios a recorrer: ', len(path))
    salvarLog(usr,'info: se ha mostrado la ruta mas corta.')
    kms = 0
    G2 = nx.Graph()
    
    for x in range(len(path)-1):
        print('ruta: ',path[x], path[x + 1],' kilometros: ' ,G[path[x]][path[x + 1]]["weight"])
        kms = kms + G[path[x]][path[x + 1]]["weight"]
        #creamos ruta 
        G2.add_edge(path[x],path[x + 1],weight = G[path[x]][path[x + 1]]["weight"])
    print('kilometros totales a recorrer: ',kms)
    salvarLog(usr,'info: se han mostrado los kilometros a recorrer.')
    #mostramos la ruta
    nx.draw(G2,with_labels=True)
    plt.savefig("graph2.png")
    plt.show()   
            
        
def agregaNodo():
    try:
        etiqueta = str(input('Ingrese Nombre del Sitio Turistico:'))
        G.add_node(etiqueta)
    except ValueError:
        print("No es un dato valido")
        salvarLog(usr,'error: ha ingresado un dato no valido.')


def verGrafo():
    print(G.nodes())
    print(G.edges(data=True))
    print(labels)
   
    nx.draw(G,with_labels=True)
    plt.savefig("graph.png")
    plt.show()

def agregarCarretera():
    try:
        origen = str(input('Ingrese Nodo Origen:'))
        destino = str(input('Ingrese Nodo Destino:'))
        peso = int(input('Ingrese la distancia en kilometros:'))
        G.add_edge(origen,destino,weight = peso)
        
    except ValueError:
        print("No es un nummero valido")

def borrarCarretera():
    try:
        origen = str(input('Ingrese Nodo Origen:'))
        destino = str(input('Ingrese Nodo Destino:'))
        peso = int(input('Ingrese peso del kilometros:'))
        G.remove_edge(origen,destino,weight = peso)
        
    except ValueError:
        print("No es un nummero valido")
        salvarLog(usr,'error: ha ingresado un dato no valido.')
    

def salvarGrafos():
#grava los datos en un archivo csv que fueron cargados
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
        salvarLog(usr,'error: existe un problema con el archivo de grafos.')

#void main()
if __name__ == '__main__':
    print("starting")
    usuarios = leerDataUsr()#cargamos usuarios
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
    


def despliegaLog():
    usrBuscar = str(input('Ingrese usuario a desplegar:'))
    try:
        file1 = open('log.csv', 'r')
        Lines = file1.readlines()
        for line in Lines:
            x = line.replace('\n','').split(',')
            if (len(x) > 0 and x[0] == usrBuscar):
                print(line)
    except:
        print('hay un problema con el archivo de log')



    
