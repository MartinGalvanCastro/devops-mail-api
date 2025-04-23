version: 0.2

phases:
  install:
    commands:
      - echo "Installing dev dependencies…" && pip install uv && uv sync --dev

  pre_build:
    commands:
      - echo "Running tests…" && uv run manage.py test
      - echo "Retrieving AWS account ID…" && ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
      - echo "Logging in to Amazon ECR…" && docker login -u AWS -p $(aws ecr get-login-password --region $AWS_REGION) $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

  build:
    commands:
      - echo "Building Docker image with build args…" && docker build --platform $DOCKER_PLATFORM --target $DOCKER_TARGET --build-arg APP_VERSION=$APP_VERSION --build-arg DB_HOST=$DB_HOST --build-arg DB_PORT=$DB_PORT --build-arg DB_USER=$DB_USER --build-arg DB_PASSWORD=$DB_PASSWORD --build-arg DB_NAME=$DB_NAME --build-arg DB_DRIVER=$DB_DRIVER -t $ECR_REPO:latest .
      - echo "Tagging image for ECR…" && docker tag $ECR_REPO:latest $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest

  post_build:
    commands:
      - echo "Pushing image to ECR…" && docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest
      - echo "Build complete on $(date)"
