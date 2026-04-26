# --- Data Sources ---
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

data "aws_vpc" "main" {
  filter {
    name   = "cidr"
    values = ["10.0.0.0/16"]  # ใช้ CIDR แทน ID ปลอดภัยกว่
  }
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }
  filter {
    name   = "map-public-ip-on-launch"
    values = ["false"]
  }
}

# --- Security Module ---
module "security" {
  source       = "./modules/security"
  project_name = var.project_name
  vpc_id       = data.aws_vpc.main.id  # ✅ ดึงมาอัตโนมัต
}

module "storage" {
  source                     = "./modules/storage"
  project_name               = var.project_name
  account_id                 = data.aws_caller_identity.current.account_id
  db_password                = var.db_password
  spectrum_role_arn          = module.security.spectrum_role_arn
  redshift_spectrum_role_arn = module.security.spectrum_role_arn
  private_subnet_ids         = data.aws_subnets.private.ids
  redshift_sg_id             = module.security.redshift_sg_id
}

# --- Streaming Module ---
module "streaming" {
  source          = "./modules/streaming"
  project_name    = var.project_name
  aws_region      = data.aws_region.current.id
  account_id      = data.aws_caller_identity.current.account_id
  s3_bucket_id    = module.storage.data_lake_bucket_id
  lambda_role_arn = module.security.lambda_role_arn
}