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

resource "aws_apigatewayv2_integration" "slam" {
  api_id      = aws_apigatewayv2_api.api.id
  integration_type = "AWS_PROXY"

  integration_uri = aws_lambda_function.lambda.invoke_arn
  payload_format_version = "2.0"
  timeout_milliseconds = 30000
}

resource "aws_apigatewayv2_route" "example" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "ANY /"

  target = "integrations/${aws_apigatewayv2_integration.slam.id}"
}

resource "aws_apigatewayv2_api_mapping" "mapping" {
  api_id      = aws_apigatewayv2_api.api.id
  domain_name = aws_apigatewayv2_domain_name.api.id
  stage       = aws_apigatewayv2_stage.default.name
}

locals {
  api_gw_cloudwatch_format = join(
    ",",
    formatlist(
      "\"%s\":\"$context.%s\"",
      [
        "requestTime",
        "requestId",
        "requestIp",
        "httpMethod",
        "status",
        "routeKey",
        "protocol",
        "path",
        "responseLength",
        "responseLatency",
        "integrationRequestId",
        "integrationResponseStatus",
        "integrationLatency",
        "integrationServiceStatus",
      ],
      [
        "requestTime",
        "requestId",
        "identity.sourceIp",
        "httpMethod",
        "status",
        "routeKey",
        "protocol",
        "path",
        "responseLength",
        "responseLatency",
        "integration.requestId",
        "integration.status",
        "integration.latency",
        "integration.integrationStatus",
      ]
    )
  )
}

resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.api.id
  name = "v1"
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn
    format = "{${local.api_gw_cloudwatch_format}}"
//    format = "{" +
//      "\"requestTime\": \"$context.requestTime\"," +
//      "\"requestId\":\"$context.requestId\"," +
//      "\"ip\": \"$context.identity.sourceIp\"," +
//      "\"httpMethod\":\"$context.httpMethod\"," +
//      "\"status\":\"$context.status\"," +
//      "\"routeKey\": \"$context.routeKey\"," +
//      "\"protocol\":\"$context.protocol\"," +
//      "\"path\":\"$context.path\"," +
//      "\"queryString\":\"$$context.requestOverride.querystring.querystring_name\"," +
//      "\"responseLength\":\"$context.responseLength\"," +
//      "\"responseLatency\":\"$context.responseLatency\"," +
//      "\"integrationRequestId\": \"$context.integration.requestId\"," +
//      "\"integrationResponseStatus\": \"$context.integration.status\"," +
//      "\"integrationLatency\": \"$context.integration.latency\"," +
//      "\"integrationServiceStatus\": \"$context.integration.integrationStatus\"" +
//    "}"
  }
  auto_deploy = true
}

// Cloudwatch

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.api.name}"
  retention_in_days = 7
}
