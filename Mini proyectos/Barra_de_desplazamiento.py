import tkinter as tk
ventana = tk.Tk()
ventana.title ('Barra de desplazamiento')
ventana.geometry('400x200')
ventana.configure(bg="#060129")

marco = tk.Frame(
    ventana, 
    bg="#060129")
marco.pack(
    padx=10, 
    pady=10)

scrollbar = tk.Scrollbar(
    marco,
    troughcolor="#ab9ff7",
    bg="#723D00",
    activebackground="#a67ee5")
scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y)

#width y height en la Listbox controlan el tamaño en caracteres y filas.
lista = tk.Listbox (
    marco,
    yscrollcommand=scrollbar.set,
    width=50,
    height=15,
    bg="#ab9ff7",
    fg="#723D00",
    font=("Calibri", 10))
lista.configure(
    bg="#ab9ff7",
    fg="#723D00")
for i in range (100):
    lista.insert(tk.END, f'Ventana de contenido')
lista.pack(
    side=tk.LEFT,
    fill=tk.BOTH)
scrollbar.config(command=lista.yview)
ventana.mainloop()