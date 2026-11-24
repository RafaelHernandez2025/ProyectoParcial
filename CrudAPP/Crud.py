import pymssql
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

def conectar_db():
    """Establece la conexión con la base de datos SQL Server."""
    try:
        # ajusta estos datos con la conexion de la bd
        conn = pymssql.connect(
            server='ASUSRAFA\\SQLEXPRES2025', 
            user='Rafael_Hernandez', 
            password='123456789.', 
            database='GestionIT'
        )
        return conn
    except Exception as e:
        print(f"Aviso de conexión: {e}")
        return None

def obtener_inventario():

    conn = conectar_db()
    query = "SELECT IDprod, nombreProd, costoprod, existencias, descripcion FROM productos"
        df = pd.read_sql(query, conn)
        conn.close()

    
    