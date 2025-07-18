from flask import Flask, jsonify, request, render_template_string, redirect
import os
import psycopg2
from azure.storage.blob import BlobServiceClient
import datetime
import json

# Charger les variables d'environnement depuis le fichier .env si présent
def load_env_file():
    env_file = '/opt/flask_app/.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
        print(f"Variables d'environnement chargées depuis {env_file}")
    else:
        print("Fichier .env non trouvé, utilisation des variables par défaut")

# Charger la configuration
load_env_file()

app = Flask(__name__)

# Configuration pour la base de données
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'sbeldb')
DB_USER = os.getenv('DB_USER', 'dbadmin')
DB_PASS = os.getenv('DB_PASS', 'SecurePass123!')

# Configuration pour Azure Storage
STORAGE_ACCOUNT_NAME = os.getenv('STORAGE_ACCOUNT_NAME', 'sbelstorage')
STORAGE_ACCOUNT_KEY = os.getenv('STORAGE_ACCOUNT_KEY', '')
CONTAINER_NAME = os.getenv('CONTAINER_NAME', 'staticfiles')

# Connexion à la DB
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=5432,
            sslmode='require'
        )
        return conn
    except Exception as e:
        print(f"Erreur de connexion DB: {e}")
        return None

# Initialiser les tables
def init_db():
    try:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            
            # Table des catégories
            cur.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL UNIQUE,
                    color VARCHAR(7) DEFAULT '#007bff',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table des tâches
            cur.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    description TEXT,
                    category_id INTEGER REFERENCES categories(id),
                    priority VARCHAR(10) DEFAULT 'medium',
                    status VARCHAR(20) DEFAULT 'pending',
                    due_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table des fichiers attachés
            cur.execute('''
                CREATE TABLE IF NOT EXISTS task_files (
                    id SERIAL PRIMARY KEY,
                    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
                    filename VARCHAR(255) NOT NULL,
                    blob_url TEXT,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insérer des catégories par défaut
            cur.execute('''
                INSERT INTO categories (name, color) VALUES 
                ('Personnel', '#28a745'),
                ('Travail', '#007bff'),
                ('Urgent', '#dc3545'),
                ('Projets', '#6f42c1')
                ON CONFLICT (name) DO NOTHING
            ''')
            
            conn.commit()
            cur.close()
            conn.close()
            print("Base de données initialisée avec succès")
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la DB: {e}")

# Configuration Azure Storage
def get_blob_service_client():
    try:
        if STORAGE_ACCOUNT_KEY:
            account_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
            blob_service_client = BlobServiceClient(
                account_url=account_url,
                credential=STORAGE_ACCOUNT_KEY
            )
            return blob_service_client
        else:
            print("Clé de stockage Azure non configurée")
            return None
    except Exception as e:
        print(f"Erreur de connexion au stockage Azure: {e}")
        return None

# Template HTML moderne pour la TodoList
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>📝 TodoList Cloud - Démo Terraform & Ansible</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 20px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 1.1em; }
        .status-bar {
            background: #f8f9fa;
            padding: 15px 30px;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        .status-item { 
            display: flex; 
            align-items: center; 
            margin: 5px 0;
        }
        .status-item span { margin-left: 8px; }
        .main-content {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 30px;
            padding: 30px;
        }
        .sidebar {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            height: fit-content;
        }
        .task-form {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        .form-group { margin-bottom: 15px; }
        .form-group label { 
            display: block; 
            margin-bottom: 5px; 
            font-weight: 600;
            color: #495057;
        }
        .form-control {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        .form-control:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
            text-align: center;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        .btn-success { background: #28a745; color: white; }
        .btn-danger { background: #dc3545; color: white; }
        .btn-warning { background: #ffc107; color: #212529; }
        .btn-sm { padding: 6px 12px; font-size: 12px; }
        .tasks-container {
            background: white;
        }
        .task-filters {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .filter-btn {
            padding: 8px 16px;
            border: 2px solid #e9ecef;
            background: white;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .filter-btn.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        .task-item {
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s;
            position: relative;
        }
        .task-item:hover {
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        .task-header {
            display: flex;
            justify-content: between;
            align-items: flex-start;
            margin-bottom: 10px;
        }
        .task-title {
            font-size: 1.2em;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        .task-meta {
            display: flex;
            gap: 10px;
            align-items: center;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }
        .badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-priority-high { background: #ffebee; color: #c62828; }
        .badge-priority-medium { background: #fff3e0; color: #ef6c00; }
        .badge-priority-low { background: #e8f5e8; color: #2e7d32; }
        .badge-status-pending { background: #e3f2fd; color: #1565c0; }
        .badge-status-in-progress { background: #fff3e0; color: #ef6c00; }
        .badge-status-completed { background: #e8f5e8; color: #2e7d32; }
        .task-description {
            color: #6c757d;
            margin-bottom: 15px;
            line-height: 1.5;
        }
        .task-actions {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #6c757d;
            font-size: 0.9em;
        }
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            .header h1 { font-size: 2em; }
            .status-bar {
                flex-direction: column;
                align-items: flex-start;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 TodoList Cloud</h1>
            <p>Application moderne déployée avec Terraform et Ansible</p>
        </div>
        
        <div class="status-bar">
            <div class="status-item">
                <span>🗄️ Base de données:</span>
                <span>{{ db_status }}</span>
            </div>
            <div class="status-item">
                <span>☁️ Stockage Azure:</span>
                <span>{{ storage_status }}</span>
            </div>
            <div class="status-item">
                <span>🕒 Dernière mise à jour:</span>
                <span>{{ timestamp }}</span>
            </div>
        </div>
        
        <div class="main-content">
            <div class="sidebar">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{{ stats.total }}</div>
                        <div class="stat-label">Total</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ stats.pending }}</div>
                        <div class="stat-label">En attente</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ stats.completed }}</div>
                        <div class="stat-label">Terminées</div>
                    </div>
                </div>
                
                <div class="task-form">
                    <h3>➕ Nouvelle tâche</h3>
                    <form action="/tasks" method="post">
                        <div class="form-group">
                            <label>Titre *</label>
                            <input type="text" name="title" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label>Description</label>
                            <textarea name="description" class="form-control" rows="3"></textarea>
                        </div>
                        <div class="form-group">
                            <label>Catégorie</label>
                            <select name="category_id" class="form-control">
                                <option value="">Aucune catégorie</option>
                                {% for category in categories %}
                                <option value="{{ category[0] }}">{{ category[1] }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Priorité</label>
                            <select name="priority" class="form-control">
                                <option value="low">🟢 Faible</option>
                                <option value="medium" selected>🟡 Moyenne</option>
                                <option value="high">🔴 Élevée</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Date d'échéance</label>
                            <input type="date" name="due_date" class="form-control">
                        </div>
                        <button type="submit" class="btn btn-primary">Créer la tâche</button>
                    </form>
                </div>
            </div>
            
            <div class="tasks-container">
                <div class="task-filters">
                    <button class="filter-btn active" onclick="filterTasks('all')">Toutes</button>
                    <button class="filter-btn" onclick="filterTasks('pending')">En attente</button>
                    <button class="filter-btn" onclick="filterTasks('in-progress')">En cours</button>
                    <button class="filter-btn" onclick="filterTasks('completed')">Terminées</button>
                </div>
                
                <div id="tasks-list">
                    {% for task in tasks %}
                    <div class="task-item" data-status="{{ task[6] }}">
                        <div class="task-header">
                            <div class="task-title">{{ task[1] }}</div>
                        </div>
                        <div class="task-meta">
                            <span class="badge badge-priority-{{ task[4] }}">{{ task[4]|title }}</span>
                            <span class="badge badge-status-{{ task[6] }}">{{ task[6]|replace('-', ' ')|title }}</span>
                            {% if task[7] %}
                            <span class="badge" style="background: #f8f9fa; color: #495057;">📅 {{ task[7] }}</span>
                            {% endif %}

                        </div>
                        {% if task[2] %}
                        <div class="task-description">{{ task[2] }}</div>
                        {% endif %}
                        <div class="task-actions">
                            {% if task[6] != 'completed' %}
                            <form action="/tasks/{{ task[0] }}/complete" method="post" style="display: inline;">
                                <button type="submit" class="btn btn-success btn-sm">✅ Terminer</button>
                            </form>
                            {% endif %}
                            {% if task[6] == 'pending' %}
                            <form action="/tasks/{{ task[0] }}/start" method="post" style="display: inline;">
                                <button type="submit" class="btn btn-warning btn-sm">▶️ Commencer</button>
                            </form>
                            {% endif %}
                            <form action="/tasks/{{ task[0] }}/delete" method="post" style="display: inline;">
                                <button type="submit" class="btn btn-danger btn-sm" onclick="return confirm('Supprimer cette tâche ?')">🗑️ Supprimer</button>
                            </form>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function filterTasks(status) {
            const tasks = document.querySelectorAll('.task-item');
            const buttons = document.querySelectorAll('.filter-btn');
            
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            tasks.forEach(task => {
                if (status === 'all' || task.dataset.status === status) {
                    task.style.display = 'block';
                } else {
                    task.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    # Tester la connexion DB
    db_status = "❌ Déconnecté"
    tasks = []
    categories = []
    stats = {'total': 0, 'pending': 0, 'completed': 0}
    
    try:
        conn = get_db_connection()
        if conn:
            db_status = "✅ Connecté"
            cur = conn.cursor()
            
            # Récupérer les tâches avec catégories
            cur.execute('''
                SELECT t.*, c.name as category_name, c.color as category_color
                FROM tasks t
                LEFT JOIN categories c ON t.category_id = c.id
                ORDER BY 
                    CASE t.priority 
                        WHEN 'high' THEN 1
                        WHEN 'medium' THEN 2
                        WHEN 'low' THEN 3
                    END,
                    t.created_at DESC
            ''')
            tasks = cur.fetchall()
            
            # Récupérer les catégories
            cur.execute('SELECT * FROM categories ORDER BY name')
            categories = cur.fetchall()
            
            # Calculer les statistiques
            cur.execute('SELECT COUNT(*) FROM tasks')
            stats['total'] = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending'")
            stats['pending'] = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
            stats['completed'] = cur.fetchone()[0]
            
            cur.close()
            conn.close()
    except Exception as e:
        db_status = f"❌ Erreur: {str(e)[:50]}..."
    
    # Tester la connexion Storage
    storage_status = "❌ Déconnecté"
    try:
        blob_client = get_blob_service_client()
        if blob_client:
            storage_status = "✅ Connecté"
    except Exception as e:
        storage_status = f"❌ Erreur: {str(e)[:50]}..."
    
    return render_template_string(HTML_TEMPLATE, 
                                db_status=db_status,
                                storage_status=storage_status,
                                tasks=tasks,
                                categories=categories,
                                stats=stats,
                                timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# CRUD pour les tâches
@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        if request.is_json:
            data = request.json
        else:
            data = {
                'title': request.form.get('title'),
                'description': request.form.get('description', ''),
                'category_id': request.form.get('category_id') or None,
                'priority': request.form.get('priority', 'medium'),
                'due_date': request.form.get('due_date') or None
            }
        
        if not data.get('title'):
            return jsonify({'error': 'Titre requis'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Erreur de connexion à la base de données'}), 500
        
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO tasks (title, description, category_id, priority, due_date) 
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        ''', (data['title'], data['description'], data['category_id'], 
              data['priority'], data['due_date']))
        
        task_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        if request.is_json:
            return jsonify({'id': task_id, 'message': 'Tâche créée avec succès'}), 201
        else:
            return redirect('/')
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la création: {str(e)}'}), 500

@app.route('/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    try:
        conn = get_db_connection()
        if not conn:
            return redirect('/')
        
        cur = conn.cursor()
        cur.execute('''
            UPDATE tasks SET status = 'completed', updated_at = CURRENT_TIMESTAMP 
            WHERE id = %s
        ''', (task_id,))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect('/')
    except Exception as e:
        return redirect('/')

@app.route('/tasks/<int:task_id>/start', methods=['POST'])
def start_task(task_id):
    try:
        conn = get_db_connection()
        if not conn:
            return redirect('/')
        
        cur = conn.cursor()
        cur.execute('''
            UPDATE tasks SET status = 'in-progress', updated_at = CURRENT_TIMESTAMP 
            WHERE id = %s
        ''', (task_id,))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect('/')
    except Exception as e:
        return redirect('/')

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    try:
        conn = get_db_connection()
        if not conn:
            return redirect('/')
        
        cur = conn.cursor()
        cur.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect('/')
    except Exception as e:
        return redirect('/')

# API endpoints
@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Erreur de connexion à la base de données'}), 500
        
        cur = conn.cursor()
        cur.execute('''
            SELECT t.*, c.name as category_name, c.color as category_color
            FROM tasks t
            LEFT JOIN categories c ON t.category_id = c.id
            ORDER BY t.created_at DESC
        ''')
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        
        tasks_list = []
        for task in tasks:
            tasks_list.append({
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'category_id': task[3],
                'priority': task[4],
                'status': task[6],
                'due_date': task[7].isoformat() if task[7] else None,
                'created_at': task[8].isoformat() if task[8] else None,
                'category_name': task[10] if len(task) > 10 else None,
                'category_color': task[11] if len(task) > 11 else None
            })
        
        return jsonify({'tasks': tasks_list})
    except Exception as e:
        return jsonify({'error': f'Erreur: {str(e)}'}), 500

@app.route('/api/categories', methods=['GET'])
def api_get_categories():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Erreur de connexion à la base de données'}), 500
        
        cur = conn.cursor()
        cur.execute('SELECT * FROM categories ORDER BY name')
        categories = cur.fetchall()
        cur.close()
        conn.close()
        
        categories_list = []
        for cat in categories:
            categories_list.append({
                'id': cat[0],
                'name': cat[1],
                'color': cat[2],
                'created_at': cat[3].isoformat() if cat[3] else None
            })
        
        return jsonify({'categories': categories_list})
    except Exception as e:
        return jsonify({'error': f'Erreur: {str(e)}'}), 500

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy', 
        'message': 'TodoList Cloud opérationnelle',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '2.0.0'
    })

@app.route('/test-storage', methods=['POST'])
def test_storage():
    try:
        blob_service_client = get_blob_service_client()
        if not blob_service_client:
            return jsonify({'error': 'Impossible de se connecter au stockage Azure'}), 500
        
        # Créer un backup des tâches
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*) FROM tasks')
            task_count = cur.fetchone()[0]
            cur.close()
            conn.close()
            
            backup_data = {
                'timestamp': datetime.datetime.now().isoformat(),
                'task_count': task_count,
                'backup_type': 'test'
            }
            
            container_client = blob_service_client.get_container_client(CONTAINER_NAME)
            
            try:
                container_client.create_container()
            except:
                pass
            
            blob_client = container_client.get_blob_client(f"backup-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.json")
            blob_client.upload_blob(json.dumps(backup_data), overwrite=True)
            
            return jsonify({
                'message': 'Test de stockage réussi!',
                'backup_created': True,
                'task_count': task_count
            })
        else:
            return jsonify({'error': 'Erreur de connexion à la base de données'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Erreur de stockage: {str(e)}'}), 500

if __name__ == '__main__':
    print("Initialisation de la TodoList Cloud...")
    init_db()
    print("Démarrage du serveur sur http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)