# Heterogeneous System Integrator

An application to configure and schedule data interchange between heterogeneous systems. 

## Deploy
### (FIRST DEPLOY) Build and deploy
'''python
python deploy.py -b
'''

### Default Deploy (docker image already build):
'''python
python deploy.py
'''

### Deploy without logs (detach-mode)
'''python
python deploy.py -d
'''

## Undeploy
### Default undeploy
'''python
python undeploy.py
'''

### Remove images undeploy (Have to rebuild after)
'''python
python undeploy.py -i
'''

### Remove volumes undeploy (Flushes db data)
'''python
python undeploy.py -v
'''

### Remove both undeploy
'''python
python undeploy.py -f
'''