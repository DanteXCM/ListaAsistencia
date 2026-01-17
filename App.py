from flask import Flask, render_template, request, redirect, url_for
import json, os, requests
from datetime import datetime

# Flask looks for a `templates` folder by default. In this project the
# templates are located in `Proyecto/Templates` (capital T), so pass
# `template_folder` explicitly so Flask can find the files.
app = Flask(__name__, template_folder='Templates')

# Configuración del archivo JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASISTENCIA_FILE = os.path.join(BASE_DIR, 'asistencia.json')
TIMEZONE = "America/Mexico_City" # Puedes cambiar tu zona horaria aquí

# --- Funciones Auxiliares para JSON ---

def cargar_registros():
    """Carga la lista de registros de asistencia desde el archivo JSON."""
    if os.path.exists(ASISTENCIA_FILE):
        with open(ASISTENCIA_FILE, "r", encoding="utf-8") as f:
            try:
                contenido = f.read()
                return json.loads(contenido) if contenido else []
            except json.JSONDecodeError:
                return []
    return []

def guardar_registros(registros):
    """Guarda la lista de registros en el archivo JSON."""
    with open(ASISTENCIA_FILE, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=4)

# Cargar registros al inicio
registros = cargar_registros()

# --- Funciones Auxiliares para API ---

def obtener_fecha_hora():
    """Consulta la API de hora mundial para obtener la fecha y hora actual."""
    try:
        url = f"http://worldtimeapi.org/api/timezone/{TIMEZONE}"
        respuesta = requests.get(url, timeout=5)
        respuesta.raise_for_status() # Lanza error para códigos HTTP malos
        datos = respuesta.json()
        
        # El campo datetime incluye fecha, hora y zona horaria
        fecha_hora_str = datos.get('datetime')

        # Intentamos parsear con fromisoformat; la API devuelve un ISO 8601
        # con offset, por lo que `fromisoformat` normalmente lo maneja.
        # Si falla, hacemos fallback a la hora local.
        try:
            dt_objeto = datetime.fromisoformat(fecha_hora_str)
            fecha = dt_objeto.date().isoformat()
            hora = dt_objeto.time().strftime("%H:%M:%S")
            return fecha, hora
        except Exception:
            # Fallback: quitar offset y parsear la parte antes del signo
            s = fecha_hora_str.split('+')[0].split('-')
            # reconstruir la parte con fecha y hora aproximada
            try:
                dt_objeto = datetime.fromisoformat(fecha_hora_str.split('+')[0])
                return dt_objeto.date().isoformat(), dt_objeto.time().strftime("%H:%M:%S")
            except Exception:
                now = datetime.now()
                return now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")
        
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la hora mundial: {e}")
        # Retorna fecha y hora local como fallback si la API falla
        now = datetime.now()
        return now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")

# --- Rutas de Flask ---

@app.route('/')
def index():
    """Muestra todos los registros de asistencia."""
    # Usamos una copia para no modificar la lista global durante el filtrado
    registros_a_mostrar = list(registros)
    
    # Manejar el filtrado por nombre
    filtro_nombre = request.args.get('nombre', '').strip()
    if filtro_nombre:
        registros_a_mostrar = [
            r for r in registros_a_mostrar 
            if filtro_nombre.lower() in r.get('nombre', '').lower()
        ]

    return render_template('index.html', 
                           registros=registros_a_mostrar, 
                           filtro_nombre=filtro_nombre)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    """Registra la asistencia de un alumno."""
    if request.method == 'POST':
        nombre_alumno = request.form.get('nombre')
        
        if nombre_alumno:
            fecha, hora = obtener_fecha_hora()
            
            nuevo_registro = {
                "nombre": nombre_alumno,
                "fecha": fecha,
                "hora_registro": hora,
                "asistio": True # Por defecto, si se registra, asistió
            }
            
            registros.append(nuevo_registro)
            guardar_registros(registros)
            return redirect(url_for('index'))
            
    # The project template for adding is `agregar.html` in `Proyecto/Templates`.
    return render_template('agregar.html')

@app.route('/editar/<int:indice>', methods=['GET', 'POST'])
def editar(indice):
    """Edita el nombre o el estado de asistencia de un registro."""
    if not (0 <= indice < len(registros)):
        return redirect(url_for('index'))

    registro = registros[indice]

    if request.method == 'POST':
        # Permite actualizar nombre, fecha (opcional) y estado de asistencia
        registro['nombre'] = request.form.get('nombre')
        registro['fecha'] = request.form.get('fecha')
        registro['asistio'] = request.form.get('asistio') == 'True'
        
        guardar_registros(registros)
        return redirect(url_for('index'))

    return render_template('editar.html', indice=indice, registro=registro)

@app.route('/eliminar/<int:indice>')
def eliminar(indice):
    """Elimina un registro de asistencia."""
    if 0 <= indice < len(registros):
        registros.pop(indice)
        guardar_registros(registros)
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)