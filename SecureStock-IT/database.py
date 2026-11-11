import pymssql
import pandas as pd
import numpy as np

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

def obtener_inventario_analitico():
    """Extrae datos de la BD y aplica análisis estadístico con Pandas y NumPy."""
    conn = conectar_db()
    if not conn:
        # Datos de respaldo simulados en caso de que la BD no esté en línea todavía
        data = {
            'IDprod': [1, 2, 3, 4, 5],
            'nombreProd': ['RTX 4070 Ti', 'Ryzen 9 7900X', 'SSD NVMe 2TB', 'RAM 16GB DDR5', 'Fuente 850W Gold'],
            'costoprod': [850.00, 420.00, 150.00, 80.00, 120.00],
            'existencias': [2, 15, 4, 30, 1],
            'descripcion':['nvidia RTX470Ti de 8gb de vram','Procesado AMD Ryzen 9 7900X ','Memoria corsair de 16bg de RAM DDR5','Memoria de almacenamiento SSD NVMe 2TB', 'aaaa']
        
        }
        df = pd.DataFrame(data)
    else:
        query = "SELECT IDprod, nombreProd, costoprod, existencias, descripcion FROM productos"
        df = pd.read_sql(query, conn)
        conn.close()
    
    # Análisis con NumPy: cálculo de umbral de riesgo de merma basado en la media de stock
    if not df.empty and 'existencias' in df.columns:
        media_stock = np.mean(df['existencias'])
        df['estado_alerta'] = np.where(
            df['existencias'] < (media_stock * 0.4), 
            'CRÍTICO / Riesgo de Merma', 
            'Estable'
        )
    else:
        df['estado_alerta'] = 'Sin datos'
        
    return df
