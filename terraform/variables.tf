variable "app_name" {
  type = string
}

variable "handler" {
  type    = string
  default = "main.lambda_handler"
}

variable "owner" {
  type    = string
  default = ""
}

variable "repo" {
  type    = string
  default = ""
}

variable "account_id" {
  type = string
}

variable "runtime" {
  type    = string
  default = "python3.8"
}

variable "region" {
  type    = string
  default = "eu-west-2"
}

variable "environment" {
  type = string
}

variable "zip_target" {
  type    = string
  default = ""
}

variable "commit" {
  type    = string
  default = ""
}

variable "tag" {
  type    = string
  default = ""
}

variable "log_level" {
  type    = string
  default = "error"
}

variable "memory_size" {
  type    = number
  default = 0
}

variable "timeout" {
  type    = number
  default = 0
}
