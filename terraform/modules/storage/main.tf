# 1. S3 Bucket
resource "aws_s3_bucket" "data_lake" {
  bucket        = "${var.project_name}-data-lake-${var.account_id}"
  force_destroy = true
}

# 2. Redshift Serverless Namespace
resource "aws_redshiftserverless_namespace" "banking_namespace" {
  namespace_name      = "${var.project_name}-namespace"
  db_name             = "fraud_db"
  admin_username      = "adminuser"
  admin_user_password = var.db_password
  iam_roles           = [var.redshift_spectrum_role_arn]
}

# 3. Redshift Serverless Workgroup
resource "aws_redshiftserverless_workgroup" "banking_workgroup" {
  workgroup_name      = "${var.project_name}-workgroup"
  namespace_name      = aws_redshiftserverless_namespace.banking_namespace.namespace_name
  base_capacity       = 8
  publicly_accessible = true
  subnet_ids          = var.private_subnet_ids
  security_group_ids  = [var.redshift_sg_id]
}