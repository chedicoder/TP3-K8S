variable "resource_group_name" {
  description = "The name of the Azure Resource Group."
  type        = string
  default     = "flask-app-rg"
}

variable "service_plan_name" {
  description = "The name of the Azure Service Plan."
  type        = string
  default     = "flask-app-plan"
}

variable "web_app_name" {
  description = "The name of the Azure Web App."
  type        = string
  default     = "flask-app-eya"
}

variable "subscription_id" {
  description = "The Azure Subscription ID"
  type        = string
  default     = "f6285103-f177-45c1-b6f8-de4cbd1ffb04"
}
