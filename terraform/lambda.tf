resource "aws_lambda_function" "lambda" {
  function_name = local.function_name
  role          = aws_iam_role.lambda_exec_role.arn

  handler      = local.handler
  memory_size  = var.memory_size != 0 ? var.memory_size : 128
  runtime      = var.runtime
  timeout      = var.timeout != 0 ? var.timeout : 3
  package_type = "Zip"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      APP_NAME    = var.app_name
      OWNER       = var.owner
      REGION      = var.region
      LOG_LEVEL   = var.log_level
      VERSION     = var.tag == "" ? var.commit : var.tag
    }
  }
}

// Execution role

resource "aws_iam_role" "lambda_exec_role" {
  name        = "lambda-exec-role-${local.function_name}"
  path        = "/"
  description = "Role for lambda to publish to sns function"

  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}

data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

// Artefact

locals {
  source_dir = "${path.module}/../${local.zip_target}"
}

data "archive_file" "lambda_zip" {
  type             = "zip"
  output_file_mode = "0666"

  source_dir  = local.source_dir
  excludes    = ["${local.source_dir}/bin/*"]
  output_path = "${path.module}/${var.app_name}.zip"
}

// Cloudwatch

resource "aws_cloudwatch_log_group" "lambda" {
  name = "/aws/lambda/${aws_lambda_function.lambda.function_name}"
  retention_in_days = 7
}

data "aws_iam_policy_document" "lambda_cloudwatch_policy" {
  statement {
    effect = "Allow"
    actions = ["logs:CreateLogStream"]
    resources = [aws_cloudwatch_log_group.lambda.arn]
  }

  statement {
    effect    = "Allow"
    actions   = ["logs:PutLogEvents"]
    resources = ["${aws_cloudwatch_log_group.lambda.arn}:*"]
  }
}

resource "aws_iam_role_policy" "test_lambda_cloudwatch_policy" {
  name = "lambda-cloudwatch-policy-${local.function_name}-cloudwatch-policy"
  policy = data.aws_iam_policy_document.lambda_cloudwatch_policy.json
  role = aws_iam_role.lambda_exec_role.id
}

