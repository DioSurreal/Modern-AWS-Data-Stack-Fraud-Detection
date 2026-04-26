output "data_lake_bucket_id" {
  value = aws_s3_bucket.data_lake.id
}

output "data_lake_arn" {
  value = aws_s3_bucket.data_lake.arn
}