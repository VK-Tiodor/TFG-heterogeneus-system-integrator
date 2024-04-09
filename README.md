# Heterogeneous System Integrator

An application to configure and schedule data interchange between heterogeneous systems. 

## Deploy
### (FIRST DEPLOY) Build and deploy
`python deploy.py -b`

### Default Deploy (docker image already build)
`python deploy.py`

### Deploy without logs (detach-mode)
`python deploy.py -d`

## Undeploy
### Default undeploy
`python undeploy.py`

### Remove images undeploy (Have to rebuild after)
`python undeploy.py -i`

### Remove volumes undeploy (Flushes db data)
`python undeploy.py -v`

### Remove both undeploy
`python undeploy.py -f`