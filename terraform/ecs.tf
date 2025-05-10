
// ecs.tf
resource "aws_ecs_cluster" "main" {
  name = var.cluster_name
}

resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project_name}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name            = var.service_name
      image           = var.image_uri
      essential       = true
      portMappings    = [{ containerPort = 8000, hostPort = 8000, protocol = "tcp" }]
      environment     = [
        { name = "DB_HOST",      value = aws_db_instance.default.address },
        { name = "DB_PORT",      value = tostring(aws_db_instance.default.port) },
        { name = "DB_USER",      value = var.db_username },
        { name = "DB_PASSWORD",  value = var.db_password },
        { name = "DB_NAME",      value = var.db_name },
        { name = "DB_DRIVER",    value = var.db_driver }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_logs.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = var.service_name
        }
      }
    }
  ])
}

resource "aws_ecs_service" "app" {
  name            = var.service_name
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  deployment_controller {
    type = "ECS"
  }

  health_check_grace_period_seconds = 60

  network_configuration {
    subnets          = local.default_subnet_ids
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.ecs_tg.arn
    container_name   = var.service_name
    container_port   = 8000
  }

  depends_on = [aws_lb_listener.frontend]
}