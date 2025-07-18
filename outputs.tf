output "public_ip_address" {
  description = "The public IP address of the VM"
  value       = azurerm_public_ip.public_ip.ip_address
}

output "vm_name" {
  description = "The name of the VM"
  value       = azurerm_linux_virtual_machine.vm.name
}

// Outputs pour le stockage Azure
output "storage_account_name" {
  description = "Nom du compte de stockage Azure"
  value       = azurerm_storage_account.storage.name
}

output "storage_account_key" {
  description = "Clé d'accès primaire du compte de stockage"
  value       = azurerm_storage_account.storage.primary_access_key
  sensitive   = true
}

output "storage_connection_string" {
  description = "Chaîne de connexion du compte de stockage"
  value       = azurerm_storage_account.storage.primary_connection_string
  sensitive   = true
}

output "container_name" {
  description = "Nom du conteneur de stockage"
  value       = azurerm_storage_container.container.name
}

// Outputs pour la base de données PostgreSQL
output "db_server_fqdn" {
  description = "FQDN du serveur PostgreSQL"
  value       = azurerm_postgresql_flexible_server.db_server.fqdn
}

output "db_name" {
  description = "Nom de la base de données"
  value       = azurerm_postgresql_flexible_server_database.db.name
}