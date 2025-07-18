# Script PowerShell pour deployer automatiquement l'infrastructure et l'application

Write-Host "🚀 Début du déploiement automatique..." -ForegroundColor Green

# Vérification des prérequis
Write-Host "📋 Vérification des prérequis..." -ForegroundColor Yellow

# Vérifier si WSL est disponible
try {
    wsl --version | Out-Null
    Write-Host "✅ WSL détecté" -ForegroundColor Green
} catch {
    Write-Host "❌ WSL non disponible. Veuillez installer WSL." -ForegroundColor Red
    exit 1
}

# Vérifier si Ansible est installé dans WSL
try {
    wsl ansible --version | Out-Null
    Write-Host "✅ Ansible détecté dans WSL" -ForegroundColor Green
} catch {
    Write-Host "❌ Ansible non disponible dans WSL. Veuillez installer Ansible." -ForegroundColor Red
    exit 1
}

# Vérifier si Terraform est disponible
try {
    terraform version | Out-Null
    Write-Host "✅ Terraform détecté" -ForegroundColor Green
} catch {
    Write-Host "❌ Terraform non disponible. Veuillez installer Terraform." -ForegroundColor Red
    exit 1
}

# Étape 1: Déploiement de l'infrastructure avec Terraform
Write-Host "🏗️  Déploiement de l'infrastructure avec Terraform..." -ForegroundColor Cyan

terraform init
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors de l'initialisation Terraform" -ForegroundColor Red
    exit 1
}

terraform plan
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors de la planification Terraform" -ForegroundColor Red
    exit 1
}

terraform apply -auto-approve
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors de l'application Terraform" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Infrastructure déployée avec succès" -ForegroundColor Green

# Étape 2: Test de connectivité de l'inventaire
Write-Host "🔍 Test de l'inventaire Ansible..." -ForegroundColor Cyan

wsl ansible all -i inventory.ini --list-hosts
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors du test de l'inventaire" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Inventaire validé" -ForegroundColor Green

# Étape 3: Test de connectivité SSH
Write-Host "🔐 Test de connectivité SSH..." -ForegroundColor Cyan

wsl ansible all -i inventory.ini -m ping
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Problème de connectivité SSH. Vérifiez les clés et la connectivité réseau." -ForegroundColor Yellow
    Write-Host "Continuons avec le déploiement..." -ForegroundColor Yellow
}

# Étape 4: Déploiement de l'application avec Ansible
Write-Host "📦 Déploiement de l'application avec Ansible..." -ForegroundColor Cyan

wsl ansible-playbook -i inventory.ini playbook.yml
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors du déploiement Ansible" -ForegroundColor Red
    Write-Host "💡 Conseils de dépannage:" -ForegroundColor Yellow
    Write-Host "   - Vérifiez la connectivité réseau vers le serveur" -ForegroundColor Yellow
    Write-Host "   - Vérifiez que la clé SSH est correcte et accessible" -ForegroundColor Yellow
    Write-Host "   - Vérifiez que le serveur cible est démarré" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Application déployée avec succès" -ForegroundColor Green

# Étape 5: Affichage des informations de déploiement
Write-Host "📊 Récupération des informations de déploiement..." -ForegroundColor Cyan

terraform output

Write-Host "🎉 Déploiement terminé avec succès!" -ForegroundColor Green
Write-Host "📍 Votre application est maintenant accessible." -ForegroundColor Green
Write-Host "📋 Utilisez 'terraform output' pour voir les détails de connexion." -ForegroundColor Green