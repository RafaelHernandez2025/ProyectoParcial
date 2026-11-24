
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

import re


# Módulo de inicio de sesión

auth = Blueprint("auth", __name__)


# Usuarios de prueba

usuarios = {
    "almacen@securestock.com": {
        "nombre": "Usuario de Almacén",
        "password": generate_password_hash("admin123"),
        "rol": "almacen"
    },

    "gerencia@securestock.com": {
        "nombre": "Usuario de Gerencia",
        "password": generate_password_hash("admin123"),
        "rol": "gerencia"
    }
}


# Inicio de sesión

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":

        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()

    password = request.form.get("password", "")

    # Validar campos vacíos

    if not email or not password.strip():

        return render_template(
            "login.html",
            error="Todos los campos son obligatorios."
        )

    # Validar correo electrónico

    formato = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

    if not re.fullmatch(formato, email):

        return render_template(
            "login.html",
            error="Ingresa un correo válido."
        )

    # Buscar usuario

    usuario = usuarios.get(email)

    # Validar contraseña

    if usuario and check_password_hash(
        usuario["password"],
        password
    ):

        session.clear()

        session["usuario"] = {
            "nombre": usuario["nombre"],
            "email": email,
            "rol": usuario["rol"]
        }

        return redirect("/dashboard")

    return render_template(
        "login.html",
        error="Correo o contraseña incorrectos."
    )


# Cerrar sesión

@auth.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
