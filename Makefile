.PHONY: install test deploy docs clean

install:
	pip install -e .

test:
	pytest -v --cov=albumbot tests/

deploy:
	./deploy/pack_function.sh
	cd deploy/terraform && terraform apply -auto-approve

docs:
	cd docs && ${MAKE} html

clean:
	rm -rf build dist *.egg-info
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete