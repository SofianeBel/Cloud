#!/bin/bash

# =============================================================================
# Script de Provisioning - TodoList Cloud Application
# =============================================================================
# Ce script installe et configure automatiquement toutes les dépendances
# nécessaires pour faire fonctionner l'application TodoList sur Ubuntu 22.04
# =============================================================================

set -e  # Arrêter le script en cas d'erreur

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher des messages colorés
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Fonction pour vérifier si une commande existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Fonction pour vérifier le système d'exploitation
check_os() {
    log_info "Vérification du système d'exploitation..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            if [[ "$ID" == "ubuntu" ]]; then
                log_success "Ubuntu détecté (version: $VERSION_ID)"
                return 0
            fi
        fi
    fi
    
    log_error "Ce script est conçu pour Ubuntu. Système détecté: $OSTYPE"
    exit 1
}

# Mise à jour du système
update_system() {
    log_info "Mise à jour du système..."
    sudo apt update -y
    sudo apt upgrade -y
    log_success "Système mis à jour"
}

# Installation des dépendances système
install_system_dependencies() {
    log_info "Installation des dépendances système..."
    
    local packages=(
        "python3"
        "python3-pip"
        "python3-venv"
        "python3-dev"
        "postgresql-client"
        "git"
        "curl"
        "wget"
        "unzip"
        "build-essential"
        "libpq-dev"
        "ufw"
    )
    
    for package in "${packages[@]}"; do
        log_info "Installation de $package..."
        sudo apt install -y "$package"
    done
    
    log_success "Dépendances système installées"
}

# Configuration de Python et pip
setup_python() {
    log_info "Configuration de Python..."
    
    # Vérifier la version de Python
    python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
    log_info "Version Python: $python_version"
    
    # Mettre à jour pip
    log_info "Mise à jour de pip..."
    python3 -m pip install --upgrade pip
    
    # Installer setuptools et wheel
    python3 -m pip install setuptools wheel
    
    log_success "Python configuré"
}

# Création du répertoire de l'application
setup_app_directory() {
    log_info "Configuration du répertoire de l'application..."
    
    local app_dir="/home/$(whoami)/app"
    
    if [ ! -d "$app_dir" ]; then
        mkdir -p "$app_dir"
        log_info "Répertoire créé: $app_dir"
    else
        log_info "Répertoire existant: $app_dir"
    fi
    
    # Changer vers le répertoire de l'application
    cd "$app_dir"
    
    log_success "Répertoire de l'application configuré"
}

# Installation des dépendances Python
install_python_dependencies() {
    log_info "Installation des dépendances Python..."
    
    # Créer requirements.txt s'il n'existe pas
    if [ ! -f "requirements.txt" ]; then
        log_info "Création du fichier requirements.txt..."
        cat > requirements.txt << EOF
Flask==2.3.3
psycopg2-binary==2.9.7
azure-storage-blob==12.17.0
python-dotenv==1.0.0
Werkzeug==2.3.7
requests==2.31.0
EOF
    fi
    
    # Installer les dépendances
    python3 -m pip install -r requirements.txt
    
    log_success "Dépendances Python installées"
}

# Configuration du firewall
setup_firewall() {
    log_info "Configuration du firewall UFW..."
    
    # Activer UFW
    sudo ufw --force enable
    
    # Autoriser SSH (port 22)
    sudo ufw allow 22/tcp
    log_info "Port SSH (22) autorisé"
    
    # Autoriser l'application Flask (port 5000)
    sudo ufw allow 5000/tcp
    log_info "Port Flask (5000) autorisé"
    
    # Afficher le statut
    sudo ufw status
    
    log_success "Firewall configuré"
}

# Création du fichier de service systemd
create_systemd_service() {
    log_info "Création du service systemd..."
    
    local service_file="/etc/systemd/system/todolist.service"
    local app_dir="/home/$(whoami)/app"
    local user=$(whoami)
    
    sudo tee "$service_file" > /dev/null << EOF
[Unit]
Description=TodoList Flask Application
After=network.target

[Service]
Type=simple
User=$user
WorkingDirectory=$app_dir
Environment=PATH=$app_dir/venv/bin
ExecStart=/usr/bin/python3 $app_dir/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    # Recharger systemd
    sudo systemctl daemon-reload
    
    # Activer le service (démarrage automatique)
    sudo systemctl enable todolist.service
    
    log_success "Service systemd créé et activé"
}

# Création d'un fichier d'environnement exemple
create_env_template() {
    log_info "Création du fichier d'environnement exemple..."
    
    cat > .env.example << EOF
# Configuration de la base de données PostgreSQL
DB_HOST=your-postgres-server.postgres.database.azure.com
DB_NAME=sbeldb
DB_USER=dbadmin
DB_PASS=SecurePass123!

# Configuration Azure Storage
STORAGE_ACCOUNT_NAME=sbelstorage
STORAGE_ACCOUNT_KEY=your-storage-key
CONTAINER_NAME=staticfiles

# Configuration Flask
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
EOF
    
    log_success "Fichier .env.example créé"
    log_warning "N'oubliez pas de copier .env.example vers .env et de configurer vos variables!"
}

# Fonction de vérification post-installation
verify_installation() {
    log_info "Vérification de l'installation..."
    
    # Vérifier Python
    if command_exists python3; then
        log_success "Python3: $(python3 --version)"
    else
        log_error "Python3 non trouvé"
        return 1
    fi
    
    # Vérifier pip
    if command_exists pip3; then
        log_success "Pip3: $(pip3 --version)"
    else
        log_error "Pip3 non trouvé"
        return 1
    fi
    
    # Vérifier PostgreSQL client
    if command_exists psql; then
        log_success "PostgreSQL client: $(psql --version)"
    else
        log_error "PostgreSQL client non trouvé"
        return 1
    fi
    
    # Vérifier les modules Python
    local modules=("flask" "psycopg2" "azure.storage.blob" "dotenv")
    for module in "${modules[@]}"; do
        if python3 -c "import $module" 2>/dev/null; then
            log_success "Module Python '$module' installé"
        else
            log_error "Module Python '$module' non trouvé"
            return 1
        fi
    done
    
    log_success "Toutes les vérifications sont passées!"
}

# Affichage des instructions finales
show_final_instructions() {
    log_info "Instructions finales:"
    echo
    echo "1. Copiez votre application Flask dans: /home/$(whoami)/app/"
    echo "2. Configurez vos variables d'environnement:"
    echo "   cp .env.example .env"
    echo "   nano .env"
    echo "3. Démarrez l'application:"
    echo "   sudo systemctl start todolist.service"
    echo "4. Vérifiez le statut:"
    echo "   sudo systemctl status todolist.service"
    echo "5. Consultez les logs:"
    echo "   sudo journalctl -u todolist.service -f"
    echo
    log_success "Provisioning terminé avec succès!"
}

# Fonction principale
main() {
    echo "============================================================================="
    echo "           Script de Provisioning - TodoList Cloud Application"
    echo "============================================================================="
    echo
    
    check_os
    update_system
    install_system_dependencies
    setup_python
    setup_app_directory
    install_python_dependencies
    setup_firewall
    create_systemd_service
    create_env_template
    verify_installation
    show_final_instructions
}

# Gestion des erreurs
trap 'log_error "Une erreur est survenue à la ligne $LINENO. Arrêt du script."; exit 1' ERR

# Exécution du script principal
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi