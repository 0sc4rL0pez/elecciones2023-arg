import pyodbc

"""
Me conecto a la base de datos
"""

def conectar_base_datos():
    SERVER = 'ACHEPE'
    DATABASE = 'elecciones-IA-data'

    connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'

    conn = pyodbc.connect(connectionString) 
    return conn
      
       

def agregar_base_datos(short_code, canal, cantidad_likes, fecha, descripcion):
    conn = conectar_base_datos()
    cursor = conn.cursor()

    """
    Inserta cada valor a la base de datos
    """        
    SQL_STATEMENT = f"""
    INSERT Publicaciones
    VALUES ('{short_code}', '{canal}', {cantidad_likes}, '{fecha}', '{descripcion}')
    """
    cursor.execute(SQL_STATEMENT)
    conn.commit()

    conn.close()

def agregar_base_datos_comentarios(short_code, comentarios):
    conn = conectar_base_datos()
    cursor = conn.cursor()

    """
    Inserta cada valor a la base de datos
    """        
    SQL_STATEMENT = f"""
    INSERT Comentarios
    VALUES ('{short_code}', '{comentarios}')
    """
    cursor.execute(SQL_STATEMENT)
    conn.commit()

    conn.close()

def actualizar(short_code, canal, cantidad_likes, descripcion):
    conn = conectar_base_datos()
    cursor = conn.cursor()

    """
    Actualiza cada valor a la base de datos
    """        
    SQL_STATEMENT = f"""
    UPDATE Publicaciones
    SET fuente = '{canal}', cantidad_likes = '{cantidad_likes}', descripcion = '{descripcion}'
    WHERE [id] = '{short_code}'
    """
    cursor.execute(SQL_STATEMENT)
    conn.commit()

    conn.close()

def estaEnBaseDatos(id):
        conn = conectar_base_datos()
        cursor = conn.cursor()
        result = False

        SQL_STATEMENT = f"""
                SELECT COUNT(*) AS Cantidad
                FROM Publicaciones 
                WHERE id = '{id}'
                """
        records = cursor.execute(SQL_STATEMENT)

        for r in records:
                result = r.Cantidad
        conn.close()

        if result>0:
              result = True
        
        return result
       






