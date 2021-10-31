import json
import networkx as nx #pip install networkx
import matplotlib.pyplot as plt #pip install matplotlib

usuarioAdmin = 'root'
passwordAdmin = 'toor'

archivo_usuarios = 'usuarios.json'
archivo_grafos = 'grafos.json'

#objeto grafo
G = nx.Graph()
labels = {}

#JSON USER EXAMPLE
#[{"usuario": "root","password":"toor","tipo":"0"},{"usuario": "herlich","password":"password","tipo":"1"}]




#PROCESOS DE USUARIOS
def leerDataUsr():
    #leer json con usuarios
    try:
        file = open(archivo_usuarios,mode='r')
        usuarios = json.loads( str(file.read()))
        print (usuarios)
        file.close()
        return usuarios
    except:
        print('no hay archivo de usuarios o usuarios todavia')
        return []


def addUserJson():
    print('ingrese usuario')
    usr = str(input('Ingrese Opcion:'))
    print('ingrese password')
    pwd = str(input('Ingrese Opcion:'))
    usuarios.append( {"usuario": usr, "password": pwd, "tipo": "1"})
    print(usuarios)
    if ( buscaUsuario(usr,pwd) == False ):
        grabarUsuarios()
    else:
        print('usuario ya existe')


def grabarUsuarios():
    print('grabando usuarios cuando hay algun cambio')
    print(str(usuarios))
    arch = open(archivo_usuarios, "w")
    arch.write(str(usuarios).replace("'",'\"'))
    arch.close()    


def buscaUsuario(usr,pwd):
    encontrado = False;
    for attrs in usuarios:
        if (attrs['usuario'] == usr and attrs['password'] == pwd):
            print('encontrado')
            encontrado = True
            break
    else:
        print('Nothing found!')
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
        if (opcion == 7):
            verGrafo()

def menu():
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

#PROCESOS GRAFOS
def agregaNodo():
    numNodo = 0
    try:
        numNodo = int(input('Ingrese Numero del Nodo:'))
        etiqueta = str(input('Ingrese Nombre del Nodo:'))
        G.add_node(numNodo)
        labels[numNodo] = etiqueta
    except ValueError:
        print("No es un nummero valido")


def verGrafo():
    print(G.nodes())
    print(G.edges())
    print(labels)

    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos) 
    nx.draw_networkx_edges(G, pos) 
    nx.draw_networkx_labels(G, pos, labels, font_size=16)    
    #nx.draw(G,with_labels=True)
    plt.savefig("graph.png")
    plt.show()

def agregarCarretera():
    origen = 0
    destino = 0
    try:
        origen = int(input('Ingrese Nodo Origen:'))
        destino = int(input('Ingrese Nodo Destino:'))
        G.add_edge(origen,destino)
    except ValueError:
        print("No es un nummero valido")

    

#void main()
if __name__ == '__main__':
    print("starting")
    usuarios = leerDataUsr()
    #TODO LEER GRAFOS

    print('ingrese usuario')
    usr = str(input('Ingrese Opcion:'))
    print('ingrese password')
    pwd = str(input('Ingrese Opcion:'))
    

    if ((usr == usuarioAdmin) and (pwd == passwordAdmin)):
        menuAdmin()
    else:
        if (buscaUsuario(usr,pwd)):
            menu()
        else:
            print('usuario o password no valido')
    
    
