# -----------------------
# 1. Hashing — Expedientes
# -----------------------
hash_expedientes = {}

def registrar_expediente_hash(id_exp, cliente, tipo, fecha):
    if id_exp in hash_expedientes:
        print("ID ya existe.")
        return
    expediente = {"id": id_exp, "cliente": cliente, "tipo": tipo, "fecha": fecha}
    hash_expedientes[id_exp] = expediente
    print("Expediente registrado.")

def buscar_expediente_hash(id_exp):
    resultado = hash_expedientes.get(id_exp)
    if resultado:
        print("Expediente encontrado:", resultado)
    else:
        print("No encontrado.")

# -----------------------
# 2. Bubble Sort — Citas
# -----------------------
def bubble_sort_citas(citas):
    n = len(citas)
    for i in range(n):
        for j in range(0, n-i-1):
            if (citas[j]["fecha"], citas[j]["hora"]) > (citas[j+1]["fecha"], citas[j+1]["hora"]):
                citas[j], citas[j+1] = citas[j+1], citas[j]
    return citas

# -----------------------
# 3. Quick Sort — Expedientes por fecha
# -----------------------
def quick_sort_expedientes(lista):
    if len(lista) <= 1:
        return lista
    pivote = lista[0]
    menores = [x for x in lista[1:] if x["fecha"] <= pivote["fecha"]]
    mayores = [x for x in lista[1:] if x["fecha"] > pivote["fecha"]]
    return quick_sort_expedientes(menores) + [pivote] + quick_sort_expedientes(mayores)

# -----------------------
# 4. Recursividad — Atender tareas urgentes
# -----------------------
def atender_tareas_recursivo(tareas):
    if not tareas:
        print("No hay tareas pendientes.")
        return
    actual = tareas.pop()
    print("Atendiendo tarea:", actual)
    atender_tareas_recursivo(tareas)

# -----------------------
# 5. Pila — Tareas urgentes (LIFO)
# -----------------------
pila_tareas = []

def agregar_tarea_pila(descripcion):
    pila_tareas.append(descripcion)
    print("Tarea agregada.")

def atender_tarea_pila():
    if pila_tareas:
        tarea = pila_tareas.pop()
        print("Tarea atendida:", tarea)
    else:
        print("No hay tareas urgentes.")

# -----------------------
# Ejemplo de uso
# -----------------------
if __name__ == "__main__":
    print("=== Hashing ===")
    registrar_expediente_hash(101, "Ana", "Civil", "2023-05-01")
    buscar_expediente_hash(101)

    print("\n=== Bubble Sort ===")
    citas = [
        {"fecha": "2023-05-10", "hora": "14:00"},
        {"fecha": "2023-05-08", "hora": "09:00"},
        {"fecha": "2023-05-08", "hora": "08:00"},
    ]
    ordenadas = bubble_sort_citas(citas)
    for c in ordenadas:
        print(c)

    print("\n=== Quick Sort ===")
    expedientes = [
        {"id": 1, "fecha": "2023-05-10"},
        {"id": 2, "fecha": "2023-04-01"},
        {"id": 3, "fecha": "2023-06-15"},
    ]
    ordenados = quick_sort_expedientes(expedientes)
    for e in ordenados:
        print(e)

    print("\n=== Recursividad ===")
    tareas = ["Revisar contrato", "Llamar cliente", "Enviar informe"]
    atender_tareas_recursivo(tareas)

    print("\n=== Pila ===")
    agregar_tarea_pila("Redactar demanda")
    agregar_tarea_pila("Enviar correo")
    atender_tarea_pila()
    atender_tarea_pila()
    atender_tarea_pila()