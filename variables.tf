variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "SBELTerraform"
}

variable "location" {
  description = "Azure location"
  type        = string
  default     = "westeurope"
}

variable "vnet_name" {
  description = "Name of the virtual network"
  type        = string
  default     = "sbel-vnet"
}

variable "subnet_name" {
  description = "Name of the subnet"
  type        = string
  default     = "sbel-subnet"
}

variable "public_ip_name" {
  description = "Name of the public IP"
  type        = string
  default     = "sbel-public-ip"
}

variable "ssh_key_name" {
  description = "Name of the SSH key"
  type        = string
  default     = "sbel-ssh-key"
}

variable "nsg_name" {
  description = "Name of the network security group"
  type        = string
  default     = "sbel-nsg"
}

variable "nic_name" {
  description = "Name of the network interface"
  type        = string
  default     = "sbel-nic"
}

variable "vm_name" {
  description = "Name of the virtual machine"
  type        = string
  default     = "sbel-vm"
}

variable "vm_size" {
  description = "Size of the VM"
  type        = string
  default     = "Standard_B1s"
}

variable "admin_username" {
  description = "Admin username for the VM"
  type        = string
  default     = "azureuser"
}

// Ajouter des variables pour le stockage
variable "storage_account_name" {
  description = "Name of the storage account"
  type        = string
  default     = "sbelstorage"
}

variable "container_name" {
  description = "Name of the blob container"
  type        = string
  default     = "staticfiles"
}

variable "db_server_name" {
  description = "Name of the PostgreSQL server"
  type        = string
  default     = "sbel-db-server"
}

variable "db_name" {
  description = "Name of the database"
  type        = string
  default     = "sbeldb"
}

variable "db_admin_login" {
  description = "Admin login for the database"
  type        = string
  default     = "dbadmin"
}

variable "db_admin_password" {
  description = "Admin password for the database (sensitive)"
  type        = string
  sensitive   = true
}