set shell := ["bash", "-uc"]

image_registry := "ic-registry.epfl.ch"
image_name := "ic-it/restic"
tag := "latest"

build:
  #!/bin/bash

  docker build -t {{image_registry}}/{{image_name}}:{{tag}} .

run: build
  #!/bin/bash

  docker run \
    --rm \
    -it \
    -v /tmp:/data:ro \
    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    -e RESTIC_REPOSITORY=$RESTIC_REPOSITORY \
    -e RESTIC_PASSWORD=$RESTIC_PASSWORD \
    -e RESTIC_ACTION=$RESTIC_ACTION \
    {{image_registry}}/{{image_name}}:{{tag}}

push: build
  #!/bin/bash

  docker push {{image_registry}}/{{image_name}}:{{tag}}

helm-dry-run:
  #!/bin/bash

  helm upgrade restic-backup helm \
    --install --dry-run --namespace restic-backup \
    --set IC_REGISTRY_URL="ic-registry.epfl.ch" \
    --set IMAGE_REGISTRY_USERNAME=$IC_REGISTRY_USER \
    --set IMAGE_REGISTRY_PASSWORD=$IC_REGISTRY_PASSWORD \
    --set DOCKERCONFIGJSON=$DOCKERCONFIGJSON \
    --set AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    --set AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    --set RESTIC_REPOSITORY=$RESTIC_REPOSITORY \
    --set RESTIC_PASSWORD=$RESTIC_PASSWORD \
    --set RESTIC_ACTION=$RESTIC_ACTION \
    --set VOLUME.NAME=$VOLUME_NAME \
    --set VOLUME.SERVER=$VOLUME_SERVER \
    --set VOLUME.PATH=$VOLUME_PATH

helm-install:
  #!/bin/bash

  helm upgrade restic-backup helm \
    --install --create-namespace --namespace restic-backup \
    --set IC_REGISTRY_URL="ic-registry.epfl.ch" \
    --set IMAGE_REGISTRY_USERNAME=$IC_REGISTRY_USER \
    --set IMAGE_REGISTRY_PASSWORD=$IC_REGISTRY_PASSWORD \
    --set DOCKERCONFIGJSON=$DOCKERCONFIGJSON \
    --set AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    --set AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    --set RESTIC_REPOSITORY=$RESTIC_REPOSITORY \
    --set RESTIC_PASSWORD=$RESTIC_PASSWORD \
    --set RESTIC_ACTION=$RESTIC_ACTION \
    --set VOLUME.NAME=$VOLUME_NAME \
    --set VOLUME.SERVER=$VOLUME_SERVER \
    --set VOLUME.PATH=$VOLUME_PATH
