# db_connection.py
import mysql.connector
import os

def get_connection():
    try:
        # Configuración de la conexión a MySQL en Laragon
        host = "localhost"  # Servidor local de Laragon
        user = "root"       # Usuario por defecto en Laragon
        password = "12345"       # Sin contraseña en Laragon por defecto
        database = "soldados"  # Nombre de la base de datos

        # Conectar a MySQL
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        return conn

    except mysql.connector.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None  # Evita que el programa crashe si la conexión falla

# Prueba la conexión
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("Conexión exitosa a MySQL en Laragon")
        conn.close()
    else:
        print("Fallo en la conexión a MySQL")