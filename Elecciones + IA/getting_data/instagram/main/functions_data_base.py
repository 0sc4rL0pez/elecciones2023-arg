import pyodbc


def connectDataBase():
    SERVER = 'ACHEPE'
    DATABASE = 'elecciones-IA-data'

    connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'

    conn = pyodbc.connect(connectionString) 
    return conn
      
       

def add_data_base(short_code, source, number_likes, date, caption):
    conn = connectDataBase()
    cursor = conn.cursor()

    """
    Insert each value in the data base
    """        
    SQL_STATEMENT = f"""
    INSERT Publicaciones
    VALUES ('{short_code}', '{source}', {number_likes}, '{date}', '{caption}')
    """
    cursor.execute(SQL_STATEMENT)
    conn.commit()

    conn.close()

def add_data_base_comentarios(short_code, comments):
    conn = connectDataBase()
    cursor = conn.cursor()

    """
    Insert each value in the data base
    """         
    SQL_STATEMENT = f"""
    INSERT Comentarios
    VALUES ('{short_code}', '{comments}')
    """
    cursor.execute(SQL_STATEMENT)
    conn.commit()

    conn.close()

def Update(short_code, source, number_likes, caption):
    conn = connectDataBase()
    cursor = conn.cursor()

    """
    Update each value in the data base
    """        
    SQL_STATEMENT = f"""
    UPDATE Publicaciones
    SET fuente = '{source}', cantidad_likes = '{number_likes}', descripcion = '{caption}'
    WHERE [id] = '{short_code}'
    """
    cursor.execute(SQL_STATEMENT)
    conn.commit()

    conn.close()

def IsInsideDB(id):
        conn = connectDataBase()
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
       






