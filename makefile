#
# Title:makefile
#
# Description:
#   'make clean' removes all core and object files
#   'make ultraclean' removes all executables
#
# Operating System/Environment:
#   Ubuntu 18.04.3 LTS (Bionic Beaver)
#   GNU Make 4.1
#
# Author:
#   G.S. Cole (guycole at gmail dot com)
#
AFPLAY = afplay
DOCKER = docker
MELLOW_BULLSEYE = mellow-bullseye:1
KUBECTL = kubectl
MINIKUBE = minikube

be_build:
	cd chupacabra; $(DOCKER) build . -t $(DARING_CHUPACABRA)

be_delete:
	$(KUBECTL) delete -f infra/be-deploy.yaml

be_deploy:
	$(KUBECTL) apply -f infra/be-deploy.yaml

fe_build:
	cd chupacabra; $(DOCKER) build . -t $(DARING_CHUPACABRA)

fe_delete:
	$(KUBECTL) delete -f infra/fe-deploy.yaml -n chupacabra

fe_deploy:
	$(KUBECTL) apply -f infra/fe-deploy.yaml -n chupacabra

minikube_reset:
	$(MINIKUBE) stop
	$(MINIKUBE) delete

minikube_start:
	cd infra; ./start-minikube.sh
	eval $(minikube docker-env)

minikube_setup:
	$(KUBECTL) apply -f infra/namespace.yaml
	$(MINIKUBE) addons enable ingress

test:
	. venv/bin/activate && pytest
	$(AFPLAY) /System/Library/Sounds/Submarine.aiff

#	$(AFPLAY) /System/Library/Sounds/Glass.aiff
	