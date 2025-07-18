# 🚀 Instructions de Déploiement - TodoList Cloud

## 📋 Prérequis

### Système d'exploitation
- **Windows 10/11** avec WSL2 installé
- **Ubuntu 20.04+ dans WSL** (recommandé)

### Outils requis

#### 1. Azure CLI
```bash
# Installation dans WSL
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Connexion à Azure
az login
```

#### 2. Terraform
```bash
# Installation dans WSL
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

#### 3. Ansible
```bash
# Installation dans WSL
sudo apt update
sudo apt install ansible
```

#### 4. Clés SSH
```bash
# Génération des clés SSH dans WSL
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
```

---

## 🔧 Configuration Initiale

### 1. Cloner le projet
```bash
git clone <votre-repo>
cd TodoList-Cloud
```

### 2. Configurer les variables Terraform

Éditez le fichier `terraform.tfvars` :
```hcl
# Informations générales
resource_group_name = "rg-todolist-prod"
location           = "West Europe"
project_name       = "todolist"
environment        = "prod"

# Configuration VM
vm_size = "Standard_B1s"
admin_username = "azureuser"

# Configuration base de données
db_admin_username = "dbadmin"
db_admin_password = "SecurePass123!"
db_name          = "sbeldb"

# Configuration stockage
storage_account_tier = "Standard"
storage_replication  = "LRS"
```

### 3. Configurer Ansible

Vérifiez le fichier `ansible.cfg` :
```ini
[defaults]
host_key_checking = False
remote_user = azureuser
private_key_file = ~/.ssh/id_rsa
inventory = inventory.ini
retry_files_enabled = False

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s -o UserKnownHostsFile=/dev/null -o IdentitiesOnly=yes
```

---

## 🚀 Déploiement Automatique

### Option 1 : Script PowerShell (Recommandé)

```powershell
# Depuis PowerShell Windows
.\deploy.ps1
```

Ce script :
1. ✅ Vérifie les prérequis
2. 🏗️ Déploie l'infrastructure avec Terraform
3. 📝 Génère l'inventaire Ansible
4. 🔧 Configure la VM avec Ansible
5. 🚀 Démarre l'application
6. 📊 Affiche les informations de connexion

### Option 2 : Déploiement Manuel

#### Étape 1 : Infrastructure Terraform
```bash
# Dans WSL
cd /mnt/c/path/to/project

# Initialisation
terraform init

# Planification
terraform plan

# Déploiement
terraform apply
```

#### Étape 2 : Configuration Ansible
```bash
# Générer l'inventaire
echo "[webservers]" > inventory.ini
echo "$(terraform output -raw public_ip) ansible_user=azureuser" >> inventory.ini

# Tester la connexion
ansible all -m ping

# Déployer l'application
ansible-playbook playbook.yml
```

---

## 🔍 Vérification du Déploiement

### 1. Vérifier l'infrastructure
```bash
# Lister les ressources créées
az resource list --resource-group rg-todolist-prod --output table

# Vérifier la VM
az vm show --resource-group rg-todolist-prod --name vm-todolist-prod

# Vérifier la base de données
az postgres flexible-server show --resource-group rg-todolist-prod --name psql-todolist-prod
```

### 2. Tester la connectivité
```bash
# SSH vers la VM
ssh azureuser@$(terraform output -raw public_ip)

# Vérifier les services sur la VM
sudo systemctl status todolist
sudo journalctl -u todolist -f
```

### 3. Tester l'application
```bash
# Obtenir l'IP publique
PUBLIC_IP=$(terraform output -raw public_ip)

# Tester l'application web
curl http://$PUBLIC_IP:5000

# Tester l'API
curl http://$PUBLIC_IP:5000/api/tasks

# Tester le health check
curl http://$PUBLIC_IP:5000/health
```

---

## 🛠️ Dépannage

### Problèmes courants

#### 1. Erreur de connexion SSH
```bash
# Vérifier les clés SSH
ls -la ~/.ssh/

# Tester la connexion
ssh -v azureuser@<IP_PUBLIQUE>

# Régénérer les clés si nécessaire
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
```

#### 2. Terraform : Erreur de provider
```bash
# Réinitialiser Terraform
rm -rf .terraform*
terraform init
```

#### 3. Ansible : Connexion refusée
```bash
# Vérifier l'inventaire
cat inventory.ini

# Tester la connectivité
ansible all -m ping -vvv

# Vérifier les groupes de sécurité Azure
az network nsg rule list --resource-group rg-todolist-prod --nsg-name nsg-todolist-prod
```

#### 4. Application non accessible
```bash
# Se connecter à la VM
ssh azureuser@<IP_PUBLIQUE>

# Vérifier le service
sudo systemctl status todolist

# Vérifier les logs
sudo journalctl -u todolist -f

# Vérifier le firewall
sudo ufw status

# Vérifier les ports
sudo netstat -tlnp | grep 5000
```

### Logs utiles

```bash
# Logs Terraform
terraform apply -auto-approve 2>&1 | tee terraform.log

# Logs Ansible
ansible-playbook playbook.yml -vvv 2>&1 | tee ansible.log

# Logs application sur la VM
sudo journalctl -u todolist --since "1 hour ago"
tail -f /home/azureuser/app/app.log
```

---

## 🔄 Mise à Jour de l'Application

### 1. Mise à jour du code
```bash
# Sur la VM
cd /home/azureuser/app
git pull origin main

# Redémarrer le service
sudo systemctl restart todolist
```

### 2. Mise à jour via Ansible
```bash
# Depuis votre machine locale
ansible-playbook playbook.yml --tags update
```

### 3. Mise à jour de l'infrastructure
```bash
# Modifier terraform.tfvars ou main.tf
# Puis appliquer les changements
terraform plan
terraform apply
```

---

## 🧹 Nettoyage des Ressources

### Suppression complète
```bash
# Détruire toute l'infrastructure
terraform destroy

# Confirmer la suppression
az resource list --resource-group rg-todolist-prod
```

### Suppression sélective
```bash
# Supprimer seulement la VM
terraform destroy -target=azurerm_linux_virtual_machine.main

# Supprimer seulement le stockage
terraform destroy -target=azurerm_storage_account.main
```

---

## 📊 Monitoring et Maintenance

### Surveillance de l'application
```bash
# Vérification automatique de l'état
watch -n 30 'curl -s http://<IP_PUBLIQUE>:5000/health | jq .'

# Monitoring des ressources système
ssh azureuser@<IP_PUBLIQUE> 'htop'

# Vérification de l'espace disque
ssh azureuser@<IP_PUBLIQUE> 'df -h'
```

### Sauvegarde
```bash
# Sauvegarde de la base de données
pg_dump -h <DB_HOST> -U dbadmin -d sbeldb > backup_$(date +%Y%m%d).sql

# Sauvegarde du code application
tar -czf app_backup_$(date +%Y%m%d).tar.gz /home/azureuser/app/
```

---

## 🔐 Sécurité

### Bonnes pratiques

1. **Rotation des clés SSH**
   ```bash
   # Générer de nouvelles clés
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_new
   
   # Mettre à jour Terraform
   # Redéployer la VM
   ```

2. **Mise à jour des mots de passe**
   ```bash
   # Changer le mot de passe de la base de données
   az postgres flexible-server update --resource-group rg-todolist-prod --name psql-todolist-prod --admin-password NewSecurePass456!
   ```

3. **Mise à jour du système**
   ```bash
   # Sur la VM
   sudo apt update && sudo apt upgrade -y
   sudo systemctl restart todolist
   ```
