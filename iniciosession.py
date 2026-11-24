#Esta parte importa las herramientas necesarias de Flask.
#Blueprint permite organizar el inicio de sesión como un módulo independiente, render_template muestra las páginas HTML, 
# request recibe los datos del formulario, redirect redirige al usuario hacia otra 
# página y session mantiene la información del usuario autenticado.

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session
)

#Esta librería permite proteger las contraseñas mediante hashes. 
# generate_password_hash transforma la contraseña en un hash, 
# mientras que check_password_hash verifica si la contraseña ingresada por el usuario corresponde al hash almacenado

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

#Esta librería permite trabajar con expresiones regulares, 
# las cuales se utilizan en el código para comprobar que el correo electrónico ingresado tenga un formato válido.

import re





#Crea un módulo de autenticación llamado auth, 
# cuya función es separar las operaciones de inicio y cierre de sesión del archivo principal app.py, 
# permitiendo una mejor organización del código mediante la programación modular.

auth = Blueprint("auth", __name__)


#Esta parte crea un diccionario que almacena temporalmente dos usuarios de prueba, 
# cada uno con su correo electrónico, nombre, hash de contraseña y rol. 
# Su función es permitir la autenticación sin necesidad de consultar una base de datos
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



#Obtiene el correo electrónico y la contraseña ingresados en el formulario HTML. 
# En el correo, strip() elimina los espacios innecesarios al principio y al final, 
# mientras que lower() convierte las letras a minúsculas para facilitar la búsqueda del usuario.

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


#Define la función encargada de cerrar la sesión del usuario. 
# Elimina toda la información de autenticación almacenada y redirige nuevamente al formulario de inicio de sesión.

@auth.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
