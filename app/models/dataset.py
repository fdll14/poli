from app import app
from app import mysql

class Dataset:
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dataset")
        return cursor.fetchall()
    def getOne(self, id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dataset WHERE id_dataset ="+id)
        return cursor.fetchone()
    def store(self, pertanyaan, jawaban):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dataset (pertanyaan, jawaban) VALUES (%s, %s)", (pertanyaan, jawaban))
        conn.commit()
        cursor.close()
    def destroy(self,id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM dataset WHERE id_dataset = "+id)
        conn.commit()
        cursor.close()
    def update(self, id, pertanyaan, jawaban):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE dataset SET pertanyaan ='"+pertanyaan+"', jawaban = '"+jawaban+"' WHERE id_dataset = "+id)
        conn.commit()
        cursor.close()