from fabric.api import task, env
from fabric.operations import local, sudo

@task
def install_nodejs():
  env.run("sudo apt-get install -y --no-upgrade nodejs npm")

@task
def install_nginx():
  env.run("sudo apt-get -y --no-upgrade install nginx")
  #env.run("sudo cp configurations/nginx/nginx.conf /etc/nginx/")

