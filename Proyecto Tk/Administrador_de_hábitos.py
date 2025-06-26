import tkinter as tk
from tkinter import messagebox
import time
import locale
import os
from tkcalendar import Calendar
from datetime import datetime
import json
import os

# =====> Localización en español <=====
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')
    except locale.Error:
        print("Advertencia: No se pudo configurar el idioma a español " \
        "para los nombres de los meses.")

# =====> Ventana principal <=====
ventana = tk.Tk()
ventana.title('Administrador de hábitos')
ventana.geometry('700x400')
ventana.configure(bg="#190247")
tareas_por_fecha = {}

# =====> Ventana de reloj y fecha <=====
reloj = tk.Label(
    ventana, 
    font=('Calibri', 24, 'bold'),
    fg="#034384", 
    bg="#190247")
fecha = tk.Label(
    ventana, 
    font=('Calibri', 14, 'underline'),
    fg="white", 
    bg="#190247")

reloj.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
fecha.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=50)

# =====> Funciones del reloj <=====
def actualizar():
    ahora = time.localtime()
    hora_str = time.strftime('%H:%M:%S', ahora)
    fecha_str = time.strftime('%d de %B %Y', ahora).lower()
    reloj.config(text=hora_str)
    fecha.config(text=fecha_str)
    ventana.after(1000, actualizar)

reloj_visible = True  # Variable global para controlar visibilidad

# =====> Función de visibilidad del reloj <=====
def toggle_reloj():
    global reloj_visible
    if reloj_visible:
        reloj.place_forget()
        fecha.place_forget()
    else:
        reloj.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
        fecha.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=50)
    reloj_visible = not reloj_visible

# =====> Barra para y opciones del menú desplegable <=====
barra_menu = tk.Menu(
    ventana, 
    bg="#FFFFFF", 
    fg='black',
    activebackground="#0B048A", 
    activeforeground="white")

menu_principal = tk.Menu(
    barra_menu, 
    tearoff=0, 
    bg="#FFFFFF",
    fg='black', 
    activebackground="#0B048A", 
    activeforeground="white")

barra_menu.add_cascade(label='Menú', menu=menu_principal)

submenu = tk.Menu(
    menu_principal, 
    tearoff=0, 
    bg="#FFFFFF", 
    fg='black',
    activebackground="#0B048A", 
    activeforeground="white")

menu_principal.add_cascade(label='Opciones', menu=submenu)

# =====> Funciones de guardar y cargar <=====
def guardar_tareas():
    try:
        with open("tareas.json", "w", encoding="utf-8") as archivo:
            json.dump(tareas_por_fecha, archivo, ensure_ascii=False, indent=4)
        messagebox.showinfo("Guardar", "Tareas guardadas correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")

def cargar_tareas():
    global tareas_por_fecha
    if os.path.exists("tareas.json"):
        try:
            with open("tareas.json", "r", encoding="utf-8") as archivo:
                tareas_por_fecha = json.load(archivo)
            fecha_actual = calendario.get_date()
            mostrar_tareas_para_fecha(fecha_actual)
            mostrar_resumen_diario(fecha_actual)
            messagebox.showinfo("Cargar", "Tareas cargadas correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar: {e}")
    else:
        messagebox.showinfo("Cargar", "No se encontró archivo de tareas.")

# =====> Funciones ordenar y eliminar hábitos <=====
def ordenar_habitos():
    fecha_sel = calendario.get_date()
    if fecha_sel in tareas_por_fecha:
        tareas_por_fecha[fecha_sel].sort(key=lambda t: t.strip("✅ ").lower())
        mostrar_tareas_para_fecha(fecha_sel)

def borrar_todos_los_habitos():
    if messagebox.askyesno("Confirmar", "¿Estás seguro que querés borrar *TODOS* los hábitos?"):
        tareas_por_fecha.clear()
        lista_tareas.delete(0, tk.END)
        mostrar_resumen_diario(calendario.get_date())

# =====> Funciones acerca de: y estadísticas <=====
def mostrar_acerca_de():
    messagebox.showinfo("Acerca de", "Administrador de Hábitos\nCreado por el Grupo 2 del Informatorio™\nVersión 2.0 - 2025")

def mostrar_estadisticas():
    if not tareas_por_fecha:
        messagebox.showinfo("Estadísticas", "No hay tareas registradas aún.")
        return
    total_tareas = 0
    total_completadas = 0
    productividad_por_dia = {}
    for fecha, tareas in tareas_por_fecha.items():
        total_tareas += len(tareas)
        completadas = sum(1 for t in tareas if t.startswith("✅ "))
        total_completadas += completadas
        productividad_por_dia[fecha] = completadas
    porcentaje = (total_completadas / total_tareas) * 100 if total_tareas > 0 else 0
    dias_productivos = [f for f, c in productividad_por_dia.items() if c == max(productividad_por_dia.values())]
    ventana_estadisticas = tk.Toplevel(ventana)
    ventana_estadisticas.title("Estadísticas")
    ventana_estadisticas.geometry("400x250")
    ventana_estadisticas.configure(bg="#1C1C3A")
    tk.Label(ventana_estadisticas, text=f'📋 Total de tareas: {total_tareas}',
            bg="#1C1C3A", fg="white", font=('Calibri', 11)).pack(pady=5)
    tk.Label(ventana_estadisticas, text=f"✅ Tareas completadas: {total_completadas}",
            bg="#1C1C3A", fg="lightgreen", font=('Calibri', 11)).pack(pady=5)
    
    tk.Label(ventana_estadisticas, text=f"📈 Porcentaje cumplido: {porcentaje:.1f}%",
            bg="#1C1C3A", fg="skyblue", font=('Calibri', 11, "bold")).pack(pady=5)
    
    tk.Label(ventana_estadisticas, text="🏆 Día(s) más productivo(s):",
            bg="#1C1C3A", fg="gold", font=('Calibri', 11)).pack(pady=5)
    for dia in dias_productivos:
        tk.Label(ventana_estadisticas, text=f"• {dia}",
                bg="#1C1C3A", fg="white", font=('Calibri', 10)).pack()

# =====> Comandos del menú <=====
submenu.add_command(label='Guardar tareas', command=guardar_tareas)
submenu.add_command(label='Cargar tareas', command=cargar_tareas)  
submenu.add_command(label='Ver estadísticas', command=mostrar_estadisticas)
menu_principal.add_command(label='Ordenar hábitos (A-Z)', command=ordenar_habitos)
menu_principal.add_command(label='Borrar todos los hábitos', command=borrar_todos_los_habitos)
menu_principal.add_command(label='Mostrar/Ocultar reloj', command=toggle_reloj)
menu_principal.add_separator()
menu_principal.add_command(label='Acerca de', command=mostrar_acerca_de)
menu_principal.add_separator()
menu_principal.add_command(label='Salir', command=lambda: confirmar_salida())

ventana.config(menu=barra_menu)

frame_entrada = tk.Frame(ventana, bg="#034384")
frame_entrada.pack(anchor="w", padx=10, pady=10)

entrada_tarea = tk.Entry(
    frame_entrada, 
    width=30, 
    font=('Courier New', 10),
    bg="#8595F9", 
    fg="black", 
    insertbackground="black")
entrada_tarea.pack(side=tk.LEFT, padx=5)

# =====> Función agregar y mostrar tarea <=====
def agregar_tarea():
    tarea = entrada_tarea.get().strip()
    if tarea:
        fecha_sel = calendario.get_date()
        if fecha_sel not in tareas_por_fecha:
            tareas_por_fecha[fecha_sel] = []
        if tarea not in tareas_por_fecha[fecha_sel]:
            tareas_por_fecha[fecha_sel].append(tarea)
            entrada_tarea.delete(0, tk.END)
            mostrar_tareas_para_fecha(fecha_sel)

def mostrar_tareas_para_fecha(fecha):
    lista_tareas.delete(0, tk.END)
    if fecha in tareas_por_fecha:
        for tarea in tareas_por_fecha[fecha]:
            lista_tareas.insert(tk.END, tarea)
    mostrar_resumen_diario(fecha)
entrada_tarea.bind("<Return>", lambda event: agregar_tarea())

# =====> Botón agregar <=====
boton_agregar = tk.Button(
    frame_entrada, 
    text='Agregar', 
    command=agregar_tarea,       
    bg="#17611D", 
    fg="white", 
    font=('Calibri', 9, "bold"))
boton_agregar.pack(side=tk.LEFT)

frame_lista = tk.Frame(ventana, bg='#333333')
frame_lista.place(x=10, y=100, width=300, height=230) 

# =====> Acá intentamos que el scroll tenga otra apariencia <=====
scrollbar = tk.Scrollbar(
    frame_lista,
    troughcolor="#034384", 
    bg="#555555",
    activebackground="#777777", 
    highlightbackground="#333333")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_tareas = tk.Listbox(
    frame_lista, 
    yscrollcommand=scrollbar.set,
    height=12,  
    bg="#8595F9", 
    fg="black",
    selectbackground="#370188", 
    selectforeground="white",
    highlightbackground="#FFFFFF",
    font=('Courier New', 10)
)

lista_tareas.config(font=('Courier New', 10))
lista_tareas.bind('<<ListboxSelect>>', lambda e: actualizar_texto_boton())
lista_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=lista_tareas.yview)

# =====> Función marcar y desmarcar como hecho <=====
def actualizar_texto_boton(event=None):
    seleccion = lista_tareas.curselection()
    if seleccion:
        texto = lista_tareas.get(seleccion[0])
        if texto.startswith('✅ '):
            boton_alternar.config(
                text='Desmarcar',
                bg='red',
                fg='white',
                font=('Calibri', 9, 'bold')
            )
        else:
            boton_alternar.config(
                text='Marcar como hecho',
                bg='green',
                fg='white',
                font=('Calibri', 9, 'bold')
            )

# =====> Función de tareas hechas por fecha <=====
def alternar_estado():
    seleccion = lista_tareas.curselection()
    if seleccion:
        indice = seleccion[0]
        fecha_sel = calendario.get_date()
        if fecha_sel in tareas_por_fecha:
            texto = tareas_por_fecha[fecha_sel][indice]
            if texto.startswith("✅ "):
                nuevo_texto = texto[2:]
                tareas_por_fecha[fecha_sel][indice] = nuevo_texto
                lista_tareas.itemconfig(indice, {'fg': 'red'})
            else:
                nuevo_texto = f"✅ {texto}"
                tareas_por_fecha[fecha_sel][indice] = nuevo_texto
                lista_tareas.itemconfig(indice, {'fg': 'green'})
            mostrar_tareas_para_fecha(fecha_sel)
            actualizar_texto_boton()

# =====> Función eliminar tarea <=====
def eliminar_tarea():
    seleccion = lista_tareas.curselection()
    if seleccion:
        indice = seleccion[0]
        fecha_sel = calendario.get_date()
        if fecha_sel in tareas_por_fecha:
            del tareas_por_fecha[fecha_sel][indice]
            if not tareas_por_fecha[fecha_sel]:
                del tareas_por_fecha[fecha_sel]
            mostrar_tareas_para_fecha(fecha_sel)

# =====> Botón marcar y desmarcar como hecho <=====
boton_alternar = tk.Button(
    ventana, 
    text='Marcar hecho',
    command=alternar_estado, 
    bg="#FFFFFF", 
    fg="black", 
    font=('Calibri', 9, 'bold'))
boton_alternar.place(x=160, y=350)

# =====> Botón eliminar <=====
boton_eliminar = tk.Button(
    ventana, 
    text='Eliminar tarea',
    command=eliminar_tarea, 
    bg="#460101", 
    fg="white",
    font=('Calibri', 9, 'bold'))
boton_eliminar.place(x=10, y=350)

# =====> Frame para el calendario <=====
frame_calendario = tk.Frame(ventana, bg="#190247")
frame_calendario.place(x=330, y=100)
calendario = Calendar(
    frame_calendario,
    selectmode='day',
    year=datetime.now().year,
    month=datetime.now().month,
    day=datetime.now().day,
    locale='es_ES', 
    background='#370188',
    foreground='white',
    headersbackground='#034384',
    headersforeground='white',
    selectbackground='#17611D',
    selectforeground='white'
)
calendario.bind("<<CalendarSelected>>", lambda e: actualizar_fecha())
calendario.pack(padx=10, pady=10)


# =====> Etiqueta para mostrar la fecha seleccionada <=====
label_fecha = tk.Label(
    frame_calendario, 
    text="Fecha seleccionada: ", 
    bg="#190247", 
    fg="white", 
    font=("Calibri", 10)
)
label_fecha.pack()

resumen_label = tk.Label(
    frame_calendario,
    text="Resumen ",
    bg="#190247",
    fg="white",
    font=("Calibri", 10, "bold")
)
resumen_label.pack(pady=(5,0))
# =====> Función del resúmen <=====
def mostrar_resumen_diario(fecha_sel):
    tareas = tareas_por_fecha.get(fecha_sel,[])
    total = len(tareas)
    completadas = sum (1 for t in tareas if t.startswith("✅"))
    resumen_label.config(text=f"✅ Hoy completaste {completadas} de {total} hábitos.")

# =====> Función actualizar fecha <=====
def actualizar_fecha():
    fecha_sel = calendario.get_date()
    label_fecha.config(text=f"Fecha seleccionada: {fecha_sel}")
    mostrar_tareas_para_fecha(fecha_sel)
    mostrar_resumen_diario(fecha_sel)

# =====> Función cartel salida <=====
def confirmar_salida():
    if messagebox.askokcancel("Salir", "¿Seguro que quieres salir?"):
        guardar_tareas()
        ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", confirmar_salida)

actualizar()
cargar_tareas()
fecha_actual = calendario.get_date()
mostrar_tareas_para_fecha(fecha_actual)
print("Contenido cargado:", tareas_por_fecha)
ventana.mainloop()
