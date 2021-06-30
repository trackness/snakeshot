locals {
  function_name = "${var.app_name}-${var.environment}"
  zip_target    = var.zip_target != 0 ? var.zip_target : var.app_name
}
