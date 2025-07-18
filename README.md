# 📝 TodoList Cloud - Démo Terraform & Ansible

Une application TodoList moderne déployée automatiquement sur Azure avec Terraform et Ansible.

## 🚀 Fonctionnalités

### ✨ Interface Moderne
- Design responsive avec gradient et animations
- Interface utilisateur intuitive et moderne
- Filtrage des tâches par statut (Toutes, En attente, En cours, Terminées)
- Statistiques en temps réel

### 📋 Gestion des Tâches
- **Création de tâches** avec titre, description, catégorie, priorité et date d'échéance
- **Catégories colorées** : Personnel, Travail, Urgent, Projets
- **Niveaux de priorité** : Faible 🟢, Moyenne 🟡, Élevée 🔴
- **États des tâches** : En attente, En cours, Terminée
- **Actions rapides** : Commencer, Terminer, Supprimer

### 🗄️ Base de Données
- **PostgreSQL Flexible Server** sur Azure
- Tables relationnelles : `tasks`, `categories`, `task_files`
- Données d'exemple pré-chargées
- Sauvegarde automatique vers Azure Blob Storage

### ☁️ Intégration Cloud
- **Azure Blob Storage** pour les fichiers et sauvegardes
- **Monitoring** de l'état des services
- **API REST** pour l'intégration avec d'autres systèmes

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Terraform     │───▶│   Azure VM       │───▶│  PostgreSQL     │
│   (Infrastructure)│    │   (Flask App)    │    │  (Database)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Azure Blob     │
                       │  Storage        │
                       └─────────────────┘
```

## 🛠️ Déploiement

### Prérequis
- WSL (Windows Subsystem for Linux)
- Terraform installé dans WSL
- Ansible installé dans WSL
- Clés SSH configurées (`~/.ssh/id_rsa`)
- Azure CLI configuré

### Déploiement Automatique

```powershell
# Exécuter le script de déploiement
.\deploy.ps1
```

### Déploiement Manuel

```bash
# 1. Déployer l'infrastructure
wsl terraform init
wsl terraform plan
wsl terraform apply

# 2. Déployer l'application
wsl ansible-playbook -i inventory.ini playbook.yml

# 3. Charger les données d'exemple (optionnel)
wsl ansible-playbook -i inventory.ini playbook.yml --tags sample_data
```

## 📊 API Endpoints

### Tâches
- `GET /` - Interface web principale
- `GET /api/tasks` - Liste toutes les tâches (JSON)
- `POST /tasks` - Créer une nouvelle tâche
- `POST /tasks/{id}/start` - Commencer une tâche
- `POST /tasks/{id}/complete` - Terminer une tâche
- `POST /tasks/{id}/delete` - Supprimer une tâche

### Catégories
- `GET /api/categories` - Liste toutes les catégories (JSON)

### Système
- `GET /health` - Vérification de l'état de l'application
- `POST /test-storage` - Test de connexion Azure Storage

## 🔧 Configuration

### Variables d'Environnement
```bash
# Base de données
DB_HOST=your-postgres-server.postgres.database.azure.com
DB_NAME=sbeldb
DB_USER=dbadmin
DB_PASS=SecurePass123!

# Azure Storage
STORAGE_ACCOUNT_NAME=sbelstorage
STORAGE_ACCOUNT_KEY=your-storage-key
CONTAINER_NAME=staticfiles
```

### Fichiers de Configuration
- `main.tf` - Infrastructure Terraform
- `playbook.yml` - Playbook de déploiement Ansible
- `app.py` - Application Flask TodoList
- `ansible.cfg` - Configuration Ansible
- `inventory.ini` - Inventaire des serveurs
- `sample_data.sql` - Données d'exemple
- `deploy.ps1` - Script de déploiement automatique

## 🎨 Captures d'Écran

### Interface Principale
- Dashboard avec statistiques en temps réel
- Formulaire de création de tâches
- Liste des tâches avec filtres
- Actions rapides sur chaque tâche

### Fonctionnalités
- **Responsive Design** : Adapté mobile et desktop
- **Animations** : Effets de survol et transitions fluides
- **Couleurs** : Système de couleurs cohérent pour les priorités et statuts
- **UX Moderne** : Interface inspirée des meilleures pratiques actuelles

## 📝 Notes Techniques

### Stack Technologique
- **Frontend** : HTML5, CSS3, JavaScript (Vanilla)
- **Backend** : Python Flask
- **Base de données** : PostgreSQL Flexible Server
- **Cloud** : Microsoft Azure
- **Infrastructure** : Terraform
- **Déploiement** : Ansible
- **OS** : Ubuntu 22.04 LTS

### Sécurité
- Connexions SSL/TLS obligatoires
- Firewall UFW configuré
- SELinux en mode permissif
- Clés SSH pour l'authentification
- Variables d'environnement pour les secrets

## 📋 Étapes d'Utilisation

1. **Configurer l'authentification Azure** : `az login`
2. **Cloner le projet** et naviguer dans le dossier
3. **Exécuter le déploiement** : `./deploy.ps1`
4. **Accéder à l'application** via l'IP publique sur le port 5000
5. **Tester les fonctionnalités** : créer, modifier, supprimer des tâches
6. **Vérifier les intégrations** : base de données et stockage Azure
7. **Nettoyer les ressources** : `wsl terraform destroy`
