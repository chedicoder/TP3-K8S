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
  default     = "flask-app-chedi"
}

variable "subscription_id" {
  description = "The Azure Subscription ID"
  type        = string
  default     = "8e9dcb14-acc5-43cd-8641-53c8180ccfa7"
}
