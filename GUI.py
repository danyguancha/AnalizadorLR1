from operator import index
from tkinter import font, ttk
from tkinter import *
from turtle import width
from PrepararGramatica import *
from AnalizadorLR1 import *

class GUI:
    def __init__(self, gui):
        self.window = gui
        self.window.title("Analyzer LR1 with Python v1.0")
        self.Terminals = []
        self.Table = []
        self.arra =[]
        self.nick = StringVar()
        

        # =========== Ver gramatica inicial sin aplicar recursion izquierda ============
        
        
        def Gramatica1():
            
            self.productions = [["S", "C C"], ["C", "a C"], ["C", "d"]]
            
            self.noTerminals=["S","C"]

            self.initial = "S"

            s = ttk.Style()
            s.theme_use('clam')

            # Configura los estilos de la cabecera de la tabla
            s.configure('Treeview.Heading', background="#ff6961")
            
            tree = ttk.Treeview(frame, column=("c1", "c2"),show='headings', height=15)
            tree.column("# 1", anchor=CENTER)
            tree.heading("# 1", text="No Terminal")
            tree.column("# 2", anchor=CENTER)
            tree.heading("# 2", text="Produccion")
           
            for item in self.productions:
                tree.insert('', "end", text="1", values=(item[0], [item[1]]))
                #tree.insert('', "end", text="1", values=(item))
            
            tree.place(x=0, y=5)

        # =========== Aumentar la Gramatica y sacar I-0 ============

        def PrepararGramaticaa():
            #self.result = PrepareProduction.PrepareProductionForLR(PrepareProduction(self.noTerminals, self.initial, self.productions))
            self.result = PrepararGramatica.asignarPunto(PrepararGramatica(self.noTerminals, self.initial, self.productions))
            s = ttk.Style()
            s.theme_use('clam')
            #print(self.result)
            # Configura los estilos de la cabecera de la tabla
            s.configure('Treeview.Heading', background="#77dd77")

            tree = ttk.Treeview(frame, column=("c1", "c2"),
                                show='headings', height=15)
            tree.column("# 1", anchor=CENTER)
            tree.heading("# 1", text="No Terminal")
            tree.column("# 2", anchor=CENTER)
            tree.heading("# 2", text="Produccion")
            self.newNoTerminals = []
            for res in self.result:
                if not self.newNoTerminals.__contains__(res[0]):
                    # Agrega a una nueva lista los nuevos NoTerminales
                    self.newNoTerminals.append(res[0])
                    # Values son las propiedades que se mostraran en la tabla
                tree.insert('', "end", text="1", values=(res[0], [res[1]]))
            tree.place(x=0, y=5)

        # =========== Realizar LR0 ============
        def RealizarLR1():
            LR = AnalizadorLR1(self.noTerminals, self.initial, self.result)
            iteraciones = []
            #print(self.result)
            rn = [*LR.analizadorLR1(self.result, iteraciones, [])]
            s = ttk.Style()
            s.theme_use('clam')
            #print(self.result)
            # Configura los estilos de la cabecera de la tabla
            s.configure('Treeview.Heading', background="#77dd77")
            self.e = LR.LoopArray()
            label1 = Label(frame,text="los estados son {0}".format(len(self.e)) )
            label1.place(x=10, y=290)
            print(rn)
            label = Label(frame,text=rn)
            label.place(x=10, y=260)
            


        def SacarTerminales():
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
        

        def returnElement():
            element = self.e.get(int(self.nick.get()))
            s = ttk.Style()
            s.theme_use('clam')

            # Configura los estilos de la cabecera de la tabla
            s.configure('Treeview.Heading', background="#ff6961")

            tree = ttk.Treeview(frame, column=("c1", "c2"),
                                show='headings', height=15)
            tree.column("# 1", anchor=CENTER)
            tree.heading("# 1", text="No Terminal")
            tree.column("# 2", anchor=CENTER)
            tree.heading("# 2", text="Produccion")
            print()
            for item in element:
                tree.insert('', "end", text="1", values=(item[0], [item[1]]))
            tree.place(x=0, y=5)
        
        def imprimirDiccionario():
            for c, v in self.e.items():
                print(c,v)

         
        # ================ Contenedor para los botones ================
        frameBtn = LabelFrame(self.window, text="Botones",
                              font=("Arial", 15), background="#5F9DF7")
        frameBtn.place(x=110, y=5, width=205, height=280)
        
        
        # ================ Contenedor para las tablas ================
        frame = LabelFrame(self.window, text="Tablas",
                           font=("Arial", 15), background="#5F9DF7")
        frame.place(x=10, y=290, width=408, height=360)
        

        # =========== Botones para manipular la interfaz ==============
        btn_font = font.Font(family="Roboto Cn", size=11)
        Button(frameBtn, text="Ver Gramatica", font=btn_font, background="#FFF7E9",
               command=Gramatica1).place(x=0, y=5, width=200, height=35)
        Button(frameBtn, text="Preparar Gramatica", font=btn_font, background="#FFF7E9",
               command=PrepararGramaticaa).place(x=0, y=45, width=200, height=35)
        Button(frameBtn, text="Sacar LR1", font=btn_font, background="#FFF7E9",
               command=RealizarLR1).place(x=0, y=85, width=200, height=35)
        
        insert_nick = Entry(frameBtn, width=20, textvariable=self.nick)
        insert_nick.place(x=0, y=120)

        boton_nick = Button(frameBtn, text="Ver estado", command=imprimirDiccionario)
        boton_nick.place(x=130, y=120)
        
        boton_nick = Button(frameBtn, text="Ver estado", command=returnElement)
        boton_nick.place(x=130, y=120)
        
if __name__ == "__main__":
    gui = Tk()
    gui.geometry("425x650")
    gui.configure(bg="#5F9DF7")
    app = GUI(gui)
    gui.mainloop()