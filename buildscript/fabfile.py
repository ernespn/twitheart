from fabric.api import env, task, run, settings, hide, show
from fabric.utils import abort
from tasks import *
from fabric.colors import green, yellow, red

@task
def deploy():
   #with settings(hide('running', 'stdout'),show('debug'),warn_only=True):
   with settings(hide('running', 'stdout'),warn_only=True):
      print(green("checking dependencies"))
      if not "/nodejs" in env.run("whereis nodejs", capture=True):
        print(yellow("Setting up nodejs dependencies "))
        dependencies.install_nodejs()
      if not "/nginx" in env.run("whereis nginx", capture=True):
        print(yellow("Setting up nginx dependencies"))
        dependencies.install_nginx()
      print(green("Installing the artifacts..."))
      artifacts.installingArtifacts()
      print(green("Restarting the services..."))
      services.restartAll()
      #restartServices()

