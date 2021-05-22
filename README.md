# Jenkins job launcher

## User guide
### Python package
#### Installation
```bash
pip install job-laucnher
```
#### Usage
```bash
export JENKINS_USER=admin
export JENKINS_PASSWORD=admin
job-launcher run -r job_launcher_config.yaml
```

### Pyz archive
#### Usage
```bash
export JENKINS_USER=admin
export JENKINS_PASSWORD=admin
python3 job-launcher-0.1.0.pyz run -r job_launcher_config.yaml
```


### Docker image
#### Usage
```bash
export JENKINS_USER=admin
export JENKINS_PASSWORD=admin
mkdir -p output
docker run --rm -v `pwd`/job_launcher_config.yaml:/config.yaml -v `pwd`/output:/app/output -e JENKINS_USER=$JENKINS_USER -e JENKINS_PASSWORD=$JENKINS_PASSWORD job-launcher run -r /config.yaml
```