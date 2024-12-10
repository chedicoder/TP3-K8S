echo "Let's deploy the app service"
sleep 2
terraform init
terraform plan -lock=false -out=tfplan
terraform apply -auto-approve -lock=false "tfplan"