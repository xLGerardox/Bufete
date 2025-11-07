import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import Calendar
import hashlib

clientes = []
expedientes = []
agenda_citas = []
tareas_urgentes = []
hash_expedientes = {}

# Colores base
BG_COLOR = "#f0f0f0"
BTN_COLOR = "#2c3e50"
BTN_TEXT = "#ffffff"
FONT_TITLE = ("Arial", 14, "bold")
FONT_NORMAL = ("Arial", 11)

# Funciones
def registrar_cliente():
    nombre = entry_nombre.get().strip()
    dpi = entry_dpi.get().strip()
    telefono = entry_telefono.get().strip()
    if nombre and dpi and telefono:
        clientes.append({"nombre": nombre, "dpi": dpi, "telefono": telefono})
        messagebox.showinfo("Éxito", f"Cliente {nombre} registrado.")
        entry_nombre.delete(0, tk.END)
        entry_dpi.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
    else:
        messagebox.showwarning("Error", "Completa todos los campos.")

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

def abrir_agenda_cita():
    ventana_cita = tk.Toplevel(ventana)
    ventana_cita.title("Agendar Cita")
    ventana_cita.geometry("300x400")
    ventana_cita.configure(bg=BG_COLOR)

    tk.Label(ventana_cita, text="Selecciona la fecha", font=FONT_NORMAL, bg=BG_COLOR).pack(pady=5)
    cal = Calendar(ventana_cita, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=5)

    tk.Label(ventana_cita, text="Hora (HH:MM):", font=FONT_NORMAL, bg=BG_COLOR).pack(pady=5)
    entry_hora = tk.Entry(ventana_cita)
    entry_hora.pack(pady=5)

    tk.Label(ventana_cita, text="Cliente:", font=FONT_NORMAL, bg=BG_COLOR).pack(pady=5)
    entry_cliente = tk.Entry(ventana_cita)
    entry_cliente.pack(pady=5)

    tk.Label(ventana_cita, text="Motivo:", font=FONT_NORMAL, bg=BG_COLOR).pack(pady=5)
    entry_motivo = tk.Entry(ventana_cita)
    entry_motivo.pack(pady=5)

    def guardar_cita():
        fecha = cal.get_date()
        hora = entry_hora.get().strip()
        cliente = entry_cliente.get().strip()
        motivo = entry_motivo.get().strip()
        if fecha and hora and cliente and motivo:
            agenda_citas.append({"cliente": cliente, "fecha": fecha, "hora": hora, "motivo": motivo})
            messagebox.showinfo("Éxito", "Cita agendada.")
            ventana_cita.destroy()
        else:
            messagebox.showwarning("Error", "Completa todos los campos.")

    tk.Button(ventana_cita, text="Agendar", command=guardar_cita, bg=BTN_COLOR, fg=BTN_TEXT).pack(pady=10)

def mostrar_agenda():
    if not agenda_citas:
        messagebox.showinfo("Agenda vacía", "No hay citas registradas.")
        return
    texto = ""
    for cita in agenda_citas:
        texto += f"{cita['fecha']} {cita['hora']} - {cita['cliente']} ({cita['motivo']})\n"
    messagebox.showinfo("Agenda de citas", texto)

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
ventana.title("Bufete de Abogadas — Sistema")
ventana.geometry("500x650")
ventana.configure(bg=BG_COLOR)

# Sección clientes
tk.Label(ventana, text="Registro de Cliente", font=FONT_TITLE, bg=BG_COLOR).pack(pady=10)
entry_nombre = tk.Entry(ventana, width=40)
entry_nombre.pack(pady=2)
entry_nombre.insert(0, "Nombre completo")

entry_dpi = tk.Entry(ventana, width=40)
entry_dpi.pack(pady=2)
entry_dpi.insert(0, "DPI")

entry_telefono = tk.Entry(ventana, width=40)
entry_telefono.pack(pady=2)
entry_telefono.insert(0, "Teléfono")

tk.Button(ventana, text="Registrar Cliente", command=registrar_cliente, bg=BTN_COLOR, fg=BTN_TEXT).pack(pady=5)

# Sección funciones
tk.Label(ventana, text="Gestión del Sistema", font=FONT_TITLE, bg=BG_COLOR).pack(pady=10)

botones = [
    ("Registrar Expediente", registrar_expediente),
    ("Agendar Cita", abrir_agenda_cita),
    ("Mostrar Agenda", mostrar_agenda),
    ("Agregar Tarea Urgente", agregar_tarea),
    ("Atender Tarea Urgente", atender_tarea),
    ("Buscar Expediente por ID", buscar_expediente_hash),
]

for texto, funcion in botones:
    tk.Button(ventana, text=texto, command=funcion, width=40, bg=BTN_COLOR, fg=BTN_TEXT).pack(pady=3)

ventana.mainloop()