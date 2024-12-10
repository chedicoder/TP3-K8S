terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "4.13.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

# Create a resource group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = "North Europe"
}


# Create a service plan. 
resource "azurerm_service_plan" "asp" {
  name                = var.service_plan_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name = "B1"
}

# Create a web app
resource "azurerm_linux_web_app" "linux_webapp" {
  name                = var.web_app_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id = azurerm_service_plan.asp.id
  public_network_access_enabled = true

  site_config {
    application_stack {
      python_version = "3.10"
    }
  }
  # app_settings = {
  #   "FLASK_APP" = "python-webapp/app.py"
  # }
}

output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "service_plan_name" {
  value = azurerm_service_plan.asp.name
}

output "web_app_name" {
  value = azurerm_linux_web_app.linux_webapp.name
}