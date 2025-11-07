# Sistema de Gestión Jurídica — Rivera & Rivera

## Descripción
Este sistema es una aplicación de escritorio desarrollada en Python con interfaz gráfica (`tkinter`) y persistencia de datos mediante SQLite. Está diseñado para gestionar clientes, expedientes, citas y tareas urgentes en un bufete jurídico. El sistema combina funcionalidad práctica con estructuras algorítmicas como hashing, ordenamiento, recursividad y pilas.

## Características principales
- **Interfaz gráfica** con tarjetas visuales por módulo.
- **Registro de clientes** con validación y almacenamiento persistente.
- **Gestión de expedientes** con identificación única y búsqueda por ID.
- **Agenda de citas** con calendario interactivo (`tkcalendar`) y ordenamiento automático.
- **Manejo de tareas urgentes** como pila (LIFO).
- **Búsqueda de expedientes** por ID con acceso directo (hashing).
- **Persistencia real** con base de datos SQLite (`rivera.db`).
- **Estructuras algorítmicas integradas**: hashing, bubble sort, quick sort, recursividad, pilas.

## Requisitos
- Python
- Paquetes:
  - `tkinter` (incluido en Python)
  - `tkcalendar` → instalar con `pip install tkcalendar`

## Estructura del sistema
Bufe.py              # Archivo principal
rivera.db            # Base de datos SQLite (se crea automáticamente)
README.md            # Este documento

## Algoritmos y estructuras aplicadas
| Estructura / Algoritmo | Aplicación en el sistema |
|------------------------|--------------------------|
| Hashing                | Expedientes indexados por ID para búsqueda rápida |
| Bubble Sort            | Ordenamiento de citas por fecha/hora              |
| Quick Sort             | Alternativa demostrativa para ordenar expedientes |
| Recursividad           | Atención de tareas urgentes en cadena             |
| Pilas (LIFO)           | Manejo de tareas urgentes                         |

## Módulos funcionales
- **Clientes**: registro con nombre, DPI y teléfono.
- **Expedientes**: ID único, cliente, tipo de caso, fecha.
- **Agenda**: citas con fecha, hora, cliente y motivo.
- **Tareas urgentes**: ingreso y atención secuencial.
- **Búsqueda**: expedientes por ID con respuesta inmediata.

## Base de datos
El sistema utiliza SQLite. Las tablas se crean automáticamente:
- `clientes(id, nombre, dpi, telefono)`
- `expedientes(id, cliente, tipo, fecha)`
- `citas(id, cliente, fecha, hora, motivo)`
- `tareas(id, descripcion, creado_en)`

## Justificación académica

Este proyecto cumple con los requisitos del curso al integrar:
- Estructuras de datos (listas, pilas, diccionarios)
- Algoritmos clásicos (ordenamiento, recursividad)
- Persistencia de datos

## Créditos
Desarrollado por Luis Gerardo Tucux Rivera 1513423