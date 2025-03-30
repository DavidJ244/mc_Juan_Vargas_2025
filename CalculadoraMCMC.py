import tkinter as tk
from tkinter import messagebox
import struct

def float_to_bin(num):
    return format(struct.unpack('!I', struct.pack('!f', num))[0], '032b')

def bin_to_float(binary):
    return struct.unpack('!f', struct.pack('!I', int(binary, 2)))[0]

def int_to_bin(num):
    return format(num & 0xFFFFFFFF, '032b')

def bin_to_int(binary):
    num = int(binary, 2)
    return num - 0x100000000 if num & 0x80000000 else num

def evaluar_expresion():
    expresion = entrada.get()
    try:
        resultado = eval(expresion)
        
        if isinstance(resultado, int):
            binario = int_to_bin(resultado)
        else:
            binario = float_to_bin(resultado)
        
        resultado_label.config(text=f"Binario: {binario}\nDecimal: {resultado}")
    except Exception as e:
        messagebox.showerror("Error", f"Expresión inválida: {str(e)}")

def iniciar_calculadora():
    inicio_frame.pack_forget()
    calculadora_frame.pack()

root = tk.Tk()
root.title("Calculadora Binaria")
root.geometry("400x300")
root.configure(bg="#FFC0CB")

inicio_frame = tk.Frame(root, bg="#FFC0CB")
tk.Label(inicio_frame, text="Bienvenido a la Calculadora Binaria", font=("Arial", 14), bg="#FFC0CB").pack(pady=20)
tk.Button(inicio_frame, text="Iniciar", command=iniciar_calculadora, font=("Arial", 12), bg="#FF69B4", fg="white").pack()
inicio_frame.pack()

calculadora_frame = tk.Frame(root, bg="#FFC0CB")
tk.Label(calculadora_frame, text="Ingrese una expresión:", bg="#FFC0CB").pack()
entrada = tk.Entry(calculadora_frame, width=30)
entrada.pack()

tk.Button(calculadora_frame, text="Calcular", command=evaluar_expresion, bg="#FF69B4", fg="white").pack(pady=5)

resultado_label = tk.Label(calculadora_frame, text="Resultado en binario y decimal aparecerá aquí", bg="#FFC0CB")
resultado_label.pack()

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
archivo_menu = tk.Menu(menu_bar, tearoff=0)
archivo_menu.add_command(label="Salir", command=root.quit)
menu_bar.add_cascade(label="Archivo", menu=archivo_menu)

root.mainloop()
