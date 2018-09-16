all: blue green

blue green:
	echo 'colour = "$@"' > colour.py
	docker build -t willthames/docker_debug:$@ .
	docker push willthames/docker_debug:$@
