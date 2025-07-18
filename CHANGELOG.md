# 📋 Changelog - TodoList Cloud

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Non publié]

### À venir
- Authentification utilisateur avec Azure AD
- Upload de fichiers attachés aux tâches
- Notifications par email
- Mode sombre/clair
- API GraphQL
- Application mobile

---

## [1.0.0] - 2024-01-15

### 🎉 Version initiale

Première version stable de l'application TodoList Cloud avec déploiement automatisé sur Azure.

### ✨ Ajouté

#### Infrastructure
- **Terraform** : Infrastructure as Code complète pour Azure
  - Machine virtuelle Ubuntu 22.04 LTS
  - PostgreSQL Flexible Server
  - Azure Blob Storage
  - Réseau virtuel avec sécurité
  - IP publique et NSG

#### Application
- **Interface web moderne** avec design responsive
  - Gradient CSS et animations fluides
  - Statistiques en temps réel
  - Filtrage dynamique des tâches
  - Actions rapides (Commencer, Terminer, Supprimer)

- **Gestion complète des tâches**
  - Création avec titre, description, catégorie, priorité
  - États : En attente → En cours → Terminée
  - Dates d'échéance avec indicateurs visuels
  - Catégories colorées (Personnel, Travail, Urgent, Projets)

- **API REST complète**
  - `GET /api/tasks` - Liste des tâches
  - `POST /tasks` - Création de tâches
  - `POST /tasks/{id}/start` - Commencer une tâche
  - `POST /tasks/{id}/complete` - Terminer une tâche
  - `POST /tasks/{id}/delete` - Supprimer une tâche
  - `GET /api/categories` - Liste des catégories
  - `GET /health` - Vérification de l'état

#### Base de Données
- **Schéma PostgreSQL optimisé**
  - Tables : `categories`, `tasks`, `task_files`
  - Index pour les performances
  - Triggers pour les timestamps automatiques
  - Vue `task_statistics` pour les métriques

- **Données d'exemple**
  - 8 catégories pré-configurées
  - 25+ tâches d'exemple
  - Fichiers attachés de démonstration

#### Déploiement
- **Ansible** : Configuration automatisée
  - Installation des dépendances système
  - Configuration Python et Flask
  - Déploiement de l'application
  - Configuration du firewall UFW
  - Service systemd pour l'auto-démarrage

- **Script PowerShell** : Déploiement en un clic
  - Vérification des prérequis
  - Orchestration Terraform + Ansible
  - Génération automatique de l'inventaire
  - Affichage des informations de connexion

#### Sécurité
- **Authentification SSH** par clés publiques
- **Firewall UFW** configuré (ports 22, 5000)
- **SSL/TLS** obligatoire pour PostgreSQL
- **Variables d'environnement** pour les secrets
- **Validation des entrées** utilisateur

#### Documentation
- **README.md** : Guide d'utilisation complet
- **RAPPORT_PROJET.md** : Analyse détaillée du projet
- **INSTRUCTIONS_DEPLOIEMENT.md** : Guide de déploiement
- **DOCUMENTATION_TECHNIQUE.md** : Documentation développeur
- **provision.sh** : Script de provisioning standalone

### 🔧 Configuration

#### Variables Terraform
```hcl
resource_group_name = "rg-todolist-prod"
location           = "West Europe"
project_name       = "todolist"
environment        = "prod"
vm_size           = "Standard_B1s"
db_admin_username = "dbadmin"
db_name          = "sbeldb"
```

#### Dépendances Python
```txt
Flask==2.3.3
psycopg2-binary==2.9.7
azure-storage-blob==12.17.0
python-dotenv==1.0.0
Werkzeug==2.3.7
requests==2.31.0
```

### 📊 Métriques

- **Temps de déploiement** : ~10-15 minutes
- **Coût mensuel estimé** : ~37€
- **Ressources Azure** : 7 ressources créées
- **Lignes de code** : ~1500 lignes (Python + HTML/CSS/JS)
- **Tests** : Interface web + API REST

### 🐛 Corrections

#### Problèmes résolus lors du développement

1. **Connexion SSH depuis Windows**
   - **Problème** : Ansible ne pouvait pas se connecter depuis Windows
   - **Solution** : Utilisation de WSL pour Terraform et Ansible

2. **Variables d'environnement non persistantes**
   - **Problème** : Configuration perdue après redémarrage
   - **Solution** : Fichier `.env` avec python-dotenv

3. **Firewall bloquant l'accès**
   - **Problème** : Application inaccessible malgré le déploiement
   - **Solution** : Configuration automatique UFW dans Ansible

4. **Connexion PostgreSQL SSL**
   - **Problème** : Erreurs SSL avec Azure PostgreSQL
   - **Solution** : Paramètre `sslmode=require` dans la chaîne de connexion

5. **Dépendances Python manquantes**
   - **Problème** : Modules non installés sur la VM
   - **Solution** : `requirements.txt` complet et installation via Ansible

### 🔒 Sécurité

- Aucune vulnérabilité connue
- Secrets gérés via variables d'environnement
- Connexions chiffrées (SSH, PostgreSQL SSL)
- Firewall configuré avec règles minimales

### 📈 Performance

- **Temps de réponse** : < 200ms pour les pages web
- **API REST** : < 100ms pour les endpoints simples
- **Base de données** : Index optimisés pour les requêtes fréquentes
- **Interface** : Animations CSS fluides, pas de JavaScript lourd

---

## [0.9.0] - 2024-01-10

### ✨ Version bêta

#### Ajouté
- Prototype de l'interface web
- API REST basique
- Configuration Terraform initiale
- Tests de déploiement sur Azure

#### 🔧 Modifié
- Optimisation des requêtes SQL
- Amélioration du design CSS
- Refactoring du code Flask

#### 🐛 Corrigé
- Problèmes de connexion à la base de données
- Erreurs de validation des formulaires
- Problèmes de responsive design

---

## [0.5.0] - 2024-01-05

### ✨ Version alpha

#### Ajouté
- Structure de base du projet
- Modèle de données PostgreSQL
- Application Flask minimale
- Configuration Terraform de base

#### 🔧 Configuration initiale
- Environnement de développement
- Dépendances Python
- Structure des fichiers

---

## Types de changements

- **✨ Ajouté** : Nouvelles fonctionnalités
- **🔧 Modifié** : Changements dans les fonctionnalités existantes
- **🐛 Corrigé** : Corrections de bugs
- **🗑️ Supprimé** : Fonctionnalités supprimées
- **🔒 Sécurité** : Corrections de vulnérabilités
- **📈 Performance** : Améliorations de performance
- **📚 Documentation** : Changements dans la documentation

---

## Liens

- [Repository GitHub](https://github.com/votre-username/todolist-cloud)
- [Documentation](./README.md)
- [Guide de déploiement](./INSTRUCTIONS_DEPLOIEMENT.md)
- [Documentation technique](./DOCUMENTATION_TECHNIQUE.md)
- [Rapport de projet](./RAPPORT_PROJET.md)

---

**Maintenu par l'équipe de développement TodoList Cloud** 🚀