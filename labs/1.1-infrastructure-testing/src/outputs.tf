output "bucket_name" {
  description = "Name of the bucket created"
  value       = aws_s3_bucket.terratest-lab-s3-bucket.id
}

output "bucket_arn" {
  description = "ARN of the bucket created"
  value       = aws_s3_bucket.terratest-lab-s3-bucket.arn
}

