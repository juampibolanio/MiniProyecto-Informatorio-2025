import tkinter as tk

ventana = tk.Tk()
ventana.title('Lista de tareas')
ventana.geometry('400x300')
ventana.configure(bg='#4F5A4A')

ingreso_tarea = tk.Entry(
    ventana, 
    bg="#7EF480", 
    fg="#000000",
    font=("Calibri", 10))
ingreso_tarea.pack(pady=10, ipadx=30) 

def agregar_tarea():
    tarea = ingreso_tarea.get()
    if tarea:
        lista_tareas.insert(tk.END, tarea)
        ingreso_tarea.delete(0, tk.END)

boton_agregar = tk.Button(
    ventana,
    text='Agregar tarea',
    command=agregar_tarea,
    bg='#28a745',
    fg='#000000',
    font=('Calibri', 10, 'bold'))
boton_agregar.pack(pady=5)

def eliminar_tarea():
    seleccion = lista_tareas.curselection()
    if seleccion:
        lista_tareas.delete(seleccion)

lista_tareas = tk.Listbox(ventana, 
    bg='#7EF480', 
    fg="#000000",
    font=('Calibri', 10),
    width=40)
lista_tareas.pack(pady=10)

boton_eliminar = tk.Button(
    ventana, 
    text = 'Eliminar tarea', 
    command = eliminar_tarea, 
    bg="#620101",
    fg="#FFFFFF",
    font=('Calibri', 10, 'bold'))
boton_eliminar.pack(pady=10)

ventana.mainloop()