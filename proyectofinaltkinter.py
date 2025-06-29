import tkinter as tk
from tkinter import ttk
import json
import os
from datetime import datetime
from tkinter import messagebox 

# --- Nombre del archivo donde guardaremos los hábitos ---
NOMBRE_ARCHIVO = "habitos.json"

# --- Lista global para almacenar los hábitos en memoria ---
habitos_data = []

# --- Variable global para la Treeview ---
tree = None

# --- Variable global para el Label del reloj ---
reloj_label = None


# --- Funciones de Carga, Guardado y Visualización ---

def mostrar_habitos():
    """Actualiza la Treeview para mostrar el estado actual de los hábitos."""
    for item in tree.get_children():
        tree.delete(item)

    dias_semana_claves = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

    for habit in habitos_data:
        valores_fila = []
        
        for dia_clave in dias_semana_claves:
            if habit["dias_para_hacer"].get(dia_clave, False):
                if habit["dias"].get(dia_clave, False):
                    valores_fila.append(f"{habit['nombre']} ✅")
                else:
                    valores_fila.append(habit["nombre"])
            else:
                valores_fila.append("")

        tree.insert("", tk.END, text=habit["nombre"], values=valores_fila)

def cargar_habitos():
    """Carga los hábitos desde el archivo JSON o los inicializa si no existe."""
    global habitos_data
    
    ruta_completa_json = os.path.abspath(NOMBRE_ARCHIVO)
    print(f"Buscando/creando habitos.json en: {ruta_completa_json}")

    if os.path.exists(NOMBRE_ARCHIVO):
        with open(NOMBRE_ARCHIVO, 'r', encoding='utf-8') as f:
            try:
                habitos_data = json.load(f)
            except json.JSONDecodeError:
                habitos_data = [] 
    else: 
        habitos_data = [] 
        
    print(f"Contenido de habitos_data cargado: {habitos_data}")
    
    for habit in habitos_data:
        if "dias_para_hacer" not in habit:
            dias_default = {
                "lunes": True, "martes": True, "miercoles": True, 
                "jueves": True, "viernes": True, "sabado": True, "domingo": True
            }
            habit["dias_para_hacer"] = dias_default
            if "dias" not in habit:
                habit["dias"] = {d: False for d in dias_default.keys()}
    
    if tree is not None: 
        mostrar_habitos()

def guardar_habitos():
    """Guarda los hábitos actuales en el archivo JSON."""
    with open(NOMBRE_ARCHIVO, 'w', encoding='utf-8') as f:
        json.dump(habitos_data, f, indent=4, ensure_ascii=False)

# --- Funciones de Eliminar habitos ---
def eliminar_habito():
    """Elimina los hábitos seleccionados de la lista y actualiza la vista."""
    seleccion = tree.selection()
    if seleccion:
        if not messagebox.askyesno("Confirmar Eliminación", 
                                "¿Estás seguro de que quieres eliminar los hábitos seleccionados por completo?"):
            return 

        nombres_a_eliminar = [tree.item(item_id, "text") for item_id in seleccion]
        
        global habitos_data
        habitos_data = [h for h in habitos_data if h["nombre"] not in nombres_a_eliminar]
        
        guardar_habitos()
        mostrar_habitos()

def toggle_estado_dia(event):
    """Marca o desmarca el estado de completado de un hábito para un día específico (clic simple)."""
    item_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)

    try:
        col_index = int(column_id[1:]) 
    except ValueError: 
        return

    if not item_id or col_index == 0: 
        return

    nombre_habito = tree.item(item_id, "text")
    habit_index = -1
    for i, habit in enumerate(habitos_data):
        if habit["nombre"] == nombre_habito:
            habit_index = i
            break
    
    if habit_index == -1: return

    dias_semana_claves = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    
    if col_index - 1 >= len(dias_semana_claves) or col_index - 1 < 0: return 

    dia_clave = dias_semana_claves[col_index - 1]

    if habitos_data[habit_index]["dias_para_hacer"].get(dia_clave, False):
        current_state = habitos_data[habit_index]["dias"].get(dia_clave, False)
        habitos_data[habit_index]["dias"][dia_clave] = not current_state
        guardar_habitos()
        mostrar_habitos()

def eliminar_habito_dia_especifico(event):
    """Elimina un hábito para un día específico (doble clic)."""
    item_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)

    try:
        col_index = int(column_id[1:]) 
    except ValueError:
        return

    if not item_id or col_index == 0: 
        return

    nombre_habito = tree.item(item_id, "text")
    habit_index = -1
    for i, habit in enumerate(habitos_data):
        if habit["nombre"] == nombre_habito:
            habit_index = i
            break
    
    if habit_index == -1: return

    dias_semana_claves = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    
    if col_index - 1 >= len(dias_semana_claves) or col_index - 1 < 0: return 

    dia_clave = dias_semana_claves[col_index - 1]
    dia_display = dias_semana_claves[col_index - 1].capitalize() 

    if habitos_data[habit_index]["dias_para_hacer"].get(dia_clave, False):
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación por Día",
            f"¿Estás seguro de que quieres eliminar '{nombre_habito}' para el día {dia_display}?"
        )
        if confirmacion:
            habitos_data[habit_index]["dias_para_hacer"][dia_clave] = False
            habitos_data[habit_index]["dias"][dia_clave] = False 
            guardar_habitos()
            mostrar_habitos()

# --- Funciones de Interfaz de Usuario Adicionales ---
def abrir_ventana_agregar_habito():
    """Abre una nueva ventana para agregar un nuevo hábito."""
    ventana_agregar = tk.Toplevel(ventana)
    ventana_agregar.title("Agregar Nuevo Hábito")
    ventana_agregar.geometry("350x300") 
    ventana_agregar.transient(ventana) 
    ventana_agregar.grab_set() 
    ventana_agregar.configure(bg="#E81259")

    frame_nombre = tk.Frame(ventana_agregar, bg="#E81259")
    frame_nombre.pack(pady=10)
    tk.Label(frame_nombre, text="Nombre del Hábito:", bg="#D386E8").pack(side=tk.LEFT, padx=5)
    entry_nombre_habito = tk.Entry(frame_nombre, width=30)
    entry_nombre_habito.pack(side=tk.LEFT, padx=5)

    frame_dias_hacer = tk.LabelFrame(ventana_agregar, text="¿Qué días debe realizarse?", padx=10, pady=5, bg="#D386E8")
    frame_dias_hacer.pack(pady=10, padx=10, fill=tk.X)

    dias_semana_display = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    dias_semana_claves = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    
    checkbox_vars_dias_hacer = {} 

    for i, dia in enumerate(dias_semana_display):
        var = tk.BooleanVar()
        chk = tk.Checkbutton(frame_dias_hacer, text=dia, variable=var, bg="#F0F8FF")
        chk.grid(row=i // 2, column=i % 2, padx=5, pady=2, sticky=tk.W)
        checkbox_vars_dias_hacer[dias_semana_claves[i]] = var

    def guardar_nuevo_habito():
        """Guarda el nuevo hábito con los días seleccionados."""
        nombre = entry_nombre_habito.get().strip()
        if not nombre:
            tk.messagebox.showwarning("Advertencia", "El nombre del hábito no puede estar vacío.")
            return
        
        dias_para_hacer_habit = {}
        for dia_clave in dias_semana_claves:
            dias_para_hacer_habit[dia_clave] = checkbox_vars_dias_hacer[dia_clave].get()

        if not any(dias_para_hacer_habit.values()):
            tk.messagebox.showwarning("Advertencia", "Debe seleccionar al menos un día para realizar el hábito.")
            return

        dias_completado_inicial = {dia: False for dia in dias_semana_claves}

        nuevo_habito = {
            "nombre": nombre,
            "dias_para_hacer": dias_para_hacer_habit,
            "dias": dias_completado_inicial
        }
        
        habitos_data.append(nuevo_habito)
        guardar_habitos()
        mostrar_habitos()
        ventana_agregar.destroy()

    boton_confirmar = tk.Button(ventana_agregar, text="Confirmar Hábito", command=guardar_nuevo_habito)
    boton_confirmar.pack(pady=10)

# --- Función para actualizar el reloj ---
def actualizar_reloj():
    """Actualiza el label del reloj con la fecha y hora actuales."""
    now = datetime.now()
    formato_fecha = now.strftime("%A, %d/%m/%Y")
    formato_hora = now.strftime("%H:%M:%S")
    
    dias_semana_es = {
        "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
        "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
    }
    for eng, esp in dias_semana_es.items():
        formato_fecha = formato_fecha.replace(eng, esp)

    reloj_label.config(text=f"{formato_fecha}\n{formato_hora}")
    ventana.after(1000, actualizar_reloj) 


# --- Configuración de la ventana principal ---
ventana = tk.Tk()
ventana.title('Gestor de Hábitos Diarios')
ventana.geometry('800x550')
ventana.configure(bg="#44AB7E") 

# --- Aplicar estilos con ttk.Style ---
style = ttk.Style()
style.configure("Treeview", 
                rowheight=25, 
                background="#EFF0EF", 
                fieldbackground="#050605", 
                bordercolor="gray",  
                borderwidth=3,       
                relief="solid",
                column_lines=True       
            )
style.configure("Treeview.Heading", # Estilo general para los encabezados, sin color específico de día
                background="#E1DADC", # Color gris por defecto
                foreground="black",   
                font=("Arial", 10, "bold")) 
style.map("Treeview", 
        background=[('selected', "#189052")], 
        foreground=[('selected', 'black')]) 


# --- Frame para el reloj (parte superior derecha) ---
frame_reloj = tk.Frame(ventana, bg="#44AB7E")
frame_reloj.pack(pady=10, padx=10, anchor=tk.NE) 

reloj_label = tk.Label(
    frame_reloj, 
    font=("Arial", 10, "bold"), 
    bg="#44AB7E", 
    fg="black",
    justify=tk.RIGHT 
)
reloj_label.pack(side=tk.RIGHT) 

# --- Frame para el botón "Agregar Nuevo Hábito" (centrado) ---
frame_agregar_btn = tk.Frame(ventana, bg="#44AB7E") 
frame_agregar_btn.pack(pady=5, fill=tk.X) 

boton_abrir_agregar = tk.Button(
    frame_agregar_btn, 
    text='Agregar Nuevo Hábito',
    command=abrir_ventana_agregar_habito,
    font=("Arial", 10, "bold"),
    bg="#03F584",
    fg="black",
    relief=tk.RAISED
)
boton_abrir_agregar.pack(pady=5, padx=5) 

# --- Frame para los botones de acción (Eliminar - Mismo estilo) ---
frame_acciones_lista = tk.Frame(ventana, bg="#03F584")
frame_acciones_lista.pack(pady=5)

boton_eliminar = tk.Button(
    frame_acciones_lista,
    text='Eliminar Hábito',
    command=eliminar_habito,
    font=("Arial", 10, "bold"),
    bg="#03F584",
    fg="black",
    relief=tk.RAISED
)
boton_eliminar.pack(side=tk.LEFT, padx=5)

# --- Frame para la Treeview de hábitos con barra de desplazamiento ---
frame_treeview = tk.Frame(ventana, bg="#8AD2A2")
frame_treeview.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

columnas = ("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo")
tree = ttk.Treeview(frame_treeview, columns=columnas, show="headings", height=15)

tree.heading("#0", text="Hábito", anchor=tk.W)

# El bucle que aplicaba los estilos específicos de color a los encabezados se ha modificado.
for col_display_name in columnas: # Se ha vuelto al bucle simple
    tree.heading(col_display_name, text=col_display_name, anchor=tk.CENTER)
    tree.column(col_display_name, width=80, anchor=tk.CENTER)


tree.column("#0", width=200, minwidth=150, stretch=tk.YES)

scrollbar_tree = ttk.Scrollbar(frame_treeview, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar_tree.set)

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y)
# --- Vincular eventos de clic a la Treeview ---
tree.bind("<Button-1>", toggle_estado_dia) 
tree.bind("<Double-1>", eliminar_habito_dia_especifico) 
# --- Menú desplegable ---
menu_principal = tk.Menu(ventana)
ventana.config(menu=menu_principal)

menu_archivo = tk.Menu(menu_principal, tearoff=0)
menu_archivo.add_command(label="Agregar nuevo hábito", command=abrir_ventana_agregar_habito)
menu_archivo.add_command(label="Eliminar hábito", command=eliminar_habito)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=ventana.quit)
menu_principal.add_cascade(label="Archivo", menu=menu_archivo)

def mostrar_info():
    messagebox.showinfo("Acerca de", "Gestor de Hábitos v1.0\nCreado por el grupo 2 y Tkinter")

menu_ayuda = tk.Menu(menu_principal, tearoff=0)
menu_ayuda.add_command(label="Acerca de", command=mostrar_info)
menu_principal.add_cascade(label="Ayuda", menu=menu_ayuda)

# --- Cargar hábitos al iniciar la aplicación ---
cargar_habitos()

# --- Iniciar el reloj ---
actualizar_reloj() 

# --- Bucle principal de Tkinter ---
ventana.mainloop()
