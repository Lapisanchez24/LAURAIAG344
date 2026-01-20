# ui.py
# Capa de interfaz gráfica (Tkinter)

import tkinter as tk
from tkinter import filedialog, messagebox
from controller import procesar_instruccion


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Procesador Inteligente de Excel")
        self.root.geometry("500x300")

        self.ruta_excel = None

        # Botón seleccionar archivo
        self.btn_archivo = tk.Button(
            root, text="Seleccionar archivo Excel", command=self.seleccionar_excel
        )
        self.btn_archivo.pack(pady=10)

        self.lbl_archivo = tk.Label(root, text="Ningún archivo seleccionado")
        self.lbl_archivo.pack()

        # Instrucción
        tk.Label(root, text="Escriba una instrucción en Lenguaje Natural:").pack(pady=10)
        self.txt_instruccion = tk.Entry(root, width=50)
        self.txt_instruccion.pack()

        # Botón ejecutar
        self.btn_ejecutar = tk.Button(
            root, text="Ejecutar", command=self.ejecutar
        )
        self.btn_ejecutar.pack(pady=20)

    def seleccionar_excel(self):
        self.ruta_excel = filedialog.askopenfilename(
            title="Selecciona un archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx")]
        )

        if self.ruta_excel:
            self.lbl_archivo.config(text=self.ruta_excel)

    def ejecutar(self):
        if not self.ruta_excel:
            messagebox.showerror("Error", "Selecciona un archivo Excel")
            return

        texto = self.txt_instruccion.get()
        if not texto:
            messagebox.showerror("Error", "Escribe una instrucción")
            return

        ok, mensaje = procesar_instruccion(texto, self.ruta_excel)

        if ok:
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)


def iniciar_app():
    root = tk.Tk()
    App(root)
    root.mainloop()
