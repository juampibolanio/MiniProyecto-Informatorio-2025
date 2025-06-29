import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# --- Configuración ---
NOMBRE_ARCHIVO = "habitos.json"
CATEGORIAS_DEFAULT = ["Salud", "Trabajo", "Personal", "Ejercicio", "Estudio"]

# --- Variables globales ---
habitos_data = []
tree = None
reloj_label = None


# --- Funciones de utilidad ---
def calcular_racha(habito, dia_actual=None):
    # Calcula la racha actual de un hábito.
    if dia_actual is None:
        dia_actual = datetime.now().weekday() 

    dias_semana = [
        "lunes",
        "martes",
        "miercoles",
        "jueves",
        "viernes",
        "sabado",
        "domingo",
    ]
    racha = 0

    # Verificar días anteriores para calcular la racha
    for i in range(7): 
        dia_idx = (dia_actual - i) % 7
        dia_key = dias_semana[dia_idx]

        if habito["dias_para_hacer"].get(dia_key, False):
            if habito["dias"].get(dia_key, False):
                racha += 1
            else:
                break

    return racha


def calcular_porcentaje_completado():
    # Calcula el porcentaje total de hábitos completados esta semana.
    total_esperado = 0
    total_completado = 0

    for habito in habitos_data:
        for dia, debe_hacer in habito["dias_para_hacer"].items():
            if debe_hacer:
                total_esperado += 1
                if habito["dias"].get(dia, False):
                    total_completado += 1

    if total_esperado == 0:
        return 0
    return (total_completado / total_esperado) * 100


# --- Funciones de carga y guardado ---
def mostrar_habitos():
    # Actualiza la Treeview para mostrar el estado actual de los hábitos con rachas.
    for item in tree.get_children():
        tree.delete(item)

    dias_semana_claves = [
        "lunes",
        "martes",
        "miercoles",
        "jueves",
        "viernes",
        "sabado",
        "domingo",
    ]

    for habit in habitos_data:
        valores_fila = []
        racha = calcular_racha(habit)

        for dia_clave in dias_semana_claves:
            if habit["dias_para_hacer"].get(dia_clave, False):
                if habit["dias"].get(dia_clave, False):
                    valores_fila.append(f"{habit['nombre']} ✅")
                else:
                    valores_fila.append(habit["nombre"])
            else:
                valores_fila.append("")

        # Agregar información de categoría y racha al nombre
        categoria = habit.get("categoria", "Sin categoría")
        nombre_display = (
            f"{habit['nombre']}     •     [{categoria}]     •     🔥{racha}"
        )

        tree.insert("", tk.END, text=nombre_display, values=valores_fila)


def cargar_habitos():
    # Carga los hábitos desde el archivo JSON.
    global habitos_data

    ruta_completa_json = os.path.abspath(NOMBRE_ARCHIVO)
    print(f"Buscando/creando habitos.json en: {ruta_completa_json}")

    if os.path.exists(NOMBRE_ARCHIVO):
        try:
            with open(NOMBRE_ARCHIVO, "r", encoding="utf-8") as f:
                habitos_data = json.load(f)
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Error al leer el archivo de hábitos: {e}")
            habitos_data = []
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
            habitos_data = []
    else:
        habitos_data = []

    # Actualizar estructura de datos para compatibilidad
    for habit in habitos_data:
        if "dias_para_hacer" not in habit:
            dias_default = {
                "lunes": True,
                "martes": True,
                "miercoles": True,
                "jueves": True,
                "viernes": True,
                "sabado": True,
                "domingo": True,
            }
            habit["dias_para_hacer"] = dias_default

        if "dias" not in habit:
            habit["dias"] = {d: False for d in habit["dias_para_hacer"].keys()}

        if "categoria" not in habit:
            habit["categoria"] = "Sin categoría"

    if tree is not None:
        mostrar_habitos()
        mostrar_estadisticas()


def guardar_habitos():
    # Guarda los hábitos en el archivo JSON.
    try:
        with open(NOMBRE_ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(habitos_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar hábitos: {e}")


# --- Funciones para la interfaz ---
def toggle_estado_dia(event):
    # Marca o desmarca el estado de completado.
    item_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)

    try:
        col_index = int(column_id[1:])
    except ValueError:
        return

    if not item_id or col_index == 0:
        return

    nombre_completo = tree.item(item_id, "text")
    
    nombre_habito = nombre_completo.split("     •     ")[0]

    habit_index = -1
    for i, habit in enumerate(habitos_data):
        if habit["nombre"] == nombre_habito:
            habit_index = i
            break

    if habit_index == -1:
        return

    dias_semana_claves = [
        "lunes",
        "martes",
        "miercoles",
        "jueves",
        "viernes",
        "sabado",
        "domingo",
    ]

    if col_index - 1 >= len(dias_semana_claves) or col_index - 1 < 0:
        return

    dia_clave = dias_semana_claves[col_index - 1]

    if habitos_data[habit_index]["dias_para_hacer"].get(dia_clave, False):
        current_state = habitos_data[habit_index]["dias"].get(dia_clave, False)
        new_state = not current_state
        habitos_data[habit_index]["dias"][dia_clave] = new_state

        guardar_habitos()
        mostrar_habitos()
        mostrar_estadisticas()


def abrir_ventana_agregar_habito():
    # Ventana para agregar hábitos con categorías.
    ventana_agregar = tk.Toplevel(ventana)
    ventana_agregar.title("Agregar Nuevo Hábito")
    ventana_agregar.geometry("400x450")
    ventana_agregar.transient(ventana)
    ventana_agregar.grab_set()
    ventana_agregar.configure(bg="#E8F5E8")

    # Nombre del hábito
    frame_nombre = tk.Frame(ventana_agregar, bg="#E8F5E8")
    frame_nombre.pack(pady=10)
    tk.Label(frame_nombre, text="Nombre del Hábito:", bg="#D4F1D4").pack(
        side=tk.LEFT, padx=5
    )
    entry_nombre_habito = tk.Entry(frame_nombre, width=30)
    entry_nombre_habito.pack(side=tk.LEFT, padx=5)

    # Categoría
    frame_categoria = tk.Frame(ventana_agregar, bg="#E8F5E8")
    frame_categoria.pack(pady=10)
    tk.Label(frame_categoria, text="Categoría:", bg="#D4F1D4").pack(
        side=tk.LEFT, padx=5
    )
    combo_categoria = ttk.Combobox(frame_categoria, values=CATEGORIAS_DEFAULT, width=27)
    combo_categoria.set("Seleccionar categoría")
    combo_categoria.pack(side=tk.LEFT, padx=5)

    # Días para hacer
    frame_dias_hacer = tk.LabelFrame(
        ventana_agregar,
        text="¿Qué días debe realizarse?",
        padx=10,
        pady=5,
        bg="#D4F1D4",
    )
    frame_dias_hacer.pack(pady=10, padx=10, fill=tk.X)

    dias_semana_display = [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo",
    ]
    dias_semana_claves = [
        "lunes",
        "martes",
        "miercoles",
        "jueves",
        "viernes",
        "sabado",
        "domingo",
    ]

    checkbox_vars_dias_hacer = {}

    for i, dia in enumerate(dias_semana_display):
        var = tk.BooleanVar()
        chk = tk.Checkbutton(frame_dias_hacer, text=dia, variable=var, bg="#F0F8FF")
        chk.grid(row=i // 2, column=i % 2, padx=5, pady=2, sticky=tk.W)
        checkbox_vars_dias_hacer[dias_semana_claves[i]] = var

    # Botones de selección rápida
    frame_botones_rapidos = tk.Frame(ventana_agregar, bg="#E8F5E8")
    frame_botones_rapidos.pack(pady=5)

    def seleccionar_todos():
        for var in checkbox_vars_dias_hacer.values():
            var.set(True)

    def seleccionar_laborales():
        dias_laborales = ["lunes", "martes", "miercoles", "jueves", "viernes"]
        for dia, var in checkbox_vars_dias_hacer.items():
            var.set(dia in dias_laborales)

    def seleccionar_fines():
        dias_fines = ["sabado", "domingo"]
        for dia, var in checkbox_vars_dias_hacer.items():
            var.set(dia in dias_fines)

    tk.Button(frame_botones_rapidos, text="Todos", command=seleccionar_todos).pack(
        side=tk.LEFT, padx=2
    )
    tk.Button(
        frame_botones_rapidos, text="Laborales", command=seleccionar_laborales
    ).pack(side=tk.LEFT, padx=2)
    tk.Button(
        frame_botones_rapidos, text="Fines de semana", command=seleccionar_fines
    ).pack(side=tk.LEFT, padx=2)

    def guardar_nuevo_habito():
        nombre = entry_nombre_habito.get().strip()
        categoria = combo_categoria.get().strip()

        if not nombre:
            messagebox.showwarning(
                "Advertencia", "El nombre del hábito no puede estar vacío."
            )
            return

        if categoria == "Seleccionar categoría" or not categoria:
            categoria = "Sin categoría"

        dias_para_hacer_habit = {}
        for dia_clave in dias_semana_claves:
            dias_para_hacer_habit[dia_clave] = checkbox_vars_dias_hacer[dia_clave].get()

        if not any(dias_para_hacer_habit.values()):
            messagebox.showwarning(
                "Advertencia",
                "Debe seleccionar al menos un día para realizar el hábito.",
            )
            return

        nuevo_habito = {
            "nombre": nombre,
            "categoria": categoria,
            "dias_para_hacer": dias_para_hacer_habit,
            "dias": {dia: False for dia in dias_semana_claves},
        }

        habitos_data.append(nuevo_habito)
        guardar_habitos()
        mostrar_habitos()
        mostrar_estadisticas()
        ventana_agregar.destroy()

    boton_confirmar = tk.Button(
        ventana_agregar, text="Confirmar Hábito", command=guardar_nuevo_habito
    )
    boton_confirmar.pack(pady=10)


def mostrar_estadisticas():
    # Muestra estadísticas de la semana en el label de estadísticas.
    texto_estadisticas = "📊 Estadísticas de la semana:\n\n"

    for habit in habitos_data:
        total = sum(1 for se_hace in habit["dias_para_hacer"].values() if se_hace)
        hechos = sum(
            1
            for dia, se_hace in habit["dias_para_hacer"].items()
            if se_hace and habit["dias"].get(dia, False)
        )

        porcentaje = (hechos / total * 100) if total > 0 else 0
        racha = calcular_racha(habit)

        estado = "✅" if hechos == total and total > 0 else "❌"
        texto_estadisticas += f"{estado} {habit['nombre']}: {hechos}/{total} días ({porcentaje:.0f}%) 🔥{racha}\n"

    porcentaje_global = calcular_porcentaje_completado()
    texto_estadisticas += f"\n🎯 Progreso global: {porcentaje_global:.1f}%"

    label_estadisticas.config(text=texto_estadisticas)


def eliminar_habito():
    # Elimina los hábitos seleccionados de la lista
    seleccion = tree.selection()
    if seleccion:
        if not messagebox.askyesno(
            "Confirmar Eliminación",
            "¿Estás seguro de que quieres eliminar los hábitos seleccionados?",
        ):
            return

        nombres_a_eliminar = []
        for item_id in seleccion:
            nombre_completo = tree.item(item_id, "text")
            nombre_habito = nombre_completo.split("     •     ")[
                0
            ]  # Extraer solo el nombre
            nombres_a_eliminar.append(nombre_habito)

        global habitos_data
        habitos_data = [
            h for h in habitos_data if h["nombre"] not in nombres_a_eliminar
        ]

        guardar_habitos()
        mostrar_habitos()
        mostrar_estadisticas()


def eliminar_habito_dia_especifico(event):
    # Elimina un hábito para un día específico (doble clic).
    item_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)

    try:
        col_index = int(column_id[1:])
    except ValueError:
        return

    if not item_id or col_index == 0:
        return

    nombre_completo = tree.item(item_id, "text")
    nombre_habito = nombre_completo.split("     •     ")[0]

    habit_index = -1
    for i, habit in enumerate(habitos_data):
        if habit["nombre"] == nombre_habito:
            habit_index = i
            break

    if habit_index == -1:
        return

    dias_semana_claves = [
        "lunes",
        "martes",
        "miercoles",
        "jueves",
        "viernes",
        "sabado",
        "domingo",
    ]

    if col_index - 1 >= len(dias_semana_claves) or col_index - 1 < 0:
        return

    dia_clave = dias_semana_claves[col_index - 1]
    dia_display = dias_semana_claves[col_index - 1].capitalize()

    if habitos_data[habit_index]["dias_para_hacer"].get(dia_clave, False):
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación por Día",
            f"¿Estás seguro de que quieres eliminar '{nombre_habito}' para el día {dia_display}?",
        )
        if confirmacion:
            habitos_data[habit_index]["dias_para_hacer"][dia_clave] = False
            habitos_data[habit_index]["dias"][dia_clave] = False
            guardar_habitos()
            mostrar_habitos()
            mostrar_estadisticas()


def actualizar_reloj():
    # Actualiza el label del reloj con la fecha y hora actuales.
    now = datetime.now()
    formato_fecha = now.strftime("%A, %d/%m/%Y")
    formato_hora = now.strftime("%H:%M:%S")

    dias_semana_es = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo",
    }
    for eng, esp in dias_semana_es.items():
        formato_fecha = formato_fecha.replace(eng, esp)

    reloj_label.config(text=f"{formato_fecha}\n{formato_hora}")
    ventana.after(1000, actualizar_reloj)


# --- Configuración de la ventana principal ---
ventana = tk.Tk()
ventana.title("Gestor de Hábitos Diarios")
ventana.geometry("950x700")
ventana.configure(bg="#44AB7E")

# --- Aplicar estilos con ttk.Style ---
style = ttk.Style()
style.configure(
    "Treeview",
    rowheight=25,
    background="#EFF0EF",
    fieldbackground="#050605",
    bordercolor="gray",
    borderwidth=3,
    relief="solid",
    column_lines=True,
)
style.configure(
    "Treeview.Heading",
    background="#E1DADC",
    foreground="black",
    font=("Arial", 10, "bold"),
)
style.map(
    "Treeview", background=[("selected", "#189052")], foreground=[("selected", "black")]
)

# --- Frame para el reloj ---
frame_reloj = tk.Frame(ventana, bg="#44AB7E")
frame_reloj.pack(pady=10, padx=10, anchor=tk.NE)

reloj_label = tk.Label(
    frame_reloj, font=("Arial", 10, "bold"), bg="#44AB7E", fg="black", justify=tk.RIGHT
)
reloj_label.pack(side=tk.RIGHT)

# --- Frame para botones principales ---
frame_botones_principales = tk.Frame(ventana, bg="#44AB7E")
frame_botones_principales.pack(pady=5, fill=tk.X)

boton_abrir_agregar = tk.Button(
    frame_botones_principales,
    text="➕ Agregar Nuevo Hábito",
    command=abrir_ventana_agregar_habito,
    font=("Arial", 10, "bold"),
    bg="#03F584",
    fg="black",
    relief=tk.RAISED,
)
boton_abrir_agregar.pack(side=tk.LEFT, pady=5, padx=5)

boton_eliminar = tk.Button(
    frame_botones_principales,
    text="🗑️ Eliminar Hábito",
    command=eliminar_habito,
    font=("Arial", 10, "bold"),
    bg="#FF6B6B",
    fg="white",
    relief=tk.RAISED,
)
boton_eliminar.pack(side=tk.LEFT, padx=5)

# --- Frame para la Treeview de hábitos ---
frame_treeview = tk.Frame(ventana, bg="#8AD2A2")
frame_treeview.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# --- Configurar Treeview ---
columnas = ("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo")
tree = ttk.Treeview(frame_treeview, columns=columnas, show="tree headings", height=15)

tree.heading(
    "#0",
    text="          📋Hábito          •          🏷️Categoría          •          🔥Racha",
    anchor=tk.W,
)
tree.column("#0", width=400, minwidth=400, stretch=tk.YES)

for col_display_name in columnas:
    tree.heading(col_display_name, text=col_display_name, anchor=tk.CENTER)
    tree.column(col_display_name, width=100, anchor=tk.CENTER)

scrollbar_tree = ttk.Scrollbar(frame_treeview, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar_tree.set)

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y)

# --- Vincular eventos de clic a la Treeview ---
tree.bind("<Button-1>", toggle_estado_dia)
tree.bind("<Double-1>", eliminar_habito_dia_especifico)

# --- Frame para estadísticas ---
frame_estadisticas = tk.Frame(ventana, bg="#44AB7E")
frame_estadisticas.pack(pady=5, fill=tk.X)

label_estadisticas = tk.Label(
    frame_estadisticas,
    text="📊 Estadísticas de la semana:",
    font=("Arial", 9, "bold"),
    bg="#44AB7E",
    fg="black",
    justify=tk.LEFT,
    anchor="w",
)
label_estadisticas.pack(anchor=tk.W, padx=10, fill=tk.X)

def ordenar_habitos_alfabeticamente():
    global habitos_data
    habitos_data.sort(key=lambda x: x["nombre"].lower())
    guardar_habitos()
    mostrar_habitos()
    mostrar_estadisticas()
    messagebox.showinfo("Éxito", "Hábitos ordenados alfabéticamente")

def borrar_todos_habitos():
    if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar TODOS los hábitos?"):
        global habitos_data
        habitos_data = []
        guardar_habitos()
        mostrar_habitos()
        mostrar_estadisticas()
        messagebox.showinfo("Éxito", "Todos los hábitos han sido eliminados")

def toggle_reloj():
    if reloj_label.winfo_viewable():
        frame_reloj.pack_forget()
    else:
        frame_reloj.pack(pady=10, padx=10, anchor=tk.NE, before=frame_botones_principales)

def mostrar_estadisticas_detalladas():
    total_habitos = len(habitos_data)
    if total_habitos == 0:
        messagebox.showinfo("Estadísticas", "No hay hábitos registrados")
        return
    
    dias_semana = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    dia_actual = dias_semana[datetime.now().weekday()]
    
    habitos_hoy = sum(1 for h in habitos_data if h["dias_para_hacer"].get(dia_actual, False))
    completados_hoy = sum(1 for h in habitos_data if h["dias_para_hacer"].get(dia_actual, False) and h["dias"].get(dia_actual, False))
    pendientes_hoy = habitos_hoy - completados_hoy
    
    porcentaje_global = calcular_porcentaje_completado()
    
    stats_text = f"""📊 ESTADÍSTICAS DETALLADAS

🎯 Hábitos totales registrados: {total_habitos}

📅 HOY ({dia_actual.upper()}):
✅ Completados: {completados_hoy}
⏳ Pendientes: {pendientes_hoy}
📋 Total para hoy: {habitos_hoy}

🌟 Progreso semanal global: {porcentaje_global:.1f}%"""
    
    messagebox.showinfo("📊 Estadísticas Detalladas", stats_text)

# --- Menú desplegable principal ---
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

# Menú Principal
menu_principal = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label='Principal', menu=menu_principal)

# Submenú Opciones
submenu_opciones = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label='Opciones', menu=submenu_opciones)

# Opciones del submenú
submenu_opciones.add_command(label='📁 Agregar nuevo hábito', command=abrir_ventana_agregar_habito)
submenu_opciones.add_separator()
submenu_opciones.add_command(label='🔤 Ordenar alfabéticamente', command=ordenar_habitos_alfabeticamente)
submenu_opciones.add_command(label='🗑️ Borrar todos los hábitos', command=borrar_todos_habitos)
submenu_opciones.add_separator()
submenu_opciones.add_command(label='⏰ Mostrar/Ocultar reloj', command=toggle_reloj)
submenu_opciones.add_command(label='📊 Estadísticas detalladas', command=mostrar_estadisticas_detalladas)
submenu_opciones.add_separator()

def mostrar_info():
    info_text = """
🎯 Gestor de Hábitos Diarios
━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ CARACTERÍSTICAS:
• Seguimiento diario de hábitos
• Sistema de rachas
• Categorización de hábitos
• Estadísticas de progreso

🎮 CÓMO USAR:
• Clic simple: Marcar/desmarcar hábito
• Doble clic: Eliminar hábito del día
• Los emojis indican: ✅ Completado, 🔥 Racha

👥 Grupo II - Informatorio 2025 - Creado con Python + Tkinter
    """
    ventana_info = tk.Toplevel(ventana)
    ventana_info.title("ℹ️ Acerca de")
    ventana_info.geometry("420x400")
    ventana_info.resizable(False, False)
    ventana_info.configure(bg="#3b0101")

    # Título
    titulo_label = tk.Label(
        ventana_info,
        text="Gestor de hábitos diarios",
        font=("Calibri", 14, "bold"),
        bg="#3b0101",
        fg="white",
        anchor="w"
    )
    titulo_label.pack(padx=10, pady=(10, 0), anchor="w")

    # Información
    texto_info = tk.Text(
        ventana_info, 
        wrap=tk.WORD, 
        font=("Arial", 10),
        bg="#3b0101",
        fg="white",
        insertbackground="white"
    )
    texto_info.insert(tk.END, info_text)
    texto_info.config(state=tk.DISABLED)
    texto_info.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

submenu_opciones.add_command(label='ℹ️ Acerca de', command=mostrar_info)
submenu_opciones.add_command(label='🚪 Salir', command=ventana.quit)

# --- Cargar hábitos al iniciar ---
cargar_habitos()

# --- Iniciar el reloj ---
actualizar_reloj()


# --- Mensaje de bienvenida ---
def mostrar_bienvenida():
    if not habitos_data:
        welcome_msg = """
🎉 ¡Bienvenido al Gestor de Hábitos!

Para comenzar:
1. Haz clic en "➕ Agregar Nuevo Hábito"
2. Define qué días quieres realizarlo
3. ¡Empieza a construir buenos hábitos!

Características:
• Seguimiento diario simple
• Sistema de rachas 🔥
• Organización por categorías
        """
        messagebox.showinfo("¡Bienvenido!", welcome_msg)


# Mostrar bienvenida después de que la ventana esté lista
ventana.after(1000, mostrar_bienvenida)

# --- Bucle principal ---
try:
    ventana.mainloop()
except Exception as e:
    # Guarda datos antes de cerrar en caso de error
    try:
        guardar_habitos()
    except:
        pass
    messagebox.showerror("Error", f"Error inesperado: {e}")