import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RegresionPolinomial:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def matriz_vandermonde(self, grado):
        return [[xi**p for p in range(grado+1)] for xi in self.x]

    def resolver_sistema(self, A, b):
        n = len(b)
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0]*n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j]*x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def ajustar(self, grado):
        V = self.matriz_vandermonde(grado)
        Vt = list(zip(*V))
        VtV = [[sum(Vt[i][k]*V[k][j] for k in range(len(V))) for j in range(grado+1)] for i in range(grado+1)]
        Vty = [sum(Vt[i][k]*self.y[k] for k in range(len(V))) for i in range(grado+1)]
        coef = self.resolver_sistema(VtV, Vty)
        return coef

    def predecir(self, coef, xi):
        return sum(coef[i] * xi**i for i in range(len(coef)))

    def calcular_r2(self, coef):
        y_prom = sum(self.y) / len(self.y)
        st = sum((yi - y_prom)**2 for yi in self.y)
        sr = sum((yi - self.predecir(coef, self.x[i]))**2 for i, yi in enumerate(self.y))
        return 1 - sr / st if st != 0 else 0

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Regresión Polinomial Dinámica por Grado")

        self.entrada = tk.Text(root, height=10, width=40)
        self.entrada.pack()

        self.boton = tk.Button(root, text="Procesar", command=self.procesar)
        self.boton.pack()

        self.info = tk.Label(root, text="Ingrese puntos como: x1,y1 x2,y2 ...")
        self.info.pack()

        self.selector = tk.StringVar(root)
        self.selector.trace_add("write", self.mostrar_grafico)
        self.selector_menu = tk.OptionMenu(root, self.selector, "")
        self.selector_menu.pack()

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        self.modelos = {}
        self.x_vals = []
        self.y_vals = []

    def procesar(self):
        texto = self.entrada.get("1.0", tk.END).strip()
        try:
            pares = [tuple(map(float, par.split(","))) for par in texto.split()]
            if len(pares) < 6:
                raise ValueError("Mínimo 6 puntos")
            x, y = zip(*pares)
        except:
            messagebox.showerror("Error", "Entrada inválida. Formato: x1,y1 x2,y2 ...")
            return

        self.modelos = {}
        self.x_vals, self.y_vals = x, y
        modelo = RegresionPolinomial(x, y)
        grado = 1
        r2 = 0
        while r2 < 0.95 and grado <= len(x) - 1:
            coef = modelo.ajustar(grado)
            r2 = modelo.calcular_r2(coef)
            self.modelos[grado] = (coef, r2)
            grado += 1

        # Actualizar el menú desplegable
        menu = self.selector_menu["menu"]
        menu.delete(0, "end")
        for g in self.modelos:
            menu.add_command(label=f"Grado {g}", command=lambda value=g: self.selector.set(f"Grado {value}"))
        self.selector.set(f"Grado {min(self.modelos)}")

    def mostrar_grafico(self, *args):
        if not self.modelos or not self.selector.get():
            return
        grado_texto = self.selector.get()
        grado = int(grado_texto.replace("Grado ", ""))

        coef, r2 = self.modelos[grado]
        modelo = RegresionPolinomial(self.x_vals, self.y_vals)
        self.ax.clear()
        self.ax.scatter(self.x_vals, self.y_vals, color='blue', label='Datos')

        x_pred = [min(self.x_vals) + i*(max(self.x_vals)-min(self.x_vals))/200 for i in range(201)]
        y_pred = [modelo.predecir(coef, xi) for xi in x_pred]

        self.ax.plot(x_pred, y_pred, label=f'Grado {grado} ($R^2$={r2:.3f})', color='red')
        self.ax.legend()
        self.ax.set_title(f"Curva de grado {grado}")
        self.canvas.draw()

if __name__ == '__main__':
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
