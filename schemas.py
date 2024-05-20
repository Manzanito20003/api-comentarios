from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Configurar CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    # Agrega aquí los orígenes permitidos
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

host_name = "database.ckmzaeatzvjd.us-east-1.rds.amazonaws.com"
port_number = "3306"
user_name = "admin"
password_db = "RDS_1234"
database_name = "bd_api_comentarios"

# Definir el esquema de datos
class Item(BaseModel):
    id_user: int
    id_publicacion: int
    text: str
    estado: int

# Función auxiliar para conectar a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host=host_name,
        port=port_number,
        user=user_name,
        password=password_db,
        database=database_name
    )

# Obtener todos los comentarios
@app.get('/comments')
def get_comments():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM comentarios where estado<>0")
    result = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"comentarios": result}

# Obtener comentarios por id de publicación
@app.get('/comments/{id_publicacion}')
def get_comments_by_publication(id_publicacion: int):
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM comentarios WHERE id_publicacion=%s  and estado <> 0 ", (id_publicacion,))
    result = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"comentarios": result}

# Obtener comentarios por id_user
@app.get('/comments/user/{id_user}')
def get_comments_by_user(id_user: int):
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM comentarios WHERE id_user=%s and estado <> 0 " , (id_user,))
    result = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"comentarios": result}

# Agregar un nuevo comentario
@app.post('/comments')
def add_comment(comment: Item):
    mydb = get_db_connection()
    cursor = mydb.cursor()
    sql = "INSERT INTO comentarios (id_user, id_publicacion, text,estado) VALUES (%s, %s, %s,1)"
    val = (comment.id_user, comment.id_publicacion, comment.text)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Comentario agregado exitosamente"}

# Actualizar un comentario por su ID
@app.put('/comments/{comment_id}')
def update_comment(comment_id: int, comment: Item):
    mydb = get_db_connection()
    cursor = mydb.cursor()
    sql = "UPDATE comentarios SET id_user=%s, id_publicacion=%s, text=%s WHERE id_comentario=%s"
    val = (comment.id_user, comment.id_publicacion, comment.text, comment_id)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Comentario actualizado exitosamente"}

# Eliminar un comentario por su ID
@app.delete('/comments/{comment_id}')
def delete_comment(comment_id: int):
    mydb = get_db_connection()
    cursor = mydb.cursor()
    sql = "UPDATE comentarios SET estado=0 WHERE id_comentario=%s"
    val = (comment_id,)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Comentario eliminado exitosamente"}

# Ejecutar la aplicación
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
