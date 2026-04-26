variable "project_name" { type = string }
variable "account_id"   { type = string }
variable "db_password"  { type = string }
variable "spectrum_role_arn" {
  description = "IAM Role ARN for Redshift Spectrum"
  type        = string
}
variable "redshift_spectrum_role_arn" {
  type = string
}

variable "private_subnet_ids" {
  type = list(string)
}

variable "redshift_sg_id" {
  type = string
}



