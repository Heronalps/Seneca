provider "aws" {
  region = "${var.aws_region}"
}
resource "aws_lambda_function" "test_lambda" {
  filename         = "test_lambda.zip"
  function_name    = "container_test_lambda"
  role             = "${var.aws_role}"
  handler          = "container_test_lambda.lambda_handler"
  runtime          = "python3.6"

  environment {
    variables = {
      foo = "bar"
    }
  }
}