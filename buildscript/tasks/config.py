from fabric.api import env, task
from fabric.operations import local

env.artifactFolder = "/tmp/artifact/"
env.artifactTemp = env.artifactFolder+"dist/"

@task
def localhost():
  env.run = local
  env.hosts = ['localhost']
  env.app_server_port = "3005"
  env.app_server_name = "localhost:3005"
  env.app_path = "/usr/share/nginx/nodejs-twit"
  env.nginx_client_path = env.app_path+"/client"  #Permission required for user
  env.nginx_client_port = "3080"
  env.nginx_client_server = "localhost"
  env.nginx_server_server = "localhost"
  env.nginx_server_port = "3006"
  env.nginx_server_path = env.app_path+"/server" #Permission required for user
  env.nginx_config_available = "/etc/nginx/sites-available"         #Permission required for user
  env.nginx_config_enabled = "/etc/nginx/sites-enabled"             #Permission required for user
  env.source_path = env.artifactFolder
  env.destiny_path = env.artifactFolder+"artifactDist/"                   #Permission required for user

@task
def remote():  
  env.run = run
  env.user = "worker"
  env.password = "qwerty1234"
  env.hosts = ['111.222.333.444']
  env.serverport = "3005"
  env.servername = "twittersrv.domain.com"
  env.nginx_client_path = "/usr/share/nginx/nodejs-twit/client"
  env.nginx_client_server = "twitter.domain.com"
  env.nginx_server_server = "twittersvr.domain.com"
  env.nginx_server_port = "80"

