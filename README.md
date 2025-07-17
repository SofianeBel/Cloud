# Mini-Projet : Déploiement Automatisé d’une Infrastructure Cloud avec Terraform

## Objectif
Mettre en place une infrastructure cloud complète sur Azure en utilisant Terraform pour automatiser la création d’une machine virtuelle, d’un stockage blob et d’une base de données PostgreSQL, avec une application Flask déployée dessus.

## Prérequis
- Installer Terraform (déjà fait via commande).
- Installer Azure CLI et se connecter avec `az login`.
- Avoir une clé SSH (~/.ssh/id_rsa.pub).
- Installer Ansible pour le provisioning.

## Fichiers
- `main.tf`: Configuration Terraform principale.
- `variables.tf`: Variables pour dynamiser.
- `outputs.tf`: Outputs comme IP publique.
- `terraform.tfvars`: Valeurs sensibles (e.g., mot de passe DB).
- `app.py`: Application Flask avec intégration stockage et DB.
- `playbook.yml`: Ansible pour configurer la VM.
- `inventory.ini`: Généré dynamiquement.

## Étapes d'utilisation
1. Configurer l'authentification Azure : Exécutez `az login`.
2. Mettre à jour `terraform.tfvars` avec un mot de passe DB sécurisé.
3. Initialiser : `terraform init`.
4. Déployer : `terraform apply`.
5. Accéder à l'app via l'IP publique output sur port 5000.
6. Tester upload via /upload, CRUD via /files.
7. Détruire : `terraform destroy`.

## Rapport
- Infrastructure déployée avec VM Ubuntu, stockage blob privé, PostgreSQL managé.
- App Flask lit/écrit sur stockage via identité managée, CRUD sur DB.
- Problèmes : Assurer auth Azure ; creds DB sensibles.
- Captures : (À ajouter manuellement après déploiement).