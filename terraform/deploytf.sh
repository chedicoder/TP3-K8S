echo "Let's deploy the app service"
sleep 2
terraform init
terraform plan -out=tfplan
terraform apply -auto-approve "tfplan"