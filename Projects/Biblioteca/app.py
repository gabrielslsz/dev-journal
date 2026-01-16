import os
from flask import Flask, render_template_string
from google.cloud.sql.connector import Connector
import sqlalchemy

app = Flask(__name__)

# CONFIGURAÇÕES (Use os dados da sua imagem do Cloud SQL)
INSTANCE_CONNECTION_NAME = "i2:us-central1:free-trial-first-project"
DB_USER = "postgres" # Ou o usuário que você criou
DB_PASS = "sua_senha_aqui"
DB_NAME = "postgres" # Ou o nome do banco que você criou

connector = Connector()

def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn

engine = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn)

@app.route('/')
def home():
    try:
        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text("SELECT 'Conexão Sucesso!'")).fetchone()
            return f"<h1>Status: {result[0]}</h1><p>Conectado ao Cloud SQL via VS Code!</p>"
    except Exception as e:
        return f"<h1>Erro:</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(port=8080, debug=True)