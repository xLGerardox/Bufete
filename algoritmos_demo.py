import sqlite3
import os

DB_FILE = "rivera.db"

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        dpi TEXT,
        telefono TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS expedientes (
        id INTEGER PRIMARY KEY,
        cliente TEXT,
        tipo TEXT,
        fecha TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS citas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        fecha TEXT,
        hora TEXT,
        motivo TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT,
        creado_en TEXT DEFAULT (datetime('now','localtime'))
    )""")
    conn.commit()
    conn.close()

# -----------------------
# Funciones
# -----------------------
def registrar_cliente():
    nombre = input("Nombre completo: ").strip()
    dpi = input("DPI: ").strip()
    telefono = input("Teléfono: ").strip()
    if nombre and dpi and telefono:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO clientes (nombre, dpi, telefono) VALUES (?, ?, ?)", (nombre, dpi, telefono))
        conn.commit()
        conn.close()
        print("Cliente registrado.")
    else:
        print("Datos incompletos.")

def registrar_expediente():
    try:
        id_exp = int(input("ID del expediente (número): "))
    except:
        print("ID inválido.")
        return
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM expedientes WHERE id = ?", (id_exp,))
    if cur.fetchone():
        print("Ese ID ya existe.")
        conn.close()
        return
    cliente = input("Nombre del cliente: ").strip()
    tipo = input("Tipo de caso: ").strip()
    fecha = input("Fecha de apertura: ").strip()
    if cliente and tipo and fecha:
        cur.execute("INSERT INTO expedientes (id, cliente, tipo, fecha) VALUES (?, ?, ?, ?)", (id_exp, cliente, tipo, fecha))
        conn.commit()
        conn.close()
        print("Expediente registrado.")
    else:
        print("Datos incompletos.")

def agendar_cita():
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    hora = input("Hora (HH:MM): ").strip()
    cliente = input("Nombre del cliente: ").strip()
    motivo = input("Motivo: ").strip()
    if fecha and hora and cliente and motivo:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO citas (cliente, fecha, hora, motivo) VALUES (?, ?, ?, ?)", (cliente, fecha, hora, motivo))
        conn.commit()
        conn.close()
        print("Cita agendada.")
    else:
        print("Datos incompletos.")

def mostrar_agenda():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM citas ORDER BY fecha, hora")
    citas = cur.fetchall()
    conn.close()
    if not citas:
        print("No hay citas registradas.")
        return
    for c in citas:
        print(f"{c['fecha']} {c['hora']} - {c['cliente']} : {c['motivo']}")

def agregar_tarea():
    descripcion = input("Descripción de la tarea urgente: ").strip()
    if descripcion:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO tareas (descripcion) VALUES (?)", (descripcion,))
        conn.commit()
        conn.close()
        print("Tarea agregada.")
    else:
        print("Descripción vacía.")

def atender_tarea():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, descripcion FROM tareas ORDER BY id LIMIT 1")
    tarea = cur.fetchone()
    if tarea:
        cur.execute("DELETE FROM tareas WHERE id = ?", (tarea["id"],))
        conn.commit()
        conn.close()
        print("Tarea atendida:", tarea["descripcion"])
    else:
        conn.close()
        print("No hay tareas urgentes.")

def buscar_expediente():
    try:
        id_exp = int(input("ID del expediente: "))
    except:
        print("ID inválido.")
        return
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expedientes WHERE id = ?", (id_exp,))
    exp = cur.fetchone()
    conn.close()
    if exp:
        print(f"ID: {exp['id']}\nCliente: {exp['cliente']}\nTipo: {exp['tipo']}\nFecha: {exp['fecha']}")
    else:
        print("Expediente no encontrado.")

# -----------------------
# Algoritmos de ejemplo
# -----------------------
def bubble_sort_demo():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT fecha, hora, cliente FROM citas")
    citas = [dict(row) for row in cur.fetchall()]
    conn.close()
    n = len(citas)
    for i in range(n):
        for j in range(0, n-i-1):
            if (citas[j]["fecha"], citas[j]["hora"]) > (citas[j+1]["fecha"], citas[j+1]["hora"]):
                citas[j], citas[j+1] = citas[j+1], citas[j]
    print("Citas ordenadas (Bubble Sort):")
    for c in citas:
        print(f"{c['fecha']} {c['hora']} - {c['cliente']}")

def quick_sort_expedientes(lista):
    if len(lista) <= 1:
        return lista
    pivote = lista[0]
    menores = [x for x in lista[1:] if x["fecha"] <= pivote["fecha"]]
    mayores = [x for x in lista[1:] if x["fecha"] > pivote["fecha"]]
    return quick_sort_expedientes(menores) + [pivote] + quick_sort_expedientes(mayores)

def quick_sort_demo():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, cliente, tipo, fecha FROM expedientes")
    expedientes = [dict(row) for row in cur.fetchall()]
    conn.close()
    ordenados = quick_sort_expedientes(expedientes)
    print("Expedientes ordenados (Quick Sort):")
    for e in ordenados:
        print(f"{e['fecha']} - {e['cliente']} ({e['tipo']})")

def atender_tareas_recursivo():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, descripcion FROM tareas ORDER BY id DESC")
    tareas = [dict(row) for row in cur.fetchall()]
    conn.close()
    def atender(lista):
        if not lista:
            print("No hay tareas pendientes.")
            return
        actual = lista.pop(0)
        print("Atendiendo tarea:", actual["descripcion"])
        atender(lista)
    atender(tareas)

# -----------------------
# Menú principal
# -----------------------
def menu():
    init_db()
    while True:
        print("\n--- Sistema Rivera & Rivera (Consola) ---")
        print("1. Registrar cliente")
        print("2. Registrar expediente")
        print("3. Agendar cita")
        print("4. Mostrar agenda")
        print("5. Agregar tarea urgente")
        print("6. Atender tarea urgente")
        print("7. Buscar expediente por ID")
        print("8. Bubble Sort de citas")
        print("9. Quick Sort de expedientes")
        print("10. Atender tareas (recursivo)")
        print("0. Salir")
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            registrar_expediente()
        elif opcion == "3":
            agendar_cita()
        elif opcion == "4":
            mostrar_agenda()
        elif opcion == "5":
            agregar_tarea()
        elif opcion == "6":
            atender_tarea()
        elif opcion == "7":
            buscar_expediente()
        elif opcion == "8":
            bubble_sort_demo()
        elif opcion == "9":
            quick_sort_demo()
        elif opcion == "10":
            atender_tareas_recursivo()
        elif opcion == "0":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()