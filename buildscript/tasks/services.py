from fabric.api import env, task
from fabric.operations import local
from fabric.colors import red, yellow, green

__all__ = ["restartAll"]

@task
def restartAll():
  restartNode()
  restartNginx()

@task
def restartNode():
  #env.run("killall node")
  print(yellow("starting nodejs ..."))
  env.run("nohup nodejs "+env.nginx_server_path+"/server.js & ")
  print(green("started nodejs"))

@task
def restartNginx():
  print(yellow("Killing previous services..."))
  env.run("fuser -k "+env.nginx_server_port+"/tcp")
  env.run("fuser -k "+env.app_server_port+"/tcp")
  env.run("fuser -k "+env.nginx_client_port+"/tcp")
  print(yellow("restarting nginx ..."))
  env.run("/etc/init.d/nginx stop")
  env.run("/etc/init.d/nginx start")
  print(green("nginx restarted ..."))
