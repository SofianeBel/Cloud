output "public_ip_address" {
  description = "The public IP address of the VM"
  value       = azurerm_public_ip.public_ip.ip_address
}

output "vm_name" {
  description = "The name of the VM"
  value       = azurerm_linux_virtual_machine.vm.name
}

// Ajouter output pour le stockage une fois ajouté