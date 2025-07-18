# 🚀 Application Flask - Démo Cloud

## Vue d'ensemble

Cette application Flask démontre l'intégration complète avec l'infrastructure Azure déployée via Terraform :

- **Base de données PostgreSQL** : Stockage des métadonnées de fichiers
- **Azure Blob Storage** : Stockage de fichiers dans le cloud
- **Interface web moderne** : Gestion et test des services

## 🎯 Fonctionnalités de démonstration

### 1. Page d'accueil interactive
- **URL** : `http://localhost:5000`
- Affichage en temps réel du statut des connexions
- Interface pour ajouter des fichiers à la base de données
- Liste des fichiers récemment ajoutés

### 2. API REST complète

#### Gestion des fichiers
```bash
# Créer un fichier (JSON)
POST /files
{
  "filename": "document.pdf",
  "description": "Document important"
}

# Lister tous les fichiers
GET /files

# Récupérer un fichier spécifique
GET /files/1
```

#### Test du stockage Azure
```bash
# Tester la connexion au stockage
POST /test-storage
```

#### Santé de l'application
```bash
# Vérifier le statut
GET /health
```

## 🛠️ Démarrage rapide

### Option 1 : Script automatique
```bash
python start_app.py
```

### Option 2 : Manuel
```bash
# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement (exemple)
export DB_HOST="your-db-server.postgres.database.azure.com"
export STORAGE_ACCOUNT_KEY="your-storage-key"

# Lancer l'application
python app.py
```

## 🔧 Configuration avec Terraform

Après avoir déployé l'infrastructure avec Terraform :

```bash
# Récupérer les informations de connexion
terraform output storage_account_name
terraform output storage_account_key
terraform output db_server_fqdn

# Configurer les variables d'environnement
export STORAGE_ACCOUNT_NAME=$(terraform output -raw storage_account_name)
export STORAGE_ACCOUNT_KEY=$(terraform output -raw storage_account_key)
export DB_HOST=$(terraform output -raw db_server_fqdn)
```

## 🧪 Tests de fonctionnement

### 1. Test de la base de données
1. Accédez à `http://localhost:5000`
2. Vérifiez que le statut PostgreSQL affiche "✅ Connecté"
3. Ajoutez un fichier via le formulaire
4. Vérifiez qu'il apparaît dans la liste

### 2. Test du stockage Azure
1. Cliquez sur "Tester la connexion au stockage Azure"
2. Vérifiez la réponse JSON avec le succès du test
3. Un fichier `test-connection.txt` sera créé dans le conteneur

### 3. Test de l'API
```bash
# Test avec curl
curl -X POST http://localhost:5000/files \
  -H "Content-Type: application/json" \
  -d '{"filename":"test.txt", "description":"Test API"}'

curl http://localhost:5000/files
```

## 📊 Monitoring

L'application affiche en temps réel :
- ✅/❌ Statut de connexion PostgreSQL
- ✅/❌ Statut de connexion Azure Storage
- Timestamp de la dernière vérification
- Liste des 5 derniers fichiers ajoutés

## 🔒 Sécurité

- Utilisation des clés d'accès Azure (plus simple que les identités managées)
- Variables d'environnement pour les informations sensibles
- Gestion d'erreurs robuste
- Validation des entrées utilisateur

## 🎨 Interface utilisateur

- Design moderne et responsive
- Indicateurs visuels de statut
- Formulaires intuitifs
- Messages d'erreur clairs

---

**Cette application démontre parfaitement l'intégration d'une application web avec l'infrastructure cloud Azure déployée automatiquement !** 🎉