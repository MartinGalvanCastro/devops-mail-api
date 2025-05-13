resource "aws_ssm_parameter" "db_host" {
  name  = "/blacklist-api/DB_HOST"
  type  = "String"
  value = aws_db_instance.default.address
}

resource "aws_ssm_parameter" "db_port" {
  name  = "/blacklist-api/DB_PORT"
  type  = "String"
  value = aws_db_instance.default.port
}
resource "aws_ssm_parameter" "db_user" {
  name  = "/blacklist-api/DB_USER"
  type  = "String"
  value = var.db_username
}
resource "aws_ssm_parameter" "db_password" {
  name  = "/blacklist-api/DB_PASSWORD"
  type  = "SecureString"
  value = var.db_password
}
resource "aws_ssm_parameter" "db_name" {
  name  = "/blacklist-api/DB_NAME"
  type  = "String"
  value = var.db_name
}
resource "aws_ssm_parameter" "db_driver" {
  name  = "/blacklist-api/DB_DRIVER"
  type  = "String"
  value = var.db_driver
}

resource "aws_ssm_parameter" "new_relic_license_key" {
  name  = "/blacklist-api/NEW_RELIC_LICENSE_KEY"
  type  = "String"
  value = var.NEW_RELIC_LICENSE_KEY
}