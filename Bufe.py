# SISTEMA DE GESTIÓN PARA BUFETE DE ABOGADAS Gerardo
clientes = []  # Arreglo uni
expedientes = []  # Arreglo multi
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
    fecha = input("Fecha de apertura: ").strip()
    expediente = [id_expediente, nombre_cliente, tipo, fecha]
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

# Busqueda secuencial
def buscar_cliente():
    nombre = input("Nombre del cliente: ").strip()
    for cliente in clientes:
        if cliente["nombre"].lower() == nombre.lower():
            print("Cliente encontrado:", cliente, "\n")
            return
    print("Cliente no encontrado.\n")

# Ordena burbuja
def ordenar_clientes_bubble():
    n = len(clientes)
    for i in range(n):
        for j in range(0, n - i - 1):
            if clientes[j]["nombre"] > clientes[j + 1]["nombre"]:
                clientes[j], clientes[j + 1] = clientes[j + 1], clientes[j]
    print("Clientes ordenados por nombre.\n")

# el menú princiall
def menu():
    while True:
        print("=== BUFETE DE ABOGADAS ===")
        print("1. Registrar cliente")
        print("2. Registrar expediente")
        print("3. Agendar cita")
        print("4. Agregar tarea urgente")
        print("5. Atender tarea urgente")
        print("6. Buscar cliente por nombre")
        print("7. Ordenar clientes por nombre")
        print("0. Salir")
        opcion = input("Seleccione una opción: ").strip()
        print()
        if opcion == "1": registrar_cliente()
        elif opcion == "2": registrar_expediente()
        elif opcion == "3": agendar_cita()
        elif opcion == "4": agregar_tarea()
        elif opcion == "5": atender_tarea()
        elif opcion == "6": buscar_cliente()
        elif opcion == "7": ordenar_clientes_bubble()
        elif opcion == "0":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción inválida.\n")

if __name__ == "__main__":
    menu()