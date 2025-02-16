build:
	rm -rf dist/*
	uv build
publish:
	uv publish