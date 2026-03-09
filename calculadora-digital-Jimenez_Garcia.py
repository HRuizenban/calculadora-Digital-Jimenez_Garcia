import tkinter as tk
from tkinter import messagebox
import json
import os
import csv
import pystray
from PIL import Image, ImageDraw
import threading
import keyboard

HISTORIAL_FILE = "historial.json"

# -----------
# HISTORIAL
# -----------

def cargar_historial():
    if os.path.exists(HISTORIAL_FILE):
        try:
            with open(HISTORIAL_FILE, "r") as f:
                data = f.read().strip()
                if data == "":
                    return []
                return json.loads(data)
        except:
            return []
    return []

def guardar_historial():
    with open(HISTORIAL_FILE, "w") as f:
        json.dump(historial, f)

historial = cargar_historial()

def agregar_historial(texto):
    historial.append(texto)
    if len(historial) > 10:
        historial.pop(0)

# -------------
# CALCULADORA
# -------------

expresion = ""

# Operaciones requeridas por el proyecto

def sumar(a,b):
    return a+b

def restar(a,b):
    return a-b

def multiplicar(a,b):
    return a*b

def dividir(a,b):
    if b == 0:
        return "Error división por 0"
    return a/b

def modulo(a,b):
    return a%b

def potencia(a,b):
    return a**b


def presionar(valor):
    global expresion
    expresion += str(valor)
    entrada.set(expresion)

def limpiar():
    global expresion
    expresion = ""
    entrada.set("")

def calcular():

    global expresion

    try:

        operadores = ["+","-","*","/","%","^"]

        for op in operadores:

            if op in expresion:

                partes = expresion.split(op)

                if len(partes) != 2:
                    raise ValueError

                a = float(partes[0])
                b = float(partes[1])

                if op == "+":
                    resultado_calc = sumar(a,b)

                elif op == "-":
                    resultado_calc = restar(a,b)

                elif op == "*":
                    resultado_calc = multiplicar(a,b)

                elif op == "/":
                    resultado_calc = dividir(a,b)

                elif op == "%":
                    resultado_calc = modulo(a,b)

                elif op == "^":
                    resultado_calc = potencia(a,b)

                entrada.set(str(resultado_calc))

                agregar_historial(f"{a} {op} {b} = {resultado_calc}")

                expresion = str(resultado_calc)

                return

    except:

        messagebox.showerror("Error","Operación inválida")
        limpiar()

# -----------
# CONVERSION
# -------------

def bytes_a_kb():
    valor=float(conv_entry.get())
    resultado.set(f"{valor} Bytes = {valor/1024} KB")

def kb_a_mb():
    valor=float(conv_entry.get())
    resultado.set(f"{valor} KB = {valor/1024} MB")

def mb_a_gb():
    valor=float(conv_entry.get())
    resultado.set(f"{valor} MB = {valor/1024} GB")

# ----------
# BIN, HEX,DEC
# ----------

def decimal_binario():
    valor=int(conv_entry.get())
    resultado.set(f"Binario: {bin(valor)[2:]}")

def decimal_hex():
    valor=int(conv_entry.get())
    resultado.set(f"Hexadecimal: {hex(valor)[2:]}")

def binario_decimal():
    valor=conv_entry.get()
    resultado.set(f"Decimal: {int(valor,2)}")

# -----------
# HISTORIAL
# -----------

def mostrar_historial():

    ventana=tk.Toplevel(root)
    ventana.title("Historial")
    ventana.geometry("350x300")

    texto=tk.Text(ventana,width=40,height=15)
    texto.pack()

    if not historial:
        texto.insert(tk.END,"No hay operaciones aún\n")
    else:
        for h in historial:
            texto.insert(tk.END,h+"\n")

# ---------
# CSV
# ----------

def exportar_csv():

    with open("historial.csv","w",newline="") as f:

        writer=csv.writer(f)

        writer.writerow(["Operacion"])

        for h in historial:
            writer.writerow([h])

    messagebox.showinfo("Exportado","Historial exportado a historial.csv")

# -------------
# MINIMIZAR
# -------------

def crear_imagen():
    image=Image.new('RGB',(64,64),"white")
    draw=ImageDraw.Draw(image)
    draw.rectangle((16,16,48,48),fill="black")
    return image

def mostrar_ventana(icon=None,item=None):
    root.after(0,root.deiconify)
    root.after(0,root.lift)

def cerrar_app(icon=None,item=None):
    guardar_historial()
    try:
        icon.stop()
    except:
        pass
    root.destroy()
    os._exit(0)

def tray_icon():

    icon=pystray.Icon(
        "Calculadora",
        crear_imagen(),
        "Calculadora",
        menu=pystray.Menu(
            pystray.MenuItem("Abrir",mostrar_ventana),
            pystray.MenuItem("Salir",cerrar_app)
        )
    )

    icon.run()

# -----------------
# Tracker Lost ark
# -----------------

def toggle_window():

    if root.state()=="withdrawn":
        root.deiconify()
        root.lift()
    else:
        root.withdraw()

keyboard.add_hotkey("ctrl+right",toggle_window)

# ----
# UI
# ----

root=tk.Tk()
root.title("Calculadora Multifuncional")
root.geometry("380x560")
root.resizable(False,False)

def minimizar():
    root.withdraw()

root.protocol("WM_DELETE_WINDOW",minimizar)

entrada=tk.StringVar()
resultado=tk.StringVar()

pantalla=tk.Entry(root,textvariable=entrada,font=("Arial",20),justify="right")
pantalla.pack(fill="both",padx=10,pady=10)

# -------
# BOTONES
# --------

frame=tk.Frame(root)
frame.pack()

botones=[
("7","8","9","/"),
("4","5","6","*"),
("1","2","3","-"),
("0",".","%","+"),
("^","=","C","")
]

for fila in botones:

    f=tk.Frame(frame)
    f.pack()

    for b in fila:

        if b=="=":
            tk.Button(f,text=b,width=8,height=2,command=calcular).pack(side="left")

        elif b=="C":
            tk.Button(f,text=b,width=8,height=2,command=limpiar).pack(side="left")

        elif b!="":
            tk.Button(f,text=b,width=8,height=2,command=lambda x=b:presionar(x)).pack(side="left")

# -------------------
# CONVERSIONES BOT
# -------------------

tk.Label(root,text="Conversiones de Datos").pack()

conv_entry=tk.Entry(root)
conv_entry.pack()

tk.Button(root,text="Bytes → KB",command=bytes_a_kb).pack()
tk.Button(root,text="KB → MB",command=kb_a_mb).pack()
tk.Button(root,text="MB → GB",command=mb_a_gb).pack()

# ----------------
# DEC,HEX,BIN BOT
# ----------------

tk.Label(root,text="Sistemas Numéricos").pack()

tk.Button(root,text="Decimal → Binario",command=decimal_binario).pack()
tk.Button(root,text="Decimal → Hex",command=decimal_hex).pack()
tk.Button(root,text="Binario → Decimal",command=binario_decimal).pack()

# -------------
# RESPUESTA
# ------------

tk.Label(root,textvariable=resultado,font=("Arial",12)).pack(pady=5)

# ---------------
# HISTORIAL BOT
# ---------------

tk.Button(root,text="Ver Historial",command=mostrar_historial).pack(pady=4)

tk.Button(root,text="Exportar Historial CSV",command=exportar_csv).pack(pady=4)

# --------
# Kilñl
# --------

tk.Button(
root,
text="SALIR",
bg="red",
fg="white",
font=("Arial",12,"bold"),
command=cerrar_app
).pack(pady=10)

# --------
# TRAY
# --------

tray_thread=threading.Thread(target=tray_icon,daemon=True)
tray_thread.start()

root.mainloop()