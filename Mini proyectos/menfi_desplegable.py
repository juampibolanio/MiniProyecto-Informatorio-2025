import tkinter as tk

ventana = tk.Tk()
ventana.title('Menú desplegable')
ventana.geometry('400x200')
ventana.configure(bg="#3b0101")

# =====> Barra de menú <=====
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu_principal = tk.Menu(barra_menu)
barra_menu.add_cascade(label='Principal', menu=menu_principal)

submenu = tk.Menu(menu_principal)
menu_principal.add_cascade(label='Opciones', menu=submenu)
submenu.add_command(label='Archivos')
submenu.add_command(label='Info')

# =====> Título + Información personal <=====
titulo_label = tk.Label(
    ventana,
    text="Hola Profe!",
    font=("Calibri", 14, "bold"),
    bg="#3b0101",
    fg="white",
    anchor="w"
)
titulo_label.pack(padx=10, pady=(10, 0), anchor="w")

info_label = tk.Label(
    ventana,
    text="😎 Desarrollado por Hernán Di Gialonardo\n📧 hernandigialonardo@gmail.com\n⚡ Versión 1.0",
    font=("Calibri", 10),
    bg="#3b0101",
    fg="white",
    justify="left",
    anchor="w"
)
info_label.pack(padx=10, pady=(0, 10), anchor="w")

ventana.mainloop()