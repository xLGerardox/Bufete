import hashlib

# Estructuras de datos
clientes = []  # Arreglo unidimensional
expedientes = []  # Arreglo multidimensional
agenda_citas = []  # Cola
tareas_urgentes = []  # Pila

# REGISTRO
def registrar_cliente():
    nombre = input("Nombre completo: ").strip()
    dpi = input("DPI: ").strip()
    telefono = input("Teléfono: ").strip()
    clientes.append({"nombre": nombre, "dpi": dpi, "telefono": telefono})
    print("Cliente registrado.\n")

def registrar_expediente():
    id_expediente = input("ID del expediente: ").strip()
    nombre_cliente = input("Nombre del cliente: ").strip()
    tipo = input("Tipo de caso: ").strip()
    fecha = input("Fecha de apertura (YYYY-MM-DD): ").strip()
    expediente = {
        "id": id_expediente,
        "cliente": nombre_cliente,
        "tipo": tipo,
        "fecha": fecha
    }
    expediente["hash"] = generar_hash_expediente(expediente)
    expedientes.append(expediente)
    print("Expediente registrado.\n")

def agendar_cita():
    nombre = input("Nombre del cliente: ").strip()
    fecha = input("Fecha: ").strip()
    hora = input("Hora: ").strip()
    motivo = input("Motivo de la cita: ").strip()
    agenda_citas.append({"cliente": nombre, "fecha": fecha, "hora": hora, "motivo": motivo})
    print("Cita agendada.\n")

def agregar_tarea():
    tarea = input("Descripción de la tarea urgente: ").strip()
    tareas_urgentes.append(tarea)
    print("Tarea agregada.\n")

def atender_tarea():
    if tareas_urgentes:
        print("Tarea atendida:", tareas_urgentes.pop(), "\n")
    else:
        print("No hay tareas urgentes.\n")

# Hashing para integridad de los expedientes
def generar_hash_expediente(expediente):
    contenido = f"{expediente['id']}{expediente['cliente']}{expediente['tipo']}{expediente['fecha']}"
    return hashlib.md5(contenido.encode()).hexdigest()

def verificar_integridad():
    id_buscar = input("ID del expediente a verificar: ").strip()
    encontrado = next((e for e in expedientes if e["id"] == id_buscar), None)
    if encontrado:
        actual = generar_hash_expediente(encontrado)
        print("Íntegro.\n" if actual == encontrado["hash"] else "Modificado.\n")
    else:
        print("Expediente no encontrado.\n")

# Búsqueda binaria por cliente
def buscar_cliente_binaria():
    nombre = input("Nombre del cliente: ").strip()
    lista_ordenada = sorted(clientes, key=lambda x: x["nombre"])
    izquierda, derecha = 0, len(lista_ordenada) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        actual = lista_ordenada[medio]["nombre"]
        if actual.lower() == nombre.lower():
            print("Cliente encontrado:", lista_ordenada[medio], "\n")
            return
        elif actual.lower() < nombre.lower():
            izquierda = medio + 1
        else:
            derecha = medio - 1
    print("Cliente no encontrado.\n")

# Recursividad para contar expedientes por tipo
def contar_expedientes_por_tipo(tipo, i=0):
    if i >= len(expedientes):
        return 0
    return (1 if expedientes[i]["tipo"].lower() == tipo.lower() else 0) + contar_expedientes_por_tipo(tipo, i + 1)

def contar_tipo():
    tipo = input("Tipo de expediente a contar: ").strip()
    total = contar_expedientes_por_tipo(tipo)
    print(f"Total de expedientes tipo '{tipo}': {total}\n")

# Ordenamiento por tipo (Shell Sort)
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
    print("Expedientes ordenados por tipo:")
    for e in lista:
        print(e)
    print()

# Ordenamiento por fecha (Quick Sort)
def ordenar_expedientes_por_fecha(lista):
    if len(lista) <= 1:
        return lista
    pivote = lista[0]
    menores = [x for x in lista[1:] if x["fecha"] <= pivote["fecha"]]
    mayores = [x for x in lista[1:] if x["fecha"] > pivote["fecha"]]
    return ordenar_expedientes_por_fecha(menores) + [pivote] + ordenar_expedientes_por_fecha(mayores)

def mostrar_expedientes_ordenados_por_fecha():
    ordenados = ordenar_expedientes_por_fecha(expedientes.copy())
    print("Expedientes ordenados por fecha:")
    for e in ordenados:
        print(e)
    print()

# Ordenamiento burbuja por nombre del cliente (reubicado)
def ordenar_expedientes_por_cliente_burbuja():
    n = len(expedientes)
    for i in range(n):
        for j in range(0, n - i - 1):
            if expedientes[j]["cliente"] > expedientes[j + 1]["cliente"]:
                expedientes[j], expedientes[j + 1] = expedientes[j + 1], expedientes[j]
    print("Expedientes ordenados por nombre del cliente:")
    for e in expedientes:
        print(e)
    print()

# MENÚ PRINCIPAL
def menu():
    while True:
        print("=== BUFETE DE ABOGADAS ===")
        print("1. Registrar cliente")
        print("2. Registrar expediente")
        print("3. Agendar cita")
        print("4. Agregar tarea urgente")
        print("5. Atender tarea urgente")
        print("6. Buscar cliente por nombre (binaria)")
        print("7. Ordenar expedientes por nombre del cliente (burbuja)")
        print("8. Ordenar expedientes por tipo (Shell Sort)")
        print("9. Ordenar expedientes por fecha (Quick Sort)")
        print("10. Contar expedientes por tipo (recursivo)")
        print("11. Verificar integridad de expediente (hashing)")
        print("0. Salir")
        opcion = input("Seleccione una opción: ").strip()
        print()
        if opcion == "1": registrar_cliente()
        elif opcion == "2": registrar_expediente()
        elif opcion == "3": agendar_cita()
        elif opcion == "4": agregar_tarea()
        elif opcion == "5": atender_tarea()
        elif opcion == "6": buscar_cliente_binaria()
        elif opcion == "7": ordenar_expedientes_por_cliente_burbuja()
        elif opcion == "8": ordenar_expedientes_por_tipo()
        elif opcion == "9": mostrar_expedientes_ordenados_por_fecha()
        elif opcion == "10": contar_tipo()
        elif opcion == "11": verificar_integridad()
        elif opcion == "0":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción inválida.\n")

if __name__ == "__main__":
    menu()