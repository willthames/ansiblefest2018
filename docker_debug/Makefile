all: blue green

blue green:
	echo '.header { background-color: $@; }' > static/colour.css
	docker build -t docker_debug:$@ .
