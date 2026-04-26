output "lambda_role_arn" {
  value = aws_iam_role.lambda_exec_role.arn
}

output "spectrum_role_arn" {
  value = aws_iam_role.redshift_spectrum_role.arn
}
output "redshift_sg_id" {
  value = aws_security_group.redshift_sg.id
}