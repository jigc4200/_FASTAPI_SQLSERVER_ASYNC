# database.py
import aioodbc
import asyncio

# Configuración de la base de datos
DB_CONFIG = {
    'DRIVER': 'ODBC Driver 18 for SQL Server',  # Nombre del controlador ODBC
    'SERVER': 'localhost',                      # Servidor de la base de datos
    'DATABASE': 'WalletDB',                     # Nombre de la base de datos
    'UID': 'sa',                                # Usuario de la base de datos
    'PWD': '<TuPasswordFuerte123>',             # Contraseña del usuario
    'Encrypt': 'no',                            
    'TrustServerCertificate': 'yes',            # Confiar en el certificado del servidor
}

# Crear el pool de conexiones asíncrono
connection_pool = None

async def create_pool():
    global connection_pool
    # Construir el DSN (Data Source Name) a partir de la configuración
    dsn = (
        f"DRIVER={{{DB_CONFIG['DRIVER']}}};"
        f"SERVER={DB_CONFIG['SERVER']};"
        f"DATABASE={DB_CONFIG['DATABASE']};"
        f"UID={DB_CONFIG['UID']};"
        f"PWD={DB_CONFIG['PWD']};"
        f"Encrypt={DB_CONFIG['Encrypt']};"
        f"TrustServerCertificate={DB_CONFIG['TrustServerCertificate']};"
    )
    # Crear el pool de conexiones
    connection_pool = await aioodbc.create_pool(
        dsn=dsn,  # Cadena de conexión (DSN)
        minsize=1,  # Número mínimo de conexiones en el pool
        maxsize=10,  # Número máximo de conexiones en el pool
    )

# Función para obtener una conexión del pool
async def get_db_connection():
    if connection_pool is None:
        await create_pool()
    return await connection_pool.acquire()

# Función para liberar una conexión al pool
async def release_db_connection(conn):
    await connection_pool.release(conn)