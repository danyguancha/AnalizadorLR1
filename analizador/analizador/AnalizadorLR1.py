
from typing import List
import functools
from prettytable import PrettyTable

from GUI import *

class AnalizadorLR1:
    def __init__(self):
        self.gramatica: List[List[str]] = []  #Utilizado para almacenar la gramática introducida por el usuario
        self.gramaticaAumentada =[]  #Almacenamos la gramatica despues de aumentar el punto
        self.nodos=[] # almacenamos los nodos del arbol
        self.encabezadoTabla =[] # encabezado de la tabla
        self.entradasTabla =[] # almacenamos las filas de la tabla
        
    def obtenerEntrada(self):
        
        ing1 =['S','C','C']
        ing2 =['C','a','C']
        ing3 =['C','d']
        
        self.gramatica.append(ing1)
        self.gramatica.append(ing2)
        self.gramatica.append(ing3)
        
        """ing1 =['S','B','C','|','D','A']
        ing2 =['B','b']
        ing3 =['C','A','A']
        ing4 =['A','a']
        ing5 =['D','b','a']
        
        self.gramatica.append(ing1)
        self.gramatica.append(ing2)
        self.gramatica.append(ing3)
        self.gramatica.append(ing4)
        self.gramatica.append(ing5)"""
     
        return self.gramatica
    
    
    def primeraInterfaz(self,produccion):
        primero =[]
        
        for i in produccion:
            listaTemp = ['$',i]
            
            primeroTemp = self.retornarPrimero(listaTemp)
            j=0
            while j < len(primeroTemp):
                if primeroTemp[j] in primero: #Omitir símbolo si ya está presente en la primera lista
                    j = j+1
                    continue
                primero.append(primeroTemp[j]) #Adicionamos el nuevo símbolo a la primera lista
                j= j +1
        
        return primero
   

    
    def retornarPrimero(self,lista):
        lista1 =[] #glist
        lista2 =[] #tlist
       
        for i in range(1,len(lista)):
            if lista[i]=='|':
                lista1.append(lista2)
                lista2=[]
            else:
                lista2.append(lista[i])
        lista1.append(lista2)
        
        listaInicial:List[List[str]]=[]
        
        #Ciclo externo que accede al producto individual de cada no terminal
        for i in lista1:
            #Ciclo interno accediendo al token individual de producción
            #print(i)
            for j in i:
                
                if j == '$':
                    continue
                #Si el token es épsilon, primero busque paradas para la producción
                if j == 'e':
                    listaInicial.append(j)
                    break
                #Si el token es un terminal, se agrega al primero
                elif j.islower():
                    listaInicial.append(j)
                #Si Non-Terminal es igual que para la producción en proceso, ignore Non-Terminal
                elif j.isupper():
    
                    if j == lista[0]:
                       continue
                    #Selección De Producción Para No Terminal
                    aux =[]
                    term =[]
                    primeroNoTerminal=[]
                    for g in self.gramatica:
                        if g[0]==j:
                            aux = g
                            #print(aux)
                            #break
                            term.append(self.retornarPrimero(aux))
                            #break
                            
                    #Determinación del primero de los no terminales
                    #print(term)
                    
                    for i in term:
                        primeroNoTerminal.append(i[0])
                    
                    #primeroNoTerminal = self.retornarPrimero(aux)
                   
                    #Agregar primero de no terminal a la primera lista
                    for c in primeroNoTerminal:
                        
                        if c =='e':
                            continue #No agregue elementos ya presentes en la primera lista, no agregue elementos duplicados
                        if c in listaInicial:
                            #print(c)
                            continue
                        listaInicial.append(c)
                    #Si Epsilon no está en primeroNoTerminal, entonces primero busque paradas para la producción
                    if 'e' not in primeroNoTerminal:
                        break
       
        return listaInicial
    
    
    def agregarPunto(self):
        produccionNueva = ["H", '.', 'S']
        self.gramaticaAumentada.append(produccionNueva) # Agregamos la nueva produccion
        for g in self.gramatica:
            produccionNueva = [g[0], '.']
            for i in range(1, len(g)):
                if g[i]=='|':
                    self.gramaticaAumentada.append(produccionNueva)
                    produccionNueva=[g[0], '.']
                    continue
                produccionNueva.append(g[i])
            self.gramaticaAumentada.append(produccionNueva)
        return self.gramaticaAumentada
    #Función para crear el primer nodo del árbol
    def crearPrimerNodo(self):
        lineaUno = self.gramaticaAumentada[0].copy()
        lineaUno.append(',')
        lineaUno.append('$')
        
        nodoActual = [lineaUno]
        
        for i in self.gramaticaAumentada:
            if i[0] == 'S':
                lineaDos = i.copy()
                lineaDos.append(',')
                lineaDos.append('$')
                nodoActual.append(lineaDos)
        
        #Representar el nodo I0 en el árbol
        
        #print(nodoActual)
        i = 1
        
        while i < len(nodoActual):
            
            lineaActual = nodoActual[i]  # produccion actual
            #print(lineaActual)
            indiceDelPunto = lineaActual.index('.')  #Determinación del índice de puntos en la producción actual
            
            if lineaActual[indiceDelPunto+1]==',':
                continue # Continuar si el punto está en la posición más a la derecha
            primeraProd = lineaActual[indiceDelPunto +2:] #Elementos para encontrar primero de
            #print(primeraProd)
            j = 0
            while j < len(primeraProd):
                #print(primeraProd[j])
                if primeraProd[j]==',':
                    primeraProd.pop(j)
                else:
                    j=j+1
            restoDePrimero = self.primeraInterfaz(primeraProd) # primer resultado
            #print(restoDePrimero)
            siguienteSimbolo = lineaActual[indiceDelPunto + 1]
            #print(restoDePrimero)
            aux =[]
            
            if siguienteSimbolo.isupper():
                #print(siguienteSimbolo)
                for a in self.gramaticaAumentada:
                    #print(a[0])
                    if a[0]==siguienteSimbolo:
                        aux = a.copy()
                        aux.append(',')
                       
                        """if 'a' in aux or 'd' in aux:
                            aux.append('a')
                            aux.append('d')
                        else:"""
                        for f in restoDePrimero:
                            aux.append(f)
                        nodoActual.append(aux)
                        #print(nodoActual)
            
            i = i + 1
        self.nodos.append(nodoActual)    
        return self.nodos
    

    
    def cambioDelPunto(self, produccion):
        indiceDelPunto= produccion.index('.') # Obtenemos el indice del punto
        siguienteCaracter = produccion[indiceDelPunto + 1] #Obtenemos el carácter a la derecha del punto
        #Desplazamiento del punto una posición a la derecha
        copiaProduccion = produccion.copy()
        copiaProduccion[indiceDelPunto]=siguienteCaracter
        copiaProduccion[indiceDelPunto + 1] = '.'
        return copiaProduccion #Retornamos la produccion actualizada
    
    def crearEncabezadoTabla(self):
        listaTerminales =[] #Almacenamos los simbolos terminales
        listaNoTerminales =[] # Almacenamos los simbolos no terminales
        for g in self.gramaticaAumentada:
            for s in g:
                if s == '.' or s == "H":
                    continue
                if s.isupper():
                    if s in listaNoTerminales:
                        continue
                    listaNoTerminales.append(s)
                if s.islower():
                    if s in listaTerminales:
                        continue
                    listaTerminales.append(s)
        listaTerminales.sort()#-------------------------
        listaTerminales.append('$')
        listaNoTerminales.sort()
        for t in listaTerminales:
            self.encabezadoTabla.append(t)
        
        for n in listaNoTerminales:
            self.encabezadoTabla.append(n)
        self.encabezadoTabla=['Estado No. '] + self.encabezadoTabla
        return self.encabezadoTabla
    
    def obtenerIndiceNodo(self, produccion):
        i = 0
        while i < len(self.nodos):
            n = self.nodos[i]
            if functools.reduce(lambda p, l:p and l, map(lambda m, k: m==k, produccion,n[0]),True):
                return i
            i = i + 1
    
    def mostrarNodos(self):
        for i in range(0, len(self.nodos)):
            print('-------------------------')
            print('Estado. '+str(i))
            mostrarStr = ""
            for j in range(0, len(self.nodos[i])):
                mostrarStr = self.nodos[i][j][0]+"->"
                for k in range(1,len(self.nodos[i][j])):
                    #print(self.nodos[i][j][k])
                    mostrarStr = mostrarStr +self.nodos[i][j][k] 
                    
                    
                print(mostrarStr)
    # actualizar el nodo final de la tabla de análisis
    def actualizarNodoFinalTabla(self, produccion, posicicion):
        prodActual = produccion.copy()
        indiceComa = prodActual.index(',')
        prod = prodActual[0:indiceComa]
        avanzarSiguiente = prodActual[indiceComa + 1:]
        gramaticaLocalAumentada = []
        linea = ["H", 'S', '.']
        gramaticaLocalAumentada.append(linea)
        for g in self.gramatica:
            linea = [g[0]]
            for i in range(1, len(g)):
                if g[i]=='|':
                    gramaticaLocalAumentada.append(linea)
                    linea = [g[0]]
                    continue
                linea.append(g[i])
            gramaticaLocalAumentada.append(linea)
        for i in range(0, len(gramaticaLocalAumentada)):
            g = gramaticaLocalAumentada[i]
            if functools.reduce(lambda p, l: p and l, map(lambda m, k: m == k, prod, g[0:len(g) - 1]), True):
                filasTabla =[]
                for p in self.encabezadoTabla:
                    filasTabla.append(' ')
                filasTabla[0]= posicicion
                string = 'r' + str(i)
                
                if i ==0:
                    filasTabla[self.encabezadoTabla.index('$')]= 'Aceptado'
                    self.entradasTabla.append(filasTabla)
                    continue
                for l in avanzarSiguiente:
                    filasTabla[self.encabezadoTabla.index(l)]=string
                self.entradasTabla.append(filasTabla)
                break
    
    def actualizarTabla(self, prodSiguiente, caracDerPunto ,i , indiceNodo):
        existeFila = False
        indiceFila = -1
        pt = 0
        for pt in range(0, len(self.entradasTabla)):
            if self.entradasTabla[pt][0]==i:
                existeFila = True
                indiceFila = pt
                break
        if not existeFila:
            filasTabla =[]
            for p in self.encabezadoTabla:
                filasTabla.append(' ')
            if caracDerPunto.isupper():
                filasTabla[0]=i
                filasTabla[self.encabezadoTabla.index(caracDerPunto)] = str(indiceNodo)
            if caracDerPunto.islower():
                filasTabla[0]=i
                filasTabla[self.encabezadoTabla.index(caracDerPunto)]='S'+str(indiceNodo)
            self.entradasTabla.append(filasTabla)
        else:
            filasTabla=self.entradasTabla[indiceFila]
            if caracDerPunto.isupper():
                filasTabla[self.encabezadoTabla.index(caracDerPunto)]=str(indiceNodo)
            if caracDerPunto.islower():
                filasTabla[self.encabezadoTabla.index(caracDerPunto)]='S'+str(indiceNodo)
            self.entradasTabla[indiceFila]= filasTabla
            
    def crearArbol(self):
        indiceUltimoNodo=len(self.nodos)
        i=0
        while i < len(self.nodos):
            nodoActual = self.nodos[i]
            j=0
            while j < len(nodoActual):
                produccionNueva = nodoActual[j]
                indicePunto = produccionNueva.index('.')
                caracDerPunto=produccionNueva[indicePunto + 1]
                if produccionNueva[indicePunto + 1] == ',':
                    self.actualizarNodoFinalTabla(produccionNueva,i)
                    j = j + 1
                    continue
                produccionSig = self.cambioDelPunto(produccionNueva)
                existe = False
                indiceNodo = -1
                z =0
                for z in range(0, len(self.nodos)):
                    n = self.nodos[z]
                    if functools.reduce(lambda p, l: p and l, map(lambda m, k: m == k, produccionSig, n[0]), True):
                        indiceNodo = z
                        existe = True
                if existe:
                    self.actualizarTabla(produccionSig,caracDerPunto,i,indiceNodo)
                    j = j + 1
                    continue
                nuevoNodo = [produccionSig]
                indicePunto = nuevoNodo[0].index('.')
                
                if nuevoNodo[0][indicePunto + 1]==',':
                    self.nodos.append(nuevoNodo)
                    self.actualizarTabla(produccionSig,caracDerPunto,i,indiceUltimoNodo)
                    indiceUltimoNodo = indiceUltimoNodo + 1
                    j = j + 1
                    continue
                primeraProd = nuevoNodo[0][indicePunto + 2:]
                k =0
                while k < len(primeraProd):
                    if primeraProd[k]==',':
                        primeraProd.pop(k)
                    else:
                        k = k + 1
                restoPrimero = self.primeraInterfaz(primeraProd)
                if len(restoPrimero)==0:
                    restoPrimero=['$']
                simboloSig = nuevoNodo[0][indicePunto + 1]
                
                if simboloSig.isupper():
                    for a in self.gramaticaAumentada:
                        if a[0]==simboloSig:
                            aux = a.copy()
                            aux.append(',')
                            for f in restoPrimero:
                                aux.append(f)
                            nuevoNodo.append(aux)
                self.nodos.append(nuevoNodo)
                self.actualizarTabla(produccionSig,caracDerPunto,i, indiceUltimoNodo)
                indiceUltimoNodo = indiceUltimoNodo + 1
                j = j + 1
            i = i +1
        return self.nodos
    

    
    def getEntradasTabla(self):
        return self.entradasTabla
        
    def salidaDatos(self):
        salida = self.obtenerEntrada()
        self.agregarPunto()
        self.crearEncabezadoTabla()
        salida2 =self.crearPrimerNodo()
        salida3 = self.crearArbol()
        
        print('\nEstados')
        self.mostrarNodos()
        tabla = PrettyTable()
        tabla.field_names=self.encabezadoTabla
        print('\nTabla LR1')
        for p in self.entradasTabla:
            tabla.add_row(p)
        print(tabla)
#salida = AnalizadorLR1()
#salida.salidaDatos()
        
        
        
            
        
        
        
        
    