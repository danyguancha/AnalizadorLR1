from operator import index
from textwrap import wrap
from tkinter import font, ttk
from tkinter import *
import tkinter
from tkinter.scrolledtext import ScrolledText
from turtle import width
from AnalizadorLR1 import *
import graphviz
import tkinter as tk

class GUI:
    
    def __init__(self, gui):
        self.window = gui
        self.window.title("Analizador LR1 con python")
        self.Terminals = []
        self.Table = []
        self.arra =[]
        
        self.analiza = AnalizadorLR1()
        self.gram = self.analiza.obtenerEntrada()
        self.gram2 = self.analiza.agregarPunto()
        self.encabezado = self.analiza.crearEncabezadoTabla()
        self.primerNodo = self.analiza.crearPrimerNodo()
        self.arbol = self.analiza.crearArbol()
        self.entradasTabla = self.analiza.getEntradasTabla()
        self.nick = StringVar()
      
        # ================ Contenedor para las tablas ================
        self.frame = LabelFrame(self.window, text="Visualización datos",
                            font=("Arial", 15), background="lightgray")
        self.frame.place(x=10, y=5, width=600, height=360)
        
        
    def Gramatica1(self):
        s = ttk.Style()
        s.theme_use('clam')

        # Configura los estilos de la cabecera de la tabla
        s.configure('Treeview.Heading', background="brown")
        
        tree = ttk.Treeview(self.frame, column=("c1", "c2"),show='headings', height=15)
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="No Terminal")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Produccion")
        
        for i in range(len(self.gram)):
            tree.insert('', "end", text="1", values=(self.gram[i][0], [self.gram[i][1:]]))
        
        #tree.place(x=0, y=5, width=575, height=360)
        tree.place(x=0, y=5,width=600, height=360)

    # =========== Aumentar la Gramatica y sacar I-0 ============

    def PrepararGramaticaa(self):
        #self.result = PrepareProduction.PrepareProductionForLR(PrepareProduction(self.noTerminals, self.initial, self.productions))
        #self.result = PrepararGramatica.asignarPunto(PrepararGramatica(self.noTerminals, self.initial, self.productions))
        s = ttk.Style()
        s.theme_use('clam')
        #print(self.result)
        # Configura los estilos de la cabecera de la tabla
        s.configure('Treeview.Heading', background="brown")

        tree = ttk.Treeview(self.frame, column=("c1", "c2"),
                            show='headings', height=15)
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="No Terminal")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Produccion")
        self.newNoTerminals = []
        for i in range(len(self.gram2)):
            if not self.newNoTerminals.__contains__(self.gram2[i]):
                # Agrega a una nueva lista los nuevos NoTerminales
                self.newNoTerminals.append(self.gram2[i])
                # Values son las propiedades que se mostraran en la tabla
            tree.insert('', "end", text="1", values=(self.gram2[i][0], [self.gram2[i][1:]]))
        #tree.place(x=0, y=5, width=575, height=360)
        tree.place(x=0, y=5,width=600, height=360)

    # =========== Realizar LR1 ============
    def RealizarLR1(self):
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Treeview.Heading', background="brown")
        tree = ttk.Treeview(self.frame, column=("c1", "c2"),
                            show='headings', height=15)
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="Estados")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Producciones")
        
        for i in range(len(self.arbol)):
            tree.insert('', "end", text="1", values=('Estado. '+str(i), [self.arbol[i]]))
        #tree.place(x=0, y=5, width=575, height=360)
        tree.place(x=0, y=5,width=600, height=360)

    def SacarTerminales(self):
        for production in self.Table:
            p = production
            # Divide los elementos de p
            aux = p[1].split(" ")
            aux2 = p[2]
            #Encuentra los terminales de las producciones
            for k in aux:
                if((k.isupper() == False) and (k not in self.Terminals)):
                    self.Terminals.append(k)
            #Encuentra terminales en el conjunto prediccion
            for a in aux2:
                if((a.isupper() == False) and (a not in self.Terminals)):
                    self.Terminals.append(a)
        return self.Terminals      

    def returnElement(self):
        element = self.arbol[int(self.nick.get())]
        s = ttk.Style()
        s.theme_use('clam')

        # Configura los estilos de la cabecera de la tabla
        s.configure('Treeview.Heading', background="brown")

        tree = ttk.Treeview(self.frame, column=("c1", "c2"),
                            show='headings', height=15)
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="No Terminal")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Produccion")
        print()
        for i in range(len(element)):
            tree.insert('', "end", text="1", values=(element[i][0], [element[i][1:]]))
        #tree.place(x=0, y=5, width=575, height=360)
        tree.place(x=0, y=5,width=600, height=360)
        

    def crearTabla(self):
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("Treeview", rowheight=25, font=("Arial", 8))
        s.configure('Treeview.Heading', background="brown")
        
        column_names = [f"C{i+1}" for i in range(len(self.encabezado))]
        
        tree = ttk.Treeview(self.frame, column=column_names, show='headings', height=15)
        for i, e in enumerate(self.encabezado):
            column_name = column_names[i]
            tree.column(column_name, anchor=CENTER,width=20)
            tree.heading(column_name, text=str(e))

        for j in range(len(self.entradasTabla)):
            valores = [self.entradasTabla[j][k] for k in range(len(self.encabezado))]
            tree.insert('', "end", text="1", values=valores)
        tree.place(x=0, y=5,width=600, height=360)
        #tree.pack(fill='x', padx=10, pady=5)
        
        
    def graficarAutomata(self):
        dot = graphviz.Digraph(comment='Analizador LR1',format='png')
        #dot.attr(rankdir='HR', size='8,5')
        dot.attr(rankdir='LR', size='8,5')
        
        dot.attr('node', shape='circle')
        for i in range(len(self.entradasTabla)):
            lista =[]
            for j in range(len(self.encabezado)):
                lista.append(self.entradasTabla[i][j])
                if self.encabezado[j] == 'Estado No. ':
                    continue
                if str(lista[len(lista)-1]) == ' ':
                    continue
                dot.edge(str(self.entradasTabla[i][0]), str(lista[len(lista)-1]), label=str(self.encabezado[j]))
                
        dot.render('analizador/archivosSalida/analizadorLR1.gv').replace('\\', '/')
        dot.render('analizador/archivosSalida/analizadorLR1.gv', view=True)
        
    def obtenerEntrada(self):
        contenido = self.entradaGramatica.get("1.0",END)
        salida =contenido.split(',')
        retorno =[]
        for i in salida:
            retorno.append([i.strip()])
        salida1 =[]
        for sublist in retorno:
            listaSeparada = []
            for item in sublist:
                item_separado = list(item)
                listaSeparada.append(item_separado)
            salida1.append(listaSeparada)
        return salida1
                
                
            #return salida1
            #S->CC,C->aC,C->d
    def botones(self):
        insert_nick = Entry(self.window, width=20, textvariable=self.nick)
        insert_nick.place(x=340, y=380)
        
        boton_nick = Button(self.window, text="Ver estado", command=self.returnElement)
        boton_nick.place(x=470, y=380)
    
       
if __name__ == "__main__":
    gui = tk.Tk()
    gui.geometry("620x430")
    gui.configure(bg="orange")
    gui.resizable(False,False)
    app = GUI(gui)
    app.botones()
    barra_menus = tk.Menu()
    menu_archivo = tk.Menu(barra_menus, tearoff=False)
    menu_archivo.add_command(label="Ver Gramatica",command=app.Gramatica1)
    menu_archivo.add_command(label="Agregar nueva produccion y punto",command=app.PrepararGramaticaa)
    menu_archivo.add_command(label="Analizador LR1",command=app.RealizarLR1)
    menu_archivo.add_command(label="Generar Tabla",command=app.crearTabla)
    menu_archivo.add_command(label="Graficar Automata",command=app.graficarAutomata)
    barra_menus.add_cascade(menu=menu_archivo, label="Archivo")
    gui.config(menu=barra_menus)
    gui.mainloop()
    

