data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }
}

locals {
  default_subnet_ids = data.aws_subnets.default.ids
  db_subnet_ids      = slice(local.default_subnet_ids, 0, 2)
}