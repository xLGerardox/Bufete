import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import Calendar
import hashlib

# Datos
clientes = []
expedientes = []
agenda_citas = []
tareas_urgentes = []
hash_expedientes = {}

# Estilos
BG_COLOR = "#0b1f3f"
PANEL_COLOR = "#ffffff"
ENTRY_COLOR = "#f2f2f2"
BTN_COLOR = "#dfe6e9"
BTN_TEXT = "#2d3436"
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_NORMAL = ("Segoe UI", 11)

# Funciones de placeholder
def limpiar_placeholder(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg='black')

def restaurar_placeholder(event, entry, placeholder):
    if entry.get() == '':
        entry.insert(0, placeholder)
        entry.config(fg='gray')

# Registro de cliente
def registrar_cliente():
    nombre = entry_nombre.get().strip()
    dpi = entry_dpi.get().strip()
    telefono = entry_telefono.get().strip()
    if nombre and dpi and telefono and nombre != "Nombre completo" and dpi != "DPI" and telefono != "Teléfono":
        clientes.append({"nombre": nombre, "dpi": dpi, "telefono": telefono})
        messagebox.showinfo("Éxito", f"Cliente {nombre} registrado.")
        for entry, placeholder in [(entry_nombre, "Nombre completo"), (entry_dpi, "DPI"), (entry_telefono, "Teléfono")]:
            entry.delete(0, tk.END)
            entry.insert(0, placeholder)
            entry.config(fg='gray')
    else:
        messagebox.showwarning("Error", "Completa todos los campos.")

# Registro de expediente
def registrar_expediente():
    try:
        id_exp = int(simpledialog.askstring("ID", "ID del expediente:"))
        if id_exp in hash_expedientes:
            messagebox.showwarning("Error", "Ese ID ya existe.")
            return
        cliente = simpledialog.askstring("Cliente", "Nombre del cliente:")
        tipo = simpledialog.askstring("Tipo", "Tipo de caso:")
        fecha = simpledialog.askstring("Fecha", "Fecha de apertura:")
        if cliente and tipo and fecha:
            expediente = [id_exp, cliente, tipo, fecha]
            expedientes.append(expediente)
            hash_expedientes[id_exp] = expediente
            messagebox.showinfo("Éxito", "Expediente registrado.")
        else:
            messagebox.showwarning("Error", "Datos incompletos.")
    except:
        messagebox.showwarning("Error", "ID inválido.")

# Agenda de citas
def abrir_agenda_cita():
    ventana_cita = tk.Toplevel(ventana)
    ventana_cita.title("Agendar Cita")
    ventana_cita.geometry("300x400")
    ventana_cita.configure(bg=BG_COLOR)

    tk.Label(ventana_cita, text="Selecciona la fecha", font=FONT_NORMAL, bg=BG_COLOR, fg="white").pack(pady=5)
    cal = Calendar(ventana_cita, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=5)

    campos = [("Hora (HH:MM):", "hora"), ("Cliente:", "cliente"), ("Motivo:", "motivo")]
    entradas = {}

    for texto, clave in campos:
        tk.Label(ventana_cita, text=texto, font=FONT_NORMAL, bg=BG_COLOR, fg="white").pack(pady=5)
        entrada = tk.Entry(ventana_cita, bg=ENTRY_COLOR)
        entrada.pack(pady=5)
        entradas[clave] = entrada

    def guardar_cita():
        fecha = cal.get_date()
        hora = entradas["hora"].get().strip()
        cliente = entradas["cliente"].get().strip()
        motivo = entradas["motivo"].get().strip()
        if fecha and hora and cliente and motivo:
            agenda_citas.append({"cliente": cliente, "fecha": fecha, "hora": hora, "motivo": motivo})
            messagebox.showinfo("Éxito", "Cita agendada.")
            ventana_cita.destroy()
        else:
            messagebox.showwarning("Error", "Completa todos los campos.")

    tk.Button(ventana_cita, text="Agendar", command=guardar_cita,
              bg=BTN_COLOR, fg=BTN_TEXT, font=FONT_NORMAL).pack(pady=10)

def mostrar_agenda():
    if not agenda_citas:
        messagebox.showinfo("Agenda vacía", "No hay citas registradas.")
        return
    texto = ""
    for cita in agenda_citas:
        texto += f"{cita['fecha']} {cita['hora']} - {cita['cliente']} ({cita['motivo']})\n"
    messagebox.showinfo("Agenda de citas", texto)

# Tareas urgentes
def agregar_tarea():
    tarea = simpledialog.askstring("Tarea urgente", "Descripción:")
    if tarea:
        tareas_urgentes.append(tarea)
        messagebox.showinfo("Éxito", "Tarea agregada.")
    else:
        messagebox.showwarning("Error", "No se ingresó ninguna tarea.")

def atender_tarea():
    if tareas_urgentes:
        tarea = tareas_urgentes.pop()
        messagebox.showinfo("Tarea atendida", f"Se atendió: {tarea}")
    else:
        messagebox.showinfo("Sin tareas", "No hay tareas urgentes.")

def buscar_expediente_hash():
    try:
        id_exp = int(simpledialog.askstring("Buscar expediente", "ID del expediente:"))
        resultado = hash_expedientes.get(id_exp)
        if resultado:
            messagebox.showinfo("Expediente encontrado", str(resultado))
        else:
            messagebox.showinfo("No encontrado", "Expediente no registrado.")
    except:
        messagebox.showwarning("Error", "ID inválido.")

# Interfaz principal
ventana = tk.Tk()
ventana.title("Rivera & Rivera — Sistema de Gestión")
ventana.geometry("700x800")
ventana.configure(bg=BG_COLOR)

# Cabecera
tk.Label(ventana, text="Rivera & Rivera", font=FONT_TITLE, bg=BG_COLOR, fg="white").pack(pady=20)

# Panel de cliente
panel_cliente = tk.LabelFrame(ventana, text="Registrar Cliente", bg=PANEL_COLOR, font=FONT_NORMAL, padx=10, pady=10)
panel_cliente.pack(pady=10, fill="x", padx=20)

entry_nombre = tk.Entry(panel_cliente, width=40, fg="gray", bg=ENTRY_COLOR)
entry_nombre.insert(0, "Nombre completo")
entry_nombre.bind("<FocusIn>", lambda e: limpiar_placeholder(e, entry_nombre, "Nombre completo"))
entry_nombre.bind("<FocusOut>", lambda e: restaurar_placeholder(e, entry_nombre, "Nombre completo"))
entry_nombre.pack(pady=5)

entry_dpi = tk.Entry(panel_cliente, width=40, fg="gray", bg=ENTRY_COLOR)
entry_dpi.insert(0, "DPI")
entry_dpi.bind("<FocusIn>", lambda e: limpiar_placeholder(e, entry_dpi, "DPI"))
entry_dpi.bind("<FocusOut>", lambda e: restaurar_placeholder(e, entry_dpi, "DPI"))
entry_dpi.pack(pady=5)

entry_telefono = tk.Entry(panel_cliente, width=40, fg="gray", bg=ENTRY_COLOR)
entry_telefono.insert(0, "Teléfono")
entry_telefono.bind("<FocusIn>", lambda e: limpiar_placeholder(e, entry_telefono, "Teléfono"))
entry_telefono.bind("<FocusOut>", lambda e: restaurar_placeholder(e, entry_telefono, "Teléfono"))
entry_telefono.pack(pady=5)

tk.Button(panel_cliente, text="Registrar Cliente", command=registrar_cliente,
          bg="#27ae60", fg="white", font=FONT_NORMAL, relief="flat").pack(pady=10)

# Panel de acciones
panel_acciones = tk.LabelFrame(ventana, text="Gestión del Sistema", bg=PANEL_COLOR, font=FONT_NORMAL, padx=10, pady=10)
panel_acciones.pack(pady=10, fill="x", padx=20)

fila1 = tk.Frame(panel_acciones, bg=PANEL_COLOR)
fila2 = tk.Frame(panel_acciones, bg=PANEL_COLOR)
fila1.pack(pady=5)
fila2.pack(pady=5)

botones = [
    ("Registrar Expediente", registrar_expediente),
    ("Agendar Cita", abrir_agenda_cita),
    ("Mostrar Agenda", mostrar_agenda),
    ("Agregar Tarea Urgente", agregar_tarea),
    ("Atender Tarea Urgente", atender_tarea),
    ("Buscar Expediente por ID", buscar_expediente_hash),
]

for i, (texto, funcion) in enumerate(botones):
    destino = fila1 if i < 3 else fila2
    tk.Button(destino, text=texto, command=funcion, width=25,
              bg=BTN_COLOR, fg=BTN_TEXT, font=FONT_NORMAL, relief="flat").pack(side="left", padx=10, pady=5)

ventana.mainloop()