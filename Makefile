build:
	docker build --rm -f Dockerfile --tag p4-image .
	docker network create -d bridge --subnet 10.0.1.0/24 dmz
	docker network create -d bridge --subnet 10.0.2.0/24 srv
	docker network create -d bridge --subnet 10.0.3.0/24 dev

containers:
	docker run -ti -d --name router --hostname router p4-image
	docker network connect dmz router
	docker network connect srv router
	docker network connect dev router

	docker run -ti -d --name jump --hostname jump --ip 10.0.1.3 \
		--network dmz p4-image
	docker run -ti -d --name broker --hostname broker --ip 10.0.1.4 \
		--network dmz p4-image
	
	docker run -ti -d --name auth --hostname auth --ip 10.0.2.3 \
		--network srv p4-image
	docker run -ti -d --name files --hostname files --ip 10.0.2.4 \
		--network srv p4-image
	
	docker run -ti -d --name work --hostname work --ip 10.0.3.3 \
		--network dev p4-image

remove:
	docker stop router jump broker auth files work 
	docker rm router jump broker auth files work
	docker network rm dmz srv dev

run-tests:
	echo "Testing.."
