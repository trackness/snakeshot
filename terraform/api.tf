variable "root_domain" {
  type = string
}

variable "sub_domain" {
  type    = string
  default = ""
}

locals {
  sub_domain = var.sub_domain != "" ? var.sub_domain : var.app_name
  fqdn       = "${local.sub_domain}.${data.aws_route53_zone.root_domain.name}"
}

data "aws_route53_zone" "root_domain" {
  name         = var.root_domain
  private_zone = false
}

resource "aws_apigatewayv2_api" "api" {
  name          = local.function_name
  protocol_type = "HTTP"
  target        = aws_lambda_function.lambda.arn
}

resource "aws_lambda_permission" "api_permissions" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.arn
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}

resource "aws_apigatewayv2_domain_name" "api" {
  domain_name = local.fqdn
  depends_on = [aws_acm_certificate_validation.cert]
  domain_name_configuration {
    certificate_arn = aws_acm_certificate.cert.arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }
}

resource "aws_route53_record" "sub_domain" {
  zone_id = data.aws_route53_zone.root_domain.zone_id
  name    = local.sub_domain
  type    = "A"

  alias {
    name                   = aws_apigatewayv2_domain_name.api.domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.api.domain_name_configuration[0].hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_acm_certificate" "cert" {
  domain_name       = local.fqdn
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "cert" {
  for_each = {
    for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.root_domain.zone_id
}

resource "aws_acm_certificate_validation" "cert" {
  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [for record in aws_route53_record.cert : record.fqdn]
}

resource "aws_apigatewayv2_api_mapping" "mapping" {
  api_id      = aws_apigatewayv2_api.api.id
  domain_name = aws_apigatewayv2_domain_name.api.id
  stage       = "$default"
}

resource "aws_apigatewayv2_integration" "slam" {
  api_id      = aws_apigatewayv2_api.api.id
  integration_type = "AWS"

  payload_format_version = "2.0"
}
