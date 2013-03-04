from fabric.api import task
from fabric.operations import local

__all__ = ["setup_tools"]

@task
def setup_vim():
  local("sudo apt-get install vim")
  local("cp -R configurations/vim/ ~/")

@task
def setup_gitconfig():
  local("sudo apt-get install git")
  local("cp -R configurations/gitconfig/ ~/")

@task
def setup_bash():
  local("sudo apt-get install bash")
  local("cp configurations/bash/.bashrc ~/")

@task
def setup_mc():
  local("sudo apt-get install mc")

@task
def setup_tools():
  setup_bash()
  setup_gitconfig()
  setup_vim()
  setup_mc()
