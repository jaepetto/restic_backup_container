# Restic backup container

This container is used to backup data to an S3 repository using [restic](https://github.com/restic/restic).

## development

this container is running a python script that will check that the parameters are OK and will launch restic. The script is located in the `src` folder.

The current version has been made with python 3.11.1. You can install the dependencies with `pip install -r requirements.txt`.
The dependencies are managed through [pip-tools](https://github.com/jazzband/pip-tools) in order to keep the `requirements.txt` file nice and tidy.

## build

The build / push is done through a [justfile](https://github.com/casey/just). You can build the container with `just build` and push it with `just push`.

## deployment

A Helm chart is also provided in the `helm` folder. You can deploy it with `just helm-install`.

However, the deployment expects a number of environment variables to be set:
| Variable | Description | optional | example |
| -------- | ----------- | -------- | ------- |
| AWS_ACCESS_KEY_ID | AWS access key ID | no | |
| AWS_SECRET_ACCESS_KEY | AWS secret access key | no | |
| RESTIC_REPOSITORY | restic repository | no | `s3:s3.epfl.ch/my-bucket` |
| RESTIC_PASSWORD | restic password | no | |
| RESTIC_ACTION | restic action to perform. Should be within the list: help, init, backup, check, ls, forget, prune | no | `backup` |
| IC_REGISTRY_URL | URL of the container registry | no | `ic-registry.epfl.ch` |
| IC_REGISTRY_PATH | Path of the container registry | no | `$IC_REGISTRY_URL/ic-it/restic:latest` |
| IC_REGISTRY_USER | Username to access the container registry | no | `robot$...` |
| IC_REGISTRY_PASSWORD | Password to access the container registry | no | |
| DOCKERCONFIGJSON | base64 encoded docker config.json file | no | `$(kubectl create secret docker-registry ic-registry-secret --namespace=restic-backup --docker-server=$IC_REGISTRY_URL --docker-username=$IC_REGISTRY_USER --docker-password=$IC_REGISTRY_PASSWORD -o json --dry-run=client \| jq -r '.data\|.[".dockerconfigjson"]') ` |
| VOLUME_NAME | Name of the volume to backup | no | |
| VOLUME_SERVER | Server of the volume to backup | no | `nasXXX.iccluster.epfl.ch` |
| VOLUME_PATH | Path of the volume to backup | no | `nasXXX/...` |
