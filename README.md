# Sistema de Lista de Asistencia

Este es un proyecto sencillo desarrollado en **Python** para gestionar el registro de asistencia. Utiliza una arquitectura web ligera y almacena la información de manera local en un formato estructurado.

## Características
- **Registro de asistencia:** Permite capturar los datos de los asistentes.
- **Persistencia de datos:** Los registros se guardan en un archivo `asistencia.json`, lo que facilita su lectura y portabilidad.
- **Interfaz Web:** Utiliza plantillas HTML para interactuar con el usuario de forma visual.

## Tecnologías utilizadas
* **Lenguaje:** [Python](https://www.python.org/)
* **Framework Web:** [Flask](https://flask.palletsprojects.com/) (basado en la estructura de `App.py` y `Templates`)
* **Almacenamiento:** JSON

## 📂 Estructura del Proyecto
- `App.py`: Archivo principal que contiene la lógica del servidor y las rutas.
- `Templates/`: Carpeta que contiene las vistas HTML del sistema.
- `asistencia.json`: Base de datos local en formato JSON.
- `__pycache__/`: Archivos de caché de Python (optimización).

## 💻 Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/DanteXCM/ListaAsistencia.git](https://github.com/DanteXCM/ListaAsistencia.git)
   cd ListaAsistencia
