# Heterogeneous System Integrator

An application to configure and schedule data interchange between heterogeneous systems. 

# Requirements
This aplications needs Docker to be installed: https://www.docker.com/products/docker-desktop/

## Deploy
### (FIRST DEPLOY) Build and deploy
```
python deploy.py -b
```

### Default Deploy (docker image already build)
```
python deploy.py
```

### Deploy without logs (detach-mode)
```
python deploy.py -d
```

## Undeploy
### Default undeploy
```
python undeploy.py
```

### Undeploy removing images (Have to rebuild after)
```
python undeploy.py -i
```

### Undeploy removing volumes (Flushes db data)
```
python undeploy.py -v
```

### Undeploy removing everything
```
python undeploy.py -f
```