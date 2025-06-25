import tkinter as tk
from tkinter import ttk
import time
import locale # Se necesita para los nombres de los meses en español

# Configura la localización a español para que time.strftime() use nombres de meses en español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    # Fallback para sistemas que no tienen 'es_ES.UTF-8' (ej. algunos Windows)
    # Puedes probar 'es_ES', 'Spanish_Spain.1252', 'esp'
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')
    except locale.Error:
        print("Advertencia: No se pudo configurar el idioma a español para los nombres de los meses.")


ventana = tk.Tk()
ventana.title('Diario de Hábitos')
ventana.geometry('800x400')
ventana.configure(bg="#333333") # Cambiado a un gris oscuro

# Etiquetas con colores y tamaños ajustados
reloj = tk.Label(ventana, font=('Arial', 24, 'bold'), fg='cyan', bg='#6C6F7D')
fecha = tk.Label(ventana, font=('Arial', 14), fg='lightgray', bg='#6C6F7D')

# --- Posicionamiento con place() ---
# Reloj: en la esquina superior derecha
reloj.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10) # x=-10 mueve 10px a la izquierda del borde derecho
# y=10 mueve 10px hacia abajo del borde superior

# Fecha: debajo del reloj, también alineada a la derecha
fecha.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=50) # y=50 es debajo del reloj (ajusta si es necesario)

def actualizar():
    ahora = time.localtime()
    hora_str = time.strftime('%H:%M:%S', ahora)

    # %d para el día, %B para el nombre completo del mes, %Y para el año
    # Añadimos " del " manualmente
    fecha_str = time.strftime('%d del %B %Y', ahora)
    
    # Asegúra de que el nombre del mes esté en minúsculas si lo deseas
    fecha_str = fecha_str.replace("del ", "del ").lower() # Esto asegura "del" no cambie mayuscula y el mes sea minúscula

    reloj.config(text=hora_str)
    fecha.config(text=fecha_str)
    
    # Llama a la función de nuevo después de 1 segundo
    ventana.after(1000, actualizar)

# ====== Menú desplegable ======
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

# --- Menú principal ---
menu_principal = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label='Menú', menu=menu_principal)

submenu_a = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label='Opciones', menu=submenu_a)
submenu_a.add_command(label='Ordenar')
submenu_a.add_command(label='Borrar todos los hábitos')
submenu_a.add_command(label='Salir')

# --- Menú de opciones de estadísticas ---
menu_estadisticas = tk.Menu(barra_menu, tearoff=0)
submenu_b = tk.Menu(menu_principal, tearoff=0)
barra_menu.add_cascade(label='Estadísticas', menu=submenu_b)
submenu_b.add_command(label='Mostrar todos los hábitos pendientes')
submenu_b.add_command(label='Mostrar todos los hábitos completados')

# --- Menú Acerca de ---
menu_acercaDe = tk.Menu(barra_menu, tearoff=0)
submenu_c = tk.Menu(menu_principal, tearoff=0)
barra_menu.add_cascade(label='Acerca de', menu=submenu_c)

# Inicia la actualización y el bucle principal de la ventana
actualizar()
ventana.mainloop()