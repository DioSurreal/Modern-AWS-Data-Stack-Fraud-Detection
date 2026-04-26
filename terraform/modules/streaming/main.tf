
resource "aws_kinesis_stream" "transaction_stream" {
  name             = "${var.project_name}-stream"
  shard_count      = 1 # สำหรับโปรเจกต์นี้ 1 shard ก็เหลือๆ ครับ
  retention_period = 24
}


resource "aws_ecr_repository" "lambda_repo" {
  name                 = "${var.project_name}-lambda-repo"
  force_delete         = true
  image_tag_mutability = "MUTABLE"
}

resource "aws_lambda_function" "fraud_detector" {
  function_name = "${var.project_name}-fraud-detector"
  role          = var.lambda_role_arn
  
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.lambda_repo.repository_url}:latest"
  
  timeout       = 30

  environment {
    variables = {
      S3_BUCKET = var.s3_bucket_id
    }
  }

  depends_on = [null_resource.docker_push]
}

resource "aws_lambda_event_source_mapping" "kinesis_trigger" {
  event_source_arn  = aws_kinesis_stream.transaction_stream.arn
  function_name     = aws_lambda_function.fraud_detector.arn
  starting_position = "LATEST"
  batch_size        = 100 # รับข้อมูลทีละก้อน
}

resource "null_resource" "docker_push" {
  depends_on = [aws_ecr_repository.lambda_repo]
  triggers = {
    python_code = filemd5("${path.module}/assets/lambda_function.py")
    docker_file = filemd5("${path.module}/assets/Dockerfile")
  }

provisioner "local-exec" {
  interpreter = ["PowerShell", "-Command"]
  command = join(" ; ", [
    "$ECR_URL = '${var.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com'",
    "aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin $ECR_URL",
    "docker build --platform linux/amd64 --provenance=false -t \"$ECR_URL/${var.project_name}-lambda-repo:latest\" ${path.module}/assets/",
    "docker push \"$ECR_URL/${var.project_name}-lambda-repo:latest\""
  ])
}
}