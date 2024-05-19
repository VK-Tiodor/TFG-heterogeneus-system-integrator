# Heterogeneous System Integrator
A web application that serves as middleware between a company and any enterprise management system. The goal is to facilitate data transfer between heterogeneous systems and enable the automation of these processes without the need for developing specific integrations. 

Parts: 
 - **The Interface**: allows the user to interact with the application. Composed by an API and a graphical user interface that consumes it.
 - **The Logic**: facilitates the design and execution of synchronization processes.
 - **The Infrastructure**: enables the persistence of synchronization process configurations and their execution through a distributed system.

The purpose of this application is to allow users to configure automatic data synchronizations from the graphical interface or by requests to the API endpoints. Users will be able to configure synchronizations by choosing which data to download, what transformations to apply to them, which system to send them to, and when or how frequently to do so. This system will be prepared to download and upload data through various types of connections. It will be able to filter the data that will be uploaded, sending only what is strictly necessary. It will also allow configuring data transformations, at value level and at message format level. It will accept synchronizations from multiple sources. Synchronizations can be scheduled to run without user interaction and without blocking the system.

# Requirements
### Docker
https://www.docker.com/products/docker-desktop/

### Python
https://www.python.org/downloads/release/python-3119/

# How to deploy
### (FIRST DEPLOY) Build and deploy
```bash
python deploy.py -b
```

### Default Deploy (docker image already build)
```bash
python deploy.py
```

### Deploy without logs (detach-mode)
```bash
python deploy.py -d
```

---

Then open your web browser and go to: http://localhost:8000/

# How to undeploy
### Default undeploy
```bash
python undeploy.py
```

### Undeploy removing images (Have to rebuild after)
```bash
python undeploy.py -i
```

### Undeploy removing volumes (Flushes db data)
```bash
python undeploy.py -v
```

### Undeploy removing everything
```bash
python undeploy.py -f
```