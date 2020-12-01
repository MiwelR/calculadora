from tkinter import *
from tkinter import ttk

WIDTH = 68
HEIGHT = 50

dbotones = [
    {
        'text': 'C',
        'r': 0,
        'c': 1,
    },
    {
        'text': '+/-',
        'r': 0,
        'c': 2,
    },
    {
        'text': '÷',
        'r': 0,
        'c': 3,
    },
    {
        'text': '7',
        'r': 1,
        'c': 0,
    },
    {
        'text': '8',
        'r': 1,
        'c': 1,
    },
    {
        'text': '9',
        'r': 1,
        'c': 2,
    },
    {
        'text': 'x',
        'r': 1,
        'c': 3,
    },
    {
        'text': '4',
        'r': 2,
        'c': 0,
    },
    {
        'text': '5',
        'r': 2,
        'c': 1,
    },
    {
        'text': '6',
        'r': 2,
        'c': 2,
    },
    {
        'text': '-',
        'r': 2,
        'c': 3,
    },
    {
        'text': '1',
        'r': 3,
        'c': 0,
    },
    {
        'text': '2',
        'r': 3,
        'c': 1,
    },
    {
        'text': '3',
        'r': 3,
        'c': 2,
    },
    {
        'text': '+',
        'r': 3,
        'c': 3,
    },
    {
        'text':'0',
        'r':4,
        'c':0,
        'w': 2
    },
    {
        'text': ',',
        'r': 4,
        'c': 2,
    },
    {
        'text': '=',
        'r': 4,
        'c': 3,
    },
]

class Display(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, width=WIDTH*4, height=HEIGHT)
        self.pack_propagate(0)
        s = ttk.Style()
        s.theme_use('alt')

        self.label = ttk.Label(self, text="0", anchor=E, background='#2d3037', foreground='white', font='Helvetica 36')
        self.label.pack(side=TOP, fill=BOTH, expand=True)

    def refresh(self, texto):
        self.label.config(text=texto)

class CalcButton(ttk.Frame):
    def __init__(self, parent, text, style=None, command=None, width=1, height=1):
        ttk.Frame.__init__(self, parent, width=WIDTH*width, height=HEIGHT*height)
        self.pack_propagate(0)
        s = ttk.Style()
        s.theme_use('alt')

        ttk.Button(self, text=text, style=style, command=lambda: command(text) ).pack(side=TOP, fill=BOTH, expand=True)



class Keyboard(ttk.Frame):
    def __init__(self, parent, command):
        ttk.Frame.__init__(self, parent, width=WIDTH*4, height=HEIGHT*5)
        self.pack_propagate(0)
        s = ttk.Style()
        s.theme_use('alt')
        # Configuración del estilo de botones:
        s.configure('num.TButton', background='#606268', foreground='white', font=('Helvetica', 24), highlightcolor='black')
        s.map('num.TButton', 
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', '!focus', 'cyan'), ('active', 'grey')])
        s.configure('op.TButton', background='#ff9f0a', foreground='white', font=('Helvetica', 24))
        s.map('op.TButton', 
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', '!focus', 'cyan'), ('active', '#a36607')])
        s.configure('ot.TButton', background='#42434a', foreground='white', font=('Helvetica', 24))
        s.map('ot.TButton', 
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', '!focus', 'cyan'), ('active', '#313237')])

        for boton in dbotones:
            w = boton.get('w', 1)
            h = boton.get('h', 1)
            # Aplicación de estilos personalizados a botones:
            if boton['text'] in ('0123456789,'):
                btn = CalcButton(self, boton['text'], style='num.TButton', width=w, height=h, command=command)
                btn.grid(row=boton['r'], column=boton['c'], columnspan=w, rowspan=h)
            elif boton['text'] in ('+-÷x='):
                btn = CalcButton(self, boton['text'], style='op.TButton', width=w, height=h, command=command)
                btn.grid(row=boton['r'], column=boton['c'], columnspan=w, rowspan=h)
            else:
                btn = CalcButton(self, boton['text'], style='ot.TButton', width=w, height=h, command=command)
                btn.grid(row=boton['r'], column=boton['c'], columnspan=w, rowspan=h)




class Calculator(ttk.Frame):
    valor1 = None
    valor2 = None
    r = None
    operador = ''
    cadena = ''
    operaciones = ''

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, width=WIDTH*4, height=HEIGHT*7)
        self.pack_propagate(0)
        s = ttk.Style()
        s.theme_use('alt')

        self.displayT = Display(self)
        self.displayT.label.config(text='', font='Helvetica 12')
        self.displayT.pack(side=TOP, fill=BOTH, expand=True)

        self.display = Display(self)
        self.display.pack(side=TOP, fill=BOTH, expand=True)

        self.teclado = Keyboard(self, self.gestiona_calculos)
        self.teclado.pack(side=TOP)

    def gestiona_calculos(self, tecla):

        if tecla.isdigit() != 0:
            if not (self.cadena == '' and tecla == '0'):
                self.cadena += tecla
                self.display.refresh(self.cadena)
        elif tecla in ('+', '-', 'x', '÷'):
            self.operador = tecla
            if (self.valor1 and self.cadena) and float(self.valor1) == True:
                self.valor2 = float(self.cadena)
                self.r = self.calculate()
                self.display.refresh(self.r)
                self.valor1 = self.r
                self.operaciones += (self.cadena) + (f" {self.operador} ")
                self.displayT.refresh(self.operaciones)#
                self.cadena = ''
                self.operador = ''

            elif self.valor1 and (self.cadena == ''):
                self.operaciones += self.operador #
                self.displayT.refresh(self.operaciones)

            elif not self.valor1 or (self.cadena != self.valor1):
                self.valor1 = float(self.cadena)
                self.cadena = ''
                self.operaciones += str(self.valor1) + (f" {self.operador} ") #
                self.displayT.refresh(self.operaciones)
            else:
                self.valor2 = float(self.cadena)
                self.r = self.calculate()
                self.display.refresh(self.r)
                self.valor1 = self.r
                self.operador = ''
            self.cadena = ''
        elif tecla == ',':
            if '.' not in self.cadena:
                if not (self.cadena or self.valor1):
                    self.cadena += '0.'
                    self.valor1 = self.cadena
                    self.display.refresh(self.cadena)
                elif not self.cadena and self.valor1:
                    self.cadena += '0.'
                    self.valor2 = self.cadena
                    self.display.refresh(self.cadena)
                elif self.valor1:
                    self.cadena += '.'
                    self.valor2 = self.cadena
                    self.display.refresh(self.cadena)
                else:
                    self.cadena += '.'
                    self.valor1 = self.cadena
                    self.display.refresh(self.cadena)
        elif tecla == '=':
            if not self.cadena:
                    return 
            self.valor2 = float(self.cadena)
            self.r = self.calculate()
            self.display.refresh(self.r)
            self.valor1 = self.r
            self.operaciones += tecla
            self.displayT.refresh(self.operaciones)#
            self.cadena = ''
            self.operador = ''
        elif tecla == 'C':
            self.valor1 = None
            self.valor2 = None
            self.r = None
            self.operador = ''
            self.cadena = ''
            self.operaciones = ''
            self.displayT.refresh('')
            self.display.refresh('0')


    def calculate(self):

        if self.operador == '+':
            return round((self.valor1 + self.valor2), 6)
        elif self.operador == '-':
            return round((self.valor1 - self.valor2), 6)
        elif self.operador == 'x':
            return round((self.valor1 * self.valor2), 6)
        elif self.operador == '÷':
            return round((self.valor1 / self.valor2), 6)
        else:
            pass



# Keyboard - Otra forma de realizarlo:
'''
class Keyboard(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, width=WIDTH*4, height=HEIGHT*5)
        self.pack_propagate(0)
        s = ttk.Style()
        s.theme_use('alt')

        coordenadas = []
        for fila in range(5):
            for columna in range(4):
                coordenadas.append((fila, columna))

        k = 0
        valorAnt = ''
        for tecla in botones:
            if valorAnt == tecla:
                boton = CalcButton(self, tecla, width=2)
                boton.grid(row=coordenadas[k][0], column=coordenadas[k-1][1], columnspan=2)
            else:
                boton = CalcButton(self, tecla)
                boton.grid(row=coordenadas[k][0], column=coordenadas[k][1])
            valorAnt = tecla
            k += 1
'''