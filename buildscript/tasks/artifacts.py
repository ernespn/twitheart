from fabric.api import env, task
from fabric.operations import local
from fabric.colors import red

__all__ = ["installingArtifacts"]

@task
def installingArtifacts():
  #happens only in local machine
  copyArtifactsToTmp()
  injectConfigs()
  zipArtifacts()
  sendArtifacts()
  #happens in the remote server or in local
  unzipArtifacts()
  copyArtifactsToLocation()
  #TODO : clean temporal files

@task
def cleanTmpFolder():
  try: 
    res = local("test -d "+env.artifactFolder)
    local("rm -R "+env.artifactFolder)
  except SystemExit, e:
    print(red("Folder not found, creating it ..."))  
  local("mkdir "+env.artifactFolder)
  local("mkdir "+env.artifactTemp)

@task
def copyArtifactsToTmp():
  cleanTmpFolder()
  local("cp -r ../client "+env.artifactTemp)
  local("cp -r ../nginx "+env.artifactTemp)
  local("cp -r ../server "+env.artifactTemp)

@task
def injectConfigs():
   local("sed -i s/{{SERVER_NAME}}/"+env.app_server_name+"/g "+env.artifactTemp+"client/index.html")
   local("sed -i s/{{SERVER_NAME}}/"+env.app_server_name+"/g "+env.artifactTemp+"client/js/map.js")
   local("sed -i s/{{app_server_port}}/"+env.app_server_port+"/g "+env.artifactTemp+"server/server.js")
   local("sed -i s/{{app_server_port}}/"+env.app_server_port+"/g "+env.artifactTemp+"nginx/nodejs-server")
   local("sed -i s/{{nginx_client_port}}/"+escaping(env.nginx_client_port)+"/g "+env.artifactTemp+"nginx/nodejs-client") 
   local("sed -i s/{{nginx_client_path}}/"+escaping(env.nginx_client_path)+"/g "+env.artifactTemp+"nginx/nodejs-client") 
   local("sed -i s/{{nginx_client_server}}/"+env.nginx_client_server+"/g "+env.artifactTemp+"nginx/nodejs-client") 
   local("sed -i s/{{nginx_server_server}}/"+env.nginx_server_server+"/g "+env.artifactTemp+"nginx/nodejs-server")
   local("sed -i s/{{nginx_server_port}}/"+env.nginx_server_port+"/g "+env.artifactTemp+"nginx/nodejs-server")

@task
def zipArtifacts():
  local("find "+env.artifactTemp+" -name '*~' -exec rm {} \;")
  local("cd "+env.artifactTemp+" && tar -zcvf "+env.artifactFolder+"artifacts.tgz .")

@task
def sendArtifacts():
  local("rsync -aq "+env.source_path+"artifacts.tgz "+env.destiny_path)

@task
def unzipArtifacts():
  env.run("cd "+env.destiny_path+" && tar -zxvf "+env.destiny_path+"artifacts.tgz ./")

@task
def copyArtifactsToLocation():
  env.run("cp "+env.destiny_path+"nginx/* "+env.nginx_config_available) 
  env.run("cp "+env.destiny_path+"nginx/* "+env.nginx_config_enabled) 
  try:
    env.run("test -d "+env.app_path)
    env.run("rm -R "+env.app_path)
  except SystemExit, e:
    print(red("App folder not found, creating app folder"))
  env.run("mkdir "+env.app_path)
  env.run("mkdir "+env.nginx_server_path+"/")  
  env.run("cp -R "+env.destiny_path+"server/* "+env.nginx_server_path+"/") 
  env.run("mkdir "+env.nginx_client_path+"/")
  env.run("cp -R "+env.destiny_path+"client/* "+env.nginx_client_path+"/") 

def escaping(string):
  return string.replace('/', '\\\/')
