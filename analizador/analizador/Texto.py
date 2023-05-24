from operator import index
from textwrap import wrap
from tkinter import font, ttk
from tkinter import *
import tkinter
from tkinter.scrolledtext import ScrolledText
from turtle import width
from AnalizadorLR1 import *
import graphviz

class GUI:
    
    def __init__(self, gui):
        self.window = gui
        self.window.title("Analizador LR1 con python")
        self.Terminals = []
        self.Table = []
        self.arra =[]
        
        self.analiza = AnalizadorLR1()
        #self.gram = self.analiza.obtenerEntrada([])
        self.gram2 = self.analiza.agregarPunto()
        self.encabezado = self.analiza.crearEncabezadoTabla()
        self.primerNodo = self.analiza.crearPrimerNodo()
        self.arbol = self.analiza.crearArbol()
        self.entradasTabla = self.analiza.getEntradasTabla()
        self.nick = StringVar()
        self.texto = []
        
        # ================ Contenedor para los botones ================
        self.frameBtn = LabelFrame(self.window, text="Menu opciones",
                                font=("Arial", 15), background="cyan")
        self.frameBtn.place(x=10, y=5, width=575, height=280)
        
        
        # ================ Contenedor para las tablas ================
        self.frame = LabelFrame(self.window, text="Visualización datos",
                            font=("Arial", 15), background="lightgray")
        self.frame.place(x=10, y=290, width=575, height=360)
        

        # =========== Botones para manipular la interfaz ==============
        

        # =========== Ver gramatica inicial sin aplicar recursion izquierda ============
        
        
    def Gramatica1(self):
        
        
        s = ttk.Style()
        s.theme_use('clam')

        # Configura los estilos de la cabecera de la tabla
        s.configure('Treeview.Heading', background="#ff6961")
        
        tree = ttk.Treeview(self.frame, column=("c1", "c2"),show='headings', height=15)
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="No Terminal")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Produccion")
        
        for i in range(len(self.gram)):
            tree.insert('', "end", text="1", values=(self.gram[i][0], [self.gram[i][1:]]))
        
        tree.place(x=0, y=5)

    # =========== Aumentar la Gramatica y sacar I-0 ============

    def PrepararGramaticaa(self):
        #self.result = PrepareProduction.PrepareProductionForLR(PrepareProduction(self.noTerminals, self.initial, self.productions))
        #self.result = PrepararGramatica.asignarPunto(PrepararGramatica(self.noTerminals, self.initial, self.productions))
        s = ttk.Style()
        s.theme_use('clam')
        #print(self.result)
        # Configura los estilos de la cabecera de la tabla
        s.configure('Treeview.Heading', background="lightgray")

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
        tree.place(x=0, y=5)

    # =========== Realizar LR1 ============
    def RealizarLR1(self):
                    
        s = ttk.Style()
        s.theme_use('clam')
        #print(self.result)
        # Configura los estilos de la cabecera de la tabla
        s.configure('Treeview.Heading', background="lightgray")
        #self.e = LR.LoopArray()
        label1 = Label(self.frame,text="los estados son {0}".format(len(self.arbol)) )
        label1.place(x=10, y=290)
        #print(rn)
        label = Label(self.frame,text=self.arbol)
        label.place(x=10, y=260)

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
        s.configure('Treeview.Heading', background="lightgray")

        tree = ttk.Treeview(self.frame, column=("c1", "c2"),
                            show='headings', height=15)
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="No Terminal")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Produccion")
        print()
        for i in range(len(element)):
            tree.insert('', "end", text="1", values=(element[i][0], [element[i][1:]]))
        tree.place(x=0, y=5)
        
    

    def crearTabla(self):
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("Treeview", rowheight=25, font=("Arial", 8))
        s.configure('Treeview.Heading', background="lightgray")
        
        
        tree = ttk.Treeview(self.frame, column=("C1","C2","C3","C4","C5","C6","C7","C8"),show='headings', height=15)
        for i, e in enumerate(self.encabezado):
            
            column_name = f"#{i+1}"
            
            #tree = ttk.Treeview(frame, column=str(i),show='headings', height=15)
            tree.column(column_name, anchor=CENTER, width=70)
            tree.heading(column_name, text=str(e))
        for j in range(len(self.entradasTabla)):
            valores = [self.entradasTabla[j][k] for k in range(len(self.encabezado))]
            tree.insert('', "end", text="1", values=valores)
        
        """tree = ttk.Treeview(frame, column=("C1","C2","C3","C4","C5","C6","C7"),show='headings', height=15)
                    
        
        tree.column("# 1", anchor=CENTER,width=100)
        tree.heading("# 1", text=self.encabezado[0])
        tree.column("# 2", anchor=CENTER,width=50)
        tree.heading("# 2", text=self.encabezado[1])
        tree.column("# 3", anchor=CENTER,width=50)
        tree.heading("# 3", text=self.encabezado[2])
        tree.column("# 4", anchor=CENTER,width=100)
        tree.heading("# 4", text=self.encabezado[3])
        tree.column("# 5", anchor=CENTER,width=50)
        tree.heading("# 5", text=self.encabezado[4])
        tree.column("# 6", anchor=CENTER,width=50)
        tree.heading("# 6", text=self.encabezado[5])
        tree.column("# 7", anchor=CENTER,width=50)
        tree.heading("# 7", text=self.encabezado[5])
        
        for j in range(len(self.entradasTabla)):
            valores = [self.entradasTabla[j][k] for k in range(len(self.encabezado))]
            tree.insert('', "end",text="1", values=valores)"""
                
        tree.place(x=0, y=5)

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
        contenido = entradaGramatica.get("1.0",END)
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
        self.analiza.obtenerEntrada(salida1)
                
                
            #return salida1
            #S->CC,C->aC,C->d
    def botones(self):
    
        btn_font = font.Font(family="Roboto Cn", size=11)
        Button(self.frameBtn, text="Ver Gramatica", font=btn_font, background="#FFF7E9",
                command=self.Gramatica1).place(x=320, y=5, width=200, height=35)
        
        Button(self.frameBtn, text="Cargar Gramatica", font=btn_font, background="#FFF7E9",
                command=self.obtenerEntrada).place(x=140, y=100, width=150, height=35)
        
        Button(self.frameBtn, text="Preparar Gramatica", font=btn_font, background="#FFF7E9",
                command=self.PrepararGramaticaa).place(x=320, y=45, width=200, height=35)
        Button(self.frameBtn, text="Sacar LR1", font=btn_font, background="#FFF7E9",
                command=self.RealizarLR1).place(x=320, y=85, width=200, height=35)
        
        insert_nick = Entry(self.frameBtn, width=20, textvariable=self.nick)
        insert_nick.place(x=320, y=130)
        
        entradaGramatica = ScrolledText(self.window, wrap="word")
        entradaGramatica.place(x=150, y=50, width=150, height=70)
        
        
        boton_nick = Button(self.frameBtn, text="Crear tabla", command=self.crearTabla)
        boton_nick.place(x=450, y=170)
        
        boton_nick = Button(self.frameBtn, text="Graficar Automata", command=self.graficarAutomata)
        boton_nick.place(x=450, y=200)
        
        boton_nick = Button(self.frameBtn, text="Ver estado", command=self.returnElement)
        boton_nick.place(x=450, y=130)
    
        
if __name__ == "__main__":
    gui = Tk()
    gui.geometry("600x650")
    gui.configure(bg="orange")
    gui.resizable(False,False)
    app = GUI(gui)
    app.obtenerEntrada()
    app.botones()
    gui.mainloop()