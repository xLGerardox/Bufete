import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import Calendar
import sqlite3
import os

# BASE DE DATOS (SQLite)
DB_FILE = "rivera.db"

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    # clientes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        dpi TEXT,
        telefono TEXT
    )""")
    # expedientes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expedientes (
        id INTEGER PRIMARY KEY,
        cliente TEXT,
        tipo TEXT,
        fecha TEXT
    )""")
    # citas (agenda)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS citas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        fecha TEXT,
        hora TEXT,
        motivo TEXT
    )""")
    # tareas urgentes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT,
        creado_en TEXT DEFAULT (datetime('now','localtime'))
    )""")
    conn.commit()
    conn.close()

def db_add_cliente(nombre, dpi, telefono):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO clientes (nombre, dpi, telefono) VALUES (?, ?, ?)",
                (nombre, dpi, telefono))
    conn.commit()
    conn.close()

def db_count(table):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) as c FROM {table}")
    r = cur.fetchone()
    conn.close()
    return r["c"]

def db_add_expediente(id_exp, cliente, tipo, fecha):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO expedientes (id, cliente, tipo, fecha) VALUES (?, ?, ?, ?)",
                (id_exp, cliente, tipo, fecha))
    conn.commit()
    conn.close()

def db_add_cita(cliente, fecha, hora, motivo):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO citas (cliente, fecha, hora, motivo) VALUES (?, ?, ?, ?)",
                (cliente, fecha, hora, motivo))
    conn.commit()
    conn.close()

def db_list_citas():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM citas ORDER BY fecha, hora")
    rows = cur.fetchall()
    conn.close()
    return rows

def db_add_tarea(descripcion):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO tareas (descripcion) VALUES (?)", (descripcion,))
    conn.commit()
    conn.close()

def db_pop_tarea():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, descripcion FROM tareas ORDER BY id LIMIT 1")
    row = cur.fetchone()
    if row:
        cur.execute("DELETE FROM tareas WHERE id = ?", (row["id"],))
        conn.commit()
        descripcion = row["descripcion"]
        conn.close()
        return descripcion
    conn.close()
    return None

def db_find_expediente(id_exp):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expedientes WHERE id = ?", (id_exp,))
    row = cur.fetchone()
    conn.close()
    return row

# Estilos / Apariencia
BG_COLOR = "#0b1f3f"
CARD_COLOR = "#ffffff"
ENTRY_COLOR = "#f2f2f2"
BTN_COLOR = "#dfe6e9"
BTN_TEXT = "#2d3436"
ACCENT_OK = "#27ae60"
ACCENT_CANCEL = "#e74c3c"
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_CARD_TITLE = ("Segoe UI", 12, "bold")
FONT_NORMAL = ("Segoe UI", 10)

# Entradas
def placeholder_bind(entry, placeholder):
    def on_focus_in(e):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")
    def on_focus_out(e):
        if entry.get().strip() == "":
            entry.insert(0, placeholder)
            entry.config(fg="gray")
    entry.insert(0, placeholder)
    entry.config(fg="gray")
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# Funciones
def actualizar_indicadores():
    lbl_clientes_count.config(text=f"Clientes: {db_count('clientes')}")
    lbl_expedientes_count.config(text=f"Expedientes: {db_count('expedientes')}")
    lbl_citas_count.config(text=f"Citas: {db_count('citas')}")
    lbl_tareas_count.config(text=f"Tareas: {db_count('tareas')}")

def registrar_cliente_from_modal(entries, modal):
    nombre = entries['nombre'].get().strip()
    dpi = entries['dpi'].get().strip()
    telefono = entries['telefono'].get().strip()
    if nombre and dpi and telefono and nombre != "Nombre completo" and dpi != "DPI" and telefono != "Teléfono":
        db_add_cliente(nombre, dpi, telefono)
        messagebox.showinfo("Éxito", f"Cliente {nombre} registrado.")
        modal.destroy()
        actualizar_indicadores()
    else:
        messagebox.showwarning("Error", "Completa todos los campos.")

def abrir_modal_registrar_cliente():
    modal = tk.Toplevel(ventana)
    modal.transient(ventana)
    modal.grab_set()
    modal.title("Agregar Cliente")
    modal.configure(bg=BG_COLOR)
    modal.geometry("420x260")
    frame = tk.Frame(modal, bg=CARD_COLOR, padx=12, pady=12)
    frame.place(relx=0.5, rely=0.5, anchor="c")

    tk.Label(frame, text="Registrar Cliente", font=FONT_CARD_TITLE, bg=CARD_COLOR).pack(anchor="w", pady=(0,8))

    e_nombre = tk.Entry(frame, width=40, bg=ENTRY_COLOR)
    e_dpi = tk.Entry(frame, width=40, bg=ENTRY_COLOR)
    e_tel = tk.Entry(frame, width=40, bg=ENTRY_COLOR)
    for e, ph in ((e_nombre,"Nombre completo"), (e_dpi,"DPI"), (e_tel,"Teléfono")):
        placeholder_bind(e, ph)
        e.pack(pady=6)

    botones = tk.Frame(frame, bg=CARD_COLOR)
    botones.pack(pady=(8,0), anchor="e")
    tk.Button(botones, text="Registrar", bg=ACCENT_OK, fg="white", width=10,
              command=lambda: registrar_cliente_from_modal({'nombre':e_nombre,'dpi':e_dpi,'telefono':e_tel}, modal)).pack(side="left", padx=6)
    tk.Button(botones, text="Cancelar", bg=ACCENT_CANCEL, fg="white", width=10,
              command=modal.destroy).pack(side="left", padx=6)

def registrar_expediente_dialog():
    modal = tk.Toplevel(ventana)
    modal.transient(ventana)
    modal.grab_set()
    modal.title("Registrar Expediente")
    modal.configure(bg=BG_COLOR)
    modal.geometry("420x300")
    frame = tk.Frame(modal, bg=CARD_COLOR, padx=12, pady=12)
    frame.place(relx=0.5, rely=0.5, anchor="c")

    tk.Label(frame, text="Registrar Expediente", font=FONT_CARD_TITLE, bg=CARD_COLOR).pack(anchor="w", pady=(0,8))
    e_id = tk.Entry(frame, width=40, bg=ENTRY_COLOR)
    e_cliente = tk.Entry(frame, width=40, bg=ENTRY_COLOR)
    e_tipo = tk.Entry(frame, width=40, bg=ENTRY_COLOR)
    e_fecha = tk.Entry(frame, width=40, bg=ENTRY_COLOR)
    for e, ph in ((e_id,"ID numérico"), (e_cliente,"Nombre del cliente"), (e_tipo,"Tipo de caso"), (e_fecha,"Fecha (YYYY-MM-DD)")):
        placeholder_bind(e, ph)
        e.pack(pady=6)

    def guardar():
        try:
            id_exp = int(e_id.get().strip())
        except:
            messagebox.showwarning("Error", "ID inválido")
            return
        if db_find_expediente(id_exp) is not None:
            messagebox.showwarning("Error", "Ese ID ya existe.")
            return
        cliente = e_cliente.get().strip()
        tipo = e_tipo.get().strip()
        fecha = e_fecha.get().strip()
        if cliente and tipo and fecha:
            db_add_expediente(id_exp, cliente, tipo, fecha)
            messagebox.showinfo("Éxito", "Expediente registrado.")
            modal.destroy()
            actualizar_indicadores()
        else:
            messagebox.showwarning("Error", "Datos incompletos.")

    botones = tk.Frame(frame, bg=CARD_COLOR)
    botones.pack(pady=(8,0), anchor="e")
    tk.Button(botones, text="Guardar", bg=ACCENT_OK, fg="white", width=10, command=guardar).pack(side="left", padx=6)
    tk.Button(botones, text="Cancelar", bg=ACCENT_CANCEL, fg="white", width=10, command=modal.destroy).pack(side="left", padx=6)

def abrir_modal_agendar_cita():
    modal = tk.Toplevel(ventana)
    modal.transient(ventana)
    modal.grab_set()
    modal.title("Agendar Cita")
    modal.configure(bg=BG_COLOR)
    modal.geometry("480x420")
    frame = tk.Frame(modal, bg=CARD_COLOR, padx=12, pady=12)
    frame.place(relx=0.5, rely=0.5, anchor="c")

    tk.Label(frame, text="Agendar Cita", font=FONT_CARD_TITLE, bg=CARD_COLOR).pack(anchor="w", pady=(0,8))

    cal_widget = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd')
    cal_widget.pack(pady=6)

    e_hora = tk.Entry(frame, width=40, bg=ENTRY_COLOR)
    e_cliente = tk.Entry(frame, width=40, bg=ENTRY_COLOR)
    e_motivo = tk.Entry(frame, width=40, bg=ENTRY_COLOR)
    for e, ph in ((e_hora,"Hora (HH:MM)"), (e_cliente,"Cliente"), (e_motivo,"Motivo")):
        placeholder_bind(e, ph)
        e.pack(pady=6)

    def guardar():
        fecha = cal_widget.get_date()
        hora = e_hora.get().strip()
        cliente = e_cliente.get().strip()
        motivo = e_motivo.get().strip()
        if fecha and hora and cliente and motivo and hora != "Hora (HH:MM)":
            db_add_cita(cliente, fecha, hora, motivo)
            messagebox.showinfo("Éxito", "Cita agendada.")
            modal.destroy()
            actualizar_indicadores()
        else:
            messagebox.showwarning("Error", "Completa todos los campos.")

    botones = tk.Frame(frame, bg=CARD_COLOR)
    botones.pack(pady=(8,0), anchor="e")
    tk.Button(botones, text="Agendar", bg=ACCENT_OK, fg="white", width=10, command=guardar).pack(side="left", padx=6)
    tk.Button(botones, text="Cancelar", bg=ACCENT_CANCEL, fg="white", width=10, command=modal.destroy).pack(side="left", padx=6)

def mostrar_agenda_popup():
    rows = db_list_citas()
    if not rows:
        messagebox.showinfo("Agenda", "No hay citas registradas.")
        return
    texto = ""
    for c in rows:
        texto += f"{c['fecha']} {c['hora']} - {c['cliente']} : {c['motivo']}\n"
    messagebox.showinfo("Agenda", texto)

def agregar_tarea_dialog():
    tarea = simpledialog.askstring("Tarea urgente", "Descripción:")
    if tarea:
        db_add_tarea(tarea)
        messagebox.showinfo("Éxito", "Tarea agregada.")
        actualizar_indicadores()

def atender_tarea_action():
    tarea = db_pop_tarea()
    if tarea:
        messagebox.showinfo("Tarea atendida", f"Se atendió: {tarea}")
        actualizar_indicadores()
    else:
        messagebox.showinfo("Tareas", "No hay tareas urgentes.")

def buscar_expediente_dialog():
    res = simpledialog.askstring("Buscar expediente", "ID del expediente:")
    if res is None:
        return
    try:
        id_exp = int(res)
    except:
        messagebox.showwarning("Error", "ID inválido")
        return
    row = db_find_expediente(id_exp)
    if row:
        messagebox.showinfo("Expediente encontrado", f"ID: {row['id']}\nCliente: {row['cliente']}\nTipo: {row['tipo']}\nFecha: {row['fecha']}")
    else:
        messagebox.showinfo("No encontrado", "Expediente no registrado.")

# ventana principal
init_db()
ventana = tk.Tk()
ventana.title("Rivera & Rivera — Sistema de Gestión")
ventana.geometry("900x700")
ventana.configure(bg=BG_COLOR)
ventana.minsize(800, 600)

# Cabecera
cabecera = tk.Frame(ventana, bg=BG_COLOR)
cabecera.pack(fill="x", pady=16)
tk.Label(cabecera, text="Rivera & Rivera", font=FONT_TITLE, bg=BG_COLOR, fg="white").pack()

# Indicadores superiores
indicadores = tk.Frame(ventana, bg=BG_COLOR)
indicadores.pack(fill="x", padx=24, pady=(8,12))

lbl_clientes_count = tk.Label(indicadores, text="Clientes: 0", bg=CARD_COLOR, font=FONT_NORMAL, width=18, padx=10, pady=8)
lbl_expedientes_count = tk.Label(indicadores, text="Expedientes: 0", bg=CARD_COLOR, font=FONT_NORMAL, width=18, padx=10, pady=8)
lbl_citas_count = tk.Label(indicadores, text="Citas: 0", bg=CARD_COLOR, font=FONT_NORMAL, width=18, padx=10, pady=8)
lbl_tareas_count = tk.Label(indicadores, text="Tareas: 0", bg=CARD_COLOR, font=FONT_NORMAL, width=18, padx=10, pady=8)

lbl_clientes_count.pack(side="left", padx=8)
lbl_expedientes_count.pack(side="left", padx=8)
lbl_citas_count.pack(side="left", padx=8)
lbl_tareas_count.pack(side="left", padx=8)

# tarjetas de aviso
dashboard = tk.Frame(ventana, bg=BG_COLOR)
dashboard.pack(fill="both", expand=True, padx=24, pady=8)

def crear_tarjeta(parent, titulo, descripcion, boton_text, comando):
    tarjeta = tk.Frame(parent, bg=CARD_COLOR, bd=1, relief="solid", padx=14, pady=12)
    tk.Label(tarjeta, text=titulo, font=FONT_CARD_TITLE, bg=CARD_COLOR).pack(anchor="w")
    tk.Label(tarjeta, text=descripcion, font=FONT_NORMAL, bg=CARD_COLOR, fg="#555555").pack(anchor="w", pady=(6,12))
    tk.Button(tarjeta, text=boton_text, bg=BTN_COLOR, fg=BTN_TEXT, font=FONT_NORMAL, command=comando).pack(anchor="e")
    return tarjeta

tar1 = crear_tarjeta(dashboard, "Clientes", "Registrar y ver clientes", "Abrir", abrir_modal_registrar_cliente)
tar2 = crear_tarjeta(dashboard, "Expedientes", "Crear expediente nuevo", "Crear", registrar_expediente_dialog)
tar3 = crear_tarjeta(dashboard, "Agenda", "Ver y agendar citas", "Agenda", abrir_modal_agendar_cita)
tar4 = crear_tarjeta(dashboard, "Tareas", "Agregar o atender tareas urgentes", "Tareas", agregar_tarea_dialog)
tar5 = crear_tarjeta(dashboard, "Buscar", "Buscar expediente por ID", "Buscar", buscar_expediente_dialog)
tar6 = crear_tarjeta(dashboard, "Ver agenda", "Listado de citas agendadas", "Ver", mostrar_agenda_popup)

tar1.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")
tar2.grid(row=0, column=1, padx=12, pady=12, sticky="nsew")
tar3.grid(row=0, column=2, padx=12, pady=12, sticky="nsew")
tar4.grid(row=1, column=0, padx=12, pady=12, sticky="nsew")
tar5.grid(row=1, column=1, padx=12, pady=12, sticky="nsew")
tar6.grid(row=1, column=2, padx=12, pady=12, sticky="nsew")

for c in range(3):
    dashboard.grid_columnconfigure(c, weight=1)

actualizar_indicadores()

ventana.mainloop()