output "alb_dns_name" {
  description = "DNS name of the ALB"
  value       = aws_lb.app.dns_name
}

output "db_endpoint" {
  description = "Endpoint of the RDS instance"
  value       = aws_db_instance.default.address
}

output "db_port" {
  description = "Port of the RDS instance"
  value       = aws_db_instance.default.port
}