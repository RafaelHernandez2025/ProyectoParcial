import pymssql
import pandas as pd
import numpy as np

def conectar_db():
    """Establece la conexión con la base de datos SQL Server."""
    try:
        # ajusta estos datos con la conexion de la bd
        conn = pymssql.connect(
            server='localhost', 
            user='sa', 
            password='TuPasswordSeguro', 
            database='SecureStockDB'
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
            'id_producto': [1, 2, 3, 4, 5],
            'modelo': ['RTX 4070 Ti', 'Ryzen 9 7900X', 'SSD NVMe 2TB', 'RAM 16GB DDR5', 'Fuente 850W Gold'],
            'precio': [850.00, 420.00, 150.00, 80.00, 120.00],
            'existencias': [2, 15, 4, 30, 1]
        }
        df = pd.DataFrame(data)
    else:
        query = "SELECT id_producto, modelo, precio, existencias FROM dbo.Inventario_Repuestos"
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