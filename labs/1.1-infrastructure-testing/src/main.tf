locals {
  s3_bucket_name = "terratest-lab-${var.username}-s3-bucket"
  vps_name       = "terratest-lab-${var.username}-vpc"
  subnet_name    = "terratest-lab-${var.username}-subnet"
  instance_name  = "terratest-lab-${var.username}-instance"
  sg_name        = "terratest-lab-${var.username}-sg"
}
resource "aws_vpc" "terratest-lab-vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = local.vps_name
  }
}
resource "aws_vpc_endpoint" "terratest-lab-endpoint" {
  vpc_id       = aws_vpc.terratest-lab-vpc.id
  service_name = "com.amazonaws.eu-central-1.s3"
}
resource "aws_subnet" "terratest-lab-subnet" {
  vpc_id            = aws_vpc.terratest-lab-vpc.id
  cidr_block        = "10.0.5.0/24"
  availability_zone = "eu-central-1a"
  tags = {
    Name = local.subnet_name
  }
}
resource "aws_s3_bucket" "terratest-lab-s3-bucket" {
  bucket = local.s3_bucket_name
  tags = {
    Name = local.s3_bucket_name
  }
}
resource "aws_security_group" "terratest-lab-sg" {
  name        = local.sg_name
  description = "Allow inbound traffic"
  vpc_id      = aws_vpc.terratest-lab-vpc.id
  ingress {
    description = "Allow inbound traffic from port 22"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "Allow inbound traffic from port 80"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_instance" "terratest-lab-instance" {
  ami                    = "ami-06dd92ecc74fdfb36"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.terratest-lab-subnet.id
  vpc_security_group_ids = [aws_security_group.terratest-lab-sg.id]
  tags = {
    Name = local.instance_name
  }
  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install -y nginx
              sudo systemctl start nginx
              sudo systemctl enable nginx
              sudo echo "Hello World from $(hostname -f)" > /var/www/html/index.html
              EOF
}
