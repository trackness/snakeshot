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
//  stage       = "$default"
  stage       = aws_apigatewayv2_stage.default.name
}

resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.api.id
  name = "default"
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn
    format = ""
  }
}

resource "aws_apigatewayv2_integration" "slam" {
  api_id      = aws_apigatewayv2_api.api.id
  integration_type = "AWS_PROXY"

  integration_uri = aws_lambda_function.lambda.invoke_arn
  payload_format_version = "2.0"
  timeout_milliseconds = 30000
}

// Cloudwatch

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.api.name}"
  retention_in_days = 7
}

//// supposed to be per-account, not per-repo
//resource "aws_api_gateway_account" "api_gw_cloudwatch" {
//  cloudwatch_role_arn = aws_iam_role.api_gw_cloudwatch.arn
//}
//
//// copied from lambda, need to assign permissions as mentioned here
//// https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-logging.html

//resource "aws_iam_role" "api_gw_cloudwatch" {
//  name        = "api-gw-cloudwatch-${aws_apigatewayv2_api.api.name}"
//  path        = "/"
//  description = "Role for CloudWatch logging"
//
//  assume_role_policy = data.aws_iam_policy_document.api_gw_assume_role.json
//}
//
//data "aws_iam_policy_document" "api_gw_assume_role" {
//  statement {
//    effect = "Allow"
//    actions = ["sts:AssumeRole"]
//    principals {
//      type        = "Service"
//      identifiers = ["apigateway.amazonaws.com"]
//    }
//  }
//}
//
//resource "aws_iam_role_policy" "api_gw_cloudwatch" {
//  name = "api-gw-cloudwatch-role-${local.function_name}"
//  role = aws_iam_role.api_gw_cloudwatch.id
//  policy = data.aws_iam_policy_document.api_gw_cloudwatch.json
//}
//
//data "aws_iam_policy_document" "api_gw_cloudwatch" {
//  statement {
//    effect = "Allow"
//    actions = ["logs:CreateLogStream", "logs:PutLogEvents"]
//    resources = ["${aws_cloudwatch_log_group.lambda.arn}:*"]
//  }
//}

//# Attach AmazonAPIGatewayPushToCloudWatchLogs policy to API Gateway role to allow it to write logs
//resource "aws_iam_role_policy_attachment" "attach_cloudwatch_logging" {
//  role       = aws_iam_role.api_gw_cloudwatch.name
//  policy_arn = data.aws_iam_policy.AmazonAPIGatewayPushToCloudWatchLogs.arn
//}
//
//# Enable logging for the API Gateway
//resource "aws_api_gateway_account" "main" {
//  cloudwatch_role_arn = aws_iam_role.api_gw_cloudwatch.arn
//}



//resource "aws_iam_role" "api_gw_cloudwatch" {
//  name = "api-gw-cloudwatch-role-${local.function_name}"
//  path = "/"
//  assume_role_policy = data.aws_iam_policy_document.api_gw_cloudwatch.json
//}
//
//data "aws_iam_policy_document" "api_gw_cloudwatch" {
//  statement {
//    effect = "Allow"
//    actions = ["logs:CreateLogStream"]
//    resources = [aws_cloudwatch_log_group.api_gw.arn]
//  }
//
//  statement {
//    effect    = "Allow"
//    actions   = ["logs:PutLogEvents"]
//    resources = ["${aws_cloudwatch_log_group.api_gw.arn}:*"]
//  }
//}

//resource "aws_iam_policy" "api_gw_cloudwatch" {
//  policy = data.aws_iam_policy_document.api_gw_cloudwatch.json
//}

//resource "aws_iam_role_policy_attachment" "api_gw_cloudwatch" {
//  policy_arn = aws_iam_policy.api_gw_cloudwatch.arn
//  role = aws_iam_role.lambda_exec_role.name
//}
