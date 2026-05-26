resource "aws_instance" "Flask-TodoAPP" {
  ami                    = data.aws_ami.amiID.id
  instance_type          = "t3.micro"
  key_name               = var.key_aws
  vpc_security_group_ids = [aws_security_group.todo-sg.id]
  availability_zone      = var.zone1
  user_data = file("${path.module}/user_data.sh")

  tags = {
    Name    = "Flask-TodoAPP"
    Project = "TodoAPP"
  }

}

resource "aws_ec2_instance_state" "web-state" {
  instance_id = aws_instance.Flask-TodoAPP.id
  state       = "running"
}
