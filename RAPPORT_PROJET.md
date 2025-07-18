# 📋 Rapport de Projet - TodoList Cloud avec Terraform & Ansible

## 🎯 Objectif du Projet

Ce projet démontre le déploiement automatisé d'une application TodoList moderne sur Microsoft Azure en utilisant :
- **Terraform** pour l'Infrastructure as Code (IaC)
- **Ansible** pour la configuration et le déploiement d'applications
- **Azure** comme plateforme cloud
- **Flask** comme framework web backend

---

## 🏗️ Architecture du Projet

### Vue d'ensemble
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

### Composants Principaux

1. **Infrastructure Azure (Terraform)**
   - Machine virtuelle Ubuntu 22.04 LTS
   - PostgreSQL Flexible Server
   - Azure Blob Storage
   - Groupe de ressources
   - Réseau virtuel et sous-réseau
   - Groupe de sécurité réseau

2. **Application Flask**
   - Interface web moderne et responsive
   - API REST pour la gestion des tâches
   - Intégration PostgreSQL et Azure Storage
   - Système de catégories et priorités

3. **Déploiement Automatisé**
   - Script PowerShell pour Windows
   - Playbook Ansible pour la configuration
   - Installation automatique des dépendances

---

## 📝 Étapes Détaillées du Projet

### Étape 1 : Conception de l'Infrastructure (Terraform)

#### Fichiers Terraform créés :
- `main.tf` : Ressources principales Azure
- `variables.tf` : Variables configurables
- `outputs.tf` : Sorties pour Ansible
- `terraform.tfvars` : Valeurs des variables

#### Ressources déployées :
```hcl
# Groupe de ressources
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

# Machine virtuelle
resource "azurerm_linux_virtual_machine" "main" {
  # Configuration complète de la VM
}

# Base de données PostgreSQL
resource "azurerm_postgresql_flexible_server" "main" {
  # Configuration du serveur de base de données
}

# Stockage Azure
resource "azurerm_storage_account" "main" {
  # Configuration du compte de stockage
}
```

### Étape 2 : Développement de l'Application Flask

#### Fonctionnalités implémentées :
- **Interface utilisateur moderne** avec CSS3 et animations
- **Gestion complète des tâches** (CRUD)
- **Système de catégories** (Personnel, Travail, Urgent, Projets)
- **Niveaux de priorité** (Faible, Moyenne, Élevée)
- **États des tâches** (En attente, En cours, Terminée)
- **API REST** pour l'intégration
- **Monitoring** de l'état des services

#### Structure de la base de données :
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(7) NOT NULL
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES categories(id),
    priority VARCHAR(20) DEFAULT 'medium',
    status VARCHAR(20) DEFAULT 'pending',
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Étape 3 : Configuration Ansible

#### Playbook principal (`playbook.yml`) :
- Installation des dépendances système
- Configuration de Python et pip
- Déploiement de l'application Flask
- Configuration de la base de données
- Chargement des données d'exemple
- Configuration du firewall

#### Tâches automatisées :
```yaml
- name: Install system dependencies
  apt:
    name:
      - python3
      - python3-pip
      - postgresql-client
      - git
    state: present
    update_cache: yes

- name: Install Python dependencies
  pip:
    requirements: /home/azureuser/app/requirements.txt
    executable: pip3

- name: Start Flask application
  shell: |
    cd /home/azureuser/app
    nohup python3 app.py > app.log 2>&1 &
```

### Étape 4 : Script de Déploiement Automatique

#### `deploy.ps1` - Orchestration complète :
```powershell
# 1. Vérification des prérequis
# 2. Déploiement Terraform
# 3. Génération de l'inventaire Ansible
# 4. Exécution du playbook
# 5. Affichage des informations de connexion
```

---

## 🔧 Problèmes Rencontrés et Solutions

### 1. Problème : Connexion SSH depuis Windows
**Symptôme :** Ansible ne pouvait pas se connecter à la VM Azure depuis Windows

**Cause :** Configuration SSH incompatible entre Windows et WSL

**Solution :**
- Utilisation de WSL pour exécuter Terraform et Ansible
- Configuration des clés SSH dans WSL : `~/.ssh/id_rsa`
- Modification du script PowerShell pour utiliser WSL :
```powershell
wsl terraform init
wsl ansible-playbook -i inventory.ini playbook.yml
```

### 2. Problème : Variables d'environnement non persistantes
**Symptôme :** L'application Flask ne trouvait pas les variables de configuration

**Cause :** Variables d'environnement perdues après redémarrage

**Solution :**
- Création d'un fichier `.env` sur la VM
- Chargement automatique via Python-dotenv
- Configuration dans le playbook Ansible :
```yaml
- name: Create environment file
  template:
    src: env.j2
    dest: /home/azureuser/app/.env
    mode: '0600'
```

### 3. Problème : Firewall bloquant l'accès à l'application
**Symptôme :** Application inaccessible depuis l'extérieur malgré le déploiement

**Cause :** UFW (firewall Ubuntu) bloquait le port 5000

**Solution :**
- Configuration automatique du firewall dans Ansible :
```yaml
- name: Configure UFW firewall
  ufw:
    rule: allow
    port: '5000'
    proto: tcp

- name: Enable UFW
  ufw:
    state: enabled
```

### 4. Problème : Connexion PostgreSQL SSL
**Symptôme :** Erreurs de connexion SSL à la base de données Azure

**Cause :** Azure PostgreSQL Flexible Server exige SSL par défaut

**Solution :**
- Configuration de la chaîne de connexion avec SSL :
```python
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}?sslmode=require"
```

### 5. Problème : Gestion des dépendances Python
**Symptôme :** Modules Python manquants sur la VM

**Cause :** Installation incomplète des dépendances

**Solution :**
- Création d'un fichier `requirements.txt` complet :
```txt
Flask==2.3.3
psycopg2-binary==2.9.7
azure-storage-blob==12.17.0
python-dotenv==1.0.0
Werkzeug==2.3.7
```

---

## 📊 Résultats et Métriques

### Temps de Déploiement
- **Infrastructure Terraform :** ~5-8 minutes
- **Configuration Ansible :** ~3-5 minutes
- **Total :** ~10-15 minutes pour un déploiement complet

### Ressources Azure Créées
- 1 Groupe de ressources
- 1 Machine virtuelle (Standard_B1s)
- 1 PostgreSQL Flexible Server (Burstable_B1ms)
- 1 Compte de stockage (Standard_LRS)
- 1 Réseau virtuel avec sous-réseau
- 1 IP publique
- 1 Groupe de sécurité réseau

### Coûts Estimés (par mois)
- VM Standard_B1s : ~15€
- PostgreSQL Burstable_B1ms : ~20€
- Stockage Standard_LRS : ~2€
- **Total estimé :** ~37€/mois

---

## 🎯 Fonctionnalités de l'Application

### Interface Utilisateur
- **Design moderne** avec gradient et animations CSS
- **Responsive** adapté mobile et desktop
- **Statistiques en temps réel** des tâches
- **Filtrage dynamique** par statut

### Gestion des Tâches
- Création avec titre, description, catégorie, priorité
- États : En attente → En cours → Terminée
- Actions rapides : Commencer, Terminer, Supprimer
- Dates d'échéance avec indicateurs visuels

### API REST
```bash
# Endpoints principaux
GET  /api/tasks          # Liste des tâches
POST /tasks              # Créer une tâche
POST /tasks/{id}/start   # Commencer une tâche
POST /tasks/{id}/complete # Terminer une tâche
GET  /health             # État de l'application
```

---

## 🔒 Sécurité Implémentée

### Niveau Infrastructure
- **Groupe de sécurité réseau** limitant l'accès aux ports nécessaires
- **Clés SSH** pour l'authentification (pas de mot de passe)
- **SSL/TLS** obligatoire pour PostgreSQL
- **Firewall UFW** configuré sur la VM

### Niveau Application
- **Variables d'environnement** pour les secrets
- **Validation des entrées** utilisateur
- **Gestion d'erreurs** robuste
- **Pas de logs des informations sensibles**
