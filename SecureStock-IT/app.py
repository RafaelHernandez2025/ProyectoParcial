from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from database import obtener_inventario_analitico
import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = 'SecureStock_IT_Ultra_Secret_Key_2026'

# Base de datos simulada unificada (Clientes y Empleados)
USUARIOS_SISTEMA = {
    "gerencia@securestock.com": {
        "password": "admin123", 
        "nombre": "Saeed Quintanilla (Propietario)", 
        "rol": "Rol_Gerencia_Propietario",
        "tipo": "interno"
    },
    "almacen@securestock.com": {
        "password": "admin123", 
        "nombre": "Carlos Almacén", 
        "rol": "Rol_Inventario",
        "tipo": "interno"
    },
    "tecnico@securestock.com": {
        "password": "admin123", 
        "nombre": "Jeyson Técnico", 
        "rol": "Rol_Servicio_Tecnico",
        "tipo": "interno"
    },
    "cliente@gmail.com": {
        "password": "user123",
        "nombre": "Cliente Frecuente",
        "rol": "Cliente_General",
        "tipo": "externo"
    }
}

@app.route('/')
def index_publico():
    df = obtener_inventario_analitico()
    componentes = df.to_dict(orient='records')
    return render_template('public_index.html', componentes=componentes, usuario=session.get('usuario'))

@app.route('/login', methods=['POST'])
def login_universal():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        return redirect(url_for('index_publico', error="Campos vacíos"))
        
    user = USUARIOS_SISTEMA.get(email)
    if user and user['password'] == password:
        session['usuario'] = {
            'email': email,
            'nombre': user['nombre'],
            'rol': user['rol'],
            'tipo': user['tipo']
        }
        # Redirección inteligente automática según el tipo de cuenta
        if user['tipo'] == 'interno':
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('index_publico'))
    else:
        return redirect(url_for('index_publico', error="Credenciales inválidas"))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index_publico'))

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session or session['usuario']['tipo'] != 'interno':
        return redirect(url_for('index_publico'))
    return render_template('dashboard.html', usuario=session.get('usuario'))

@app.route('/api/inventario')
def api_inventario():
    df = obtener_inventario_analitico()
    return jsonify(df.to_dict(orient='records'))

@app.route('/sobre-nosotros')
def sobre_nosotros():
    return render_template('sobre_nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/seguridad')
def seguridad():
    return render_template('seguridad.html')

@app.route('/terminos')
def terminos():
    return render_template('terminos.html')

@app.route('/servicio/recepcion')
def servicio_recepcion():
    return render_template('servicio_recepcion.html')

@app.route('/servicio/diagnostico')
def servicio_diagnostico():
    return render_template('servicio_diagnostico.html')

@app.route('/servicio/inventario-qr')
def servicio_inventario():
    return render_template('servicio_inventario.html')

@app.route('/api/registrar-admision', methods=['POST'])
def registrar_admision():
    """Recibe los datos del formulario real de recepción y prepara la inserción a BD."""
    datos = request.form
    cliente = datos.get('cliente')
    equipo = datos.get('equipo')
    serial = datos.get('serial')
    falla = datos.get('falla')
    
    # Aquí es donde, al conectar la BD real, se hará el INSERT con pymssql
    return jsonify({
        "status": "success",
        "mensaje": f"Equipo {equipo} (S/N: {serial}) registrado correctamente en el sistema para el cliente {cliente}. Datos listos para persistencia SQL Server."
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)