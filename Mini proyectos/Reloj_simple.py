import tkinter as tk
import time
import locale

ventana = tk.Tk()
ventana.title('Reloj simple')
ventana.geometry('400x200')
ventana.configure(bg="#280111")

# =====> Localización en español <=====
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')
    except locale.Error:
        print("Advertencia: No se pudo configurar el idioma a español para los nombres de los meses.")

# =====> Reloj y Fecha centrados sin llenar la ventana <=====
reloj = tk.Label(
    ventana, 
    font=('Courier New', 40, 'bold'),  # tamaño ajustado
    fg="#000000", 
    bg="#66002B",
    padx=20,
    pady=10
)
reloj.pack(anchor='center', pady=(30, 5))  # centrado sin ocupar toda la ventana

fecha = tk.Label(
    ventana, 
    font=('Courier New', 14, 'underline'),
    fg="white", 
    bg="#66002B",
    padx=10,
    pady=5
)
fecha.pack(anchor='center')

# =====> Función de actualización <=====
def actualizar():
    ahora = time.localtime()
    hora_str = time.strftime('%H:%M:%S', ahora)
    fecha_str = time.strftime('%d de %B %Y', ahora).lower()
    reloj.config(text=hora_str)
    fecha.config(text=fecha_str)
    ventana.after(1000, actualizar)

actualizar()
ventana.mainloop()
