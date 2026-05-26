output "ec2_ip" {
  value = aws_instance.Flask-TodoAPP.public_ip
}