build:
	@echo "***build"
	docker build --rm -f docker/Dockerfile --tag debian-base docker/
	docker build --rm -f docker/router/Dockerfile --tag debian-router docker/router/
	docker build --rm -f docker/jump/Dockerfile --tag debian-jump docker/jump/
	docker build --rm -f docker/broker/Dockerfile --tag debian-broker docker/broker/
	docker build --rm -f docker/auth/Dockerfile --tag debian-auth docker/auth/
	docker build --rm -f docker/files/Dockerfile --tag debian-files docker/files/
	docker build --rm -f docker/work/Dockerfile --tag debian-work docker/work/
	docker build --rm -f docker/logs/Dockerfile --tag debian-logs docker/logs/

network:
	@echo "***network"
	-docker network create -d bridge --subnet 10.0.1.0/24 dmz
	-docker network create -d bridge --subnet 10.0.2.0/24 srv
	-docker network create -d bridge --subnet 10.0.3.0/24 dev

containers: network
	@echo "***containers"
	docker run --privileged -ti -d --name router --hostname router debian-router
	docker network connect dmz router
	docker network connect srv router
	docker network connect dev router
	
	docker run --privileged -ti -d --name jump --hostname jump \
		--network dmz --ip 10.0.1.3 debian-jump
	docker run --privileged -ti -d --name broker --hostname broker \
		--network dmz --ip 10.0.1.4 debian-broker \
		--add-host=jump:10.0.1.3 \
		--add-host=auth:10.0.2.3 \
		--add-host=files:10.0.2.4 \
		--add-host=work:10.0.3.3 \
		--add-host=logs:10.0.3.4
	docker run --privileged -ti -d --name auth --hostname auth \
		--network srv --ip 10.0.2.3 debian-auth \
		--add-host=broker:10.0.1.4 \
		--add-host=jump:10.0.1.3 \
		--add-host=files:10.0.2.4 \
		--add-host=work:10.0.3.3 \
		--add-host=logs:10.0.3.4
	docker run --privileged -ti -d --name files --hostname files \
		--network srv --ip 10.0.2.4 debian-files \
		--add-host=broker:10.0.1.4 \
		--add-host=jump:10.0.1.3 \
		--add-host=auth:10.0.2.3 \
		--add-host=work:10.0.3.3 \
		--add-host=logs:10.0.3.4
	docker run --privileged -ti -d --name work --hostname work \
		--network dev --ip 10.0.3.3 debian-work
	docker run --privileged -ti -d --name logs --hostname logs \
		--network dev --ip 10.0.3.4 debian-logs

run-tests:
	@echo "tests"

remove:
	@echo "***remove"
	-docker stop router jump broker auth files work logs
	docker network prune -f
	docker rm -f router jump broker auth files work logs

clean:
	find . -name "*~" -delete
