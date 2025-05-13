variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Base name for all resources"
  type        = string
  default     = "blacklist-api"
}

variable "cluster_name" {
  description = "ECS cluster name"
  type        = string
  default     = "Blacklist-API-Cluster"
}

variable "service_name" {
  description = "ECS service and container name"
  type        = string
  default     = "Blacklist-API-fargate-service"
}

variable "image_uri" {
  description = "Full ECR image URI"
  type        = string
  default     = "501257812093.dkr.ecr.us-east-1.amazonaws.com/devops/blacklist-api-python:latest"
}

variable "vpc_id" {
  description = "VPC ID to deploy resources into"
  type        = string
  default     = "vpc-0b2179f84dc8abd4e"
}

variable "db_name" {
  description = "RDS database name"
  type        = string
  default     = "mail_db"
}

variable "db_username" {
  description = "RDS master username"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "RDS master password"
  type        = string
  default     = "postgres"
  sensitive   = true
}

variable "db_driver" {
  description = "Database connection driver string"
  type        = string
  default     = "postgresql+psycopg"
}

variable "desired_count" {
  description = "Number of ECS tasks"
  type        = number
  default     = 1
}

variable "task_cpu" {
  description = "CPU units for Fargate task"
  type        = string
  default     = "256"
}

variable "task_memory" {
  description = "Memory (MiB) for Fargate task"
  type        = string
  default     = "512"
}

variable "NEW_RELIC_LICENSE_KEY" {
  description = "New Relic license key"
  type        = string
  default     = "fd0708e1b48476b79eed54a0a501912fFFFFNRAL"
  sensitive   = true
}