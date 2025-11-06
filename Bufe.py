import tkinter as tk
from tkinter import simpledialog, messagebox
import hashlib

# Estructuras de datos
clientes = []
expedientes = []
agenda_citas = []
tareas_urgentes = []

# Funciones base
def generar_hash_expediente(expediente):
    contenido = f"{expediente['id']}{expediente['cliente']}{expediente['tipo']}{expediente['fecha']}"
    return hashlib.md5(contenido.encode()).hexdigest()

def registrar_cliente():
    nombre = simpledialog.askstring("Cliente", "Nombre completo:")
    dpi = simpledialog.askstring("Cliente", "DPI:")
    telefono = simpledialog.askstring("Cliente", "Teléfono:")
    if nombre and dpi and telefono:
        clientes.append({"nombre": nombre, "dpi": dpi, "telefono": telefono})
        messagebox.showinfo("OK", "Cliente registrado.")

def registrar_expediente():
    id_expediente = simpledialog.askstring("Expediente", "ID:")
    nombre_cliente = simpledialog.askstring("Expediente", "Nombre del cliente:")
    tipo = simpledialog.askstring("Expediente", "Tipo de caso:")
    fecha = simpledialog.askstring("Expediente", "Fecha (YYYY-MM-DD):")
    if id_expediente and nombre_cliente and tipo and fecha:
        expediente = {
            "id": id_expediente,
            "cliente": nombre_cliente,
            "tipo": tipo,
            "fecha": fecha
        }
        expediente["hash"] = generar_hash_expediente(expediente)
        expedientes.append(expediente)
        messagebox.showinfo("OK", "Expediente registrado.")

def agendar_cita():
    nombre = simpledialog.askstring("Cita", "Nombre del cliente:")
    fecha = simpledialog.askstring("Cita", "Fecha:")
    hora = simpledialog.askstring("Cita", "Hora:")
    motivo = simpledialog.askstring("Cita", "Motivo:")
    if nombre and fecha and hora and motivo:
        agenda_citas.append({"cliente": nombre, "fecha": fecha, "hora": hora, "motivo": motivo})
        messagebox.showinfo("OK", "Cita agendada.")

def agregar_tarea():
    tarea = simpledialog.askstring("Tarea urgente", "Descripción:")
    if tarea:
        tareas_urgentes.append(tarea)
        messagebox.showinfo("OK", "Tarea agregada.")

def atender_tarea():
    if tareas_urgentes:
        tarea = tareas_urgentes.pop()
        messagebox.showinfo("Tarea atendida", tarea)
    else:
        messagebox.showinfo("Sin tareas", "No hay tareas urgentes.")

def buscar_cliente_binaria():
    nombre = simpledialog.askstring("Buscar cliente", "Nombre:")
    lista_ordenada = sorted(clientes, key=lambda x: x["nombre"])
    izquierda, derecha = 0, len(lista_ordenada) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        actual = lista_ordenada[medio]["nombre"]
        if actual.lower() == nombre.lower():
            messagebox.showinfo("Cliente encontrado", str(lista_ordenada[medio]))
            return
        elif actual.lower() < nombre.lower():
            izquierda = medio + 1
        else:
            derecha = medio - 1
    messagebox.showinfo("No encontrado", "Cliente no registrado.")

def ordenar_expedientes_por_cliente_burbuja():
    n = len(expedientes)
    for i in range(n):
        for j in range(0, n - i - 1):
            if expedientes[j]["cliente"] > expedientes[j + 1]["cliente"]:
                expedientes[j], expedientes[j + 1] = expedientes[j + 1], expedientes[j]
    resultado = "\n".join(str(e) for e in expedientes)
    messagebox.showinfo("Ordenados por cliente", resultado)

def ordenar_expedientes_por_tipo():
    lista = expedientes.copy()
    n = len(lista)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = lista[i]
            j = i
            while j >= gap and lista[j - gap]["tipo"] > temp["tipo"]:
                lista[j] = lista[j - gap]
                j -= gap
            lista[j] = temp
        gap //= 2
    resultado = "\n".join(str(e) for e in lista)
    messagebox.showinfo("Ordenados por tipo", resultado)

def ordenar_expedientes_por_fecha(lista):
    if len(lista) <= 1:
        return lista
    pivote = lista[0]
    menores = [x for x in lista[1:] if x["fecha"] <= pivote["fecha"]]
    mayores = [x for x in lista[1:] if x["fecha"] > pivote["fecha"]]
    return ordenar_expedientes_por_fecha(menores) + [pivote] + ordenar_expedientes_por_fecha(mayores)

def mostrar_expedientes_ordenados_por_fecha():
    ordenados = ordenar_expedientes_por_fecha(expedientes.copy())
    resultado = "\n".join(str(e) for e in ordenados)
    messagebox.showinfo("Ordenados por fecha", resultado)

def contar_tipo():
    tipo = simpledialog.askstring("Contar expedientes", "Tipo de caso:")
    def contar(i=0):
        if i >= len(expedientes): return 0
        return (1 if expedientes[i]["tipo"].lower() == tipo.lower() else 0) + contar(i + 1)
    total = contar()
    messagebox.showinfo("Total", f"Expedientes tipo '{tipo}': {total}")

def verificar_integridad():
    id_buscar = simpledialog.askstring("Verificar expediente", "ID:")
    encontrado = next((e for e in expedientes if e["id"] == id_buscar), None)
    if encontrado:
        actual = generar_hash_expediente(encontrado)
        estado = "Íntegro" if actual == encontrado["hash"] else "Modificado"
        messagebox.showinfo("Resultado", estado)
    else:
        messagebox.showinfo("No encontrado", "Expediente no existe.")

# Interfaz básica
ventana = tk.Tk()
ventana.title("Bufete de Abogadas — Versión Técnica")

opciones = [
    ("Registrar cliente", registrar_cliente),
    ("Registrar expediente", registrar_expediente),
    ("Agendar cita", agendar_cita),
    ("Agregar tarea urgente", agregar_tarea),
    ("Atender tarea urgente", atender_tarea),
    ("Buscar cliente por nombre (binaria)", buscar_cliente_binaria),
    ("Ordenar expedientes por nombre del cliente (burbuja)", ordenar_expedientes_por_cliente_burbuja),
    ("Ordenar expedientes por tipo (Shell Sort)", ordenar_expedientes_por_tipo),
    ("Ordenar expedientes por fecha (Quick Sort)", mostrar_expedientes_ordenados_por_fecha),
    ("Contar expedientes por tipo (recursivo)", contar_tipo),
    ("Verificar integridad de expediente (hashing)", verificar_integridad),
]

for texto, funcion in opciones:
    tk.Button(ventana, text=texto, command=funcion).pack(fill="x", padx=10, pady=2)

ventana.mainloop()