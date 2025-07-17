from flask import Flask, jsonify, request
import os
import psycopg2
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Configuration pour la base de données (à sécuriser, idéalement via env vars)
DB_HOST = os.getenv('DB_HOST', 'your-db-server.postgres.database.azure.com')  # Remplacer par output Terraform
DB_NAME = os.getenv('DB_NAME', 'sbeldb')
DB_USER = os.getenv('DB_USER', 'dbadmin')
DB_PASS = os.getenv('DB_PASS', 'your-password')  # SENSIBLE, utiliser secrets

# Connexion à la DB
def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

# Créer une table simple pour demo
with get_db_connection() as conn:
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS files (id SERIAL PRIMARY KEY, filename TEXT, description TEXT)')
    conn.commit()

# Configuration pour Azure Storage
STORAGE_ACCOUNT_URL = 'https://yourstorage.blob.core.windows.net'  # Remplacer par variable
credential = DefaultAzureCredential()
blob_service_client = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential=credential)
container_client = blob_service_client.get_container_client('staticfiles')

@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1><p>Cette application Flask a été déployée automatiquement avec Terraform et Ansible! Intégrée avec stockage et DB.</p>'

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Application is running'})

# CRUD pour fichiers dans DB
@app.route('/files', methods=['POST'])
def create_file():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO files (filename, description) VALUES (%s, %s) RETURNING id', (data['filename'], data['description']))
    id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': id}), 201

@app.route('/files/<int:id>', methods=['GET'])
def read_file(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM files WHERE id = %s', (id,))
    file = cur.fetchone()
    cur.close()
    conn.close()
    if file:
        return jsonify({'id': file[0], 'filename': file[1], 'description': file[2]})
    return jsonify({'error': 'File not found'}), 404

// ... Ajouter UPDATE et DELETE de manière similaire

# Upload to storage
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    blob_client = container_client.get_blob_client(file.filename)
    blob_client.upload_blob(file)
    return jsonify({'message': 'File uploaded'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)