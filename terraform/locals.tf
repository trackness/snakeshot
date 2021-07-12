locals {
  function_name = var.app_name
  zip_target    = var.zip_target != 0 ? var.zip_target : var.app_name
  handler = "${var.app_name}.${var.handler}"
}
