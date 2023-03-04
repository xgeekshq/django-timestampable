requirements: requirements.txt
	python3 -m venv .venv
	./.venv/bin/pip install -r requirements.txt

clean:
	find . -type f -name '*.pyc' -delete
	rm -rf .venv

test:
	./.venv/bin/python manage.py test tests

coverage:
	./.venv/bin/coverage run --source='timestamps' manage.py test tests
	./.venv/bin/coverage report -m

show-urls:
	./.venv/bin/python manage.py show_urls

run: clean requirements test

build: run
	./.venv/bin/python setup.py sdist

pypi: build
	./.venv/bin/python -m twine upload dist/* --config-file ~/.pypirc

test-pypi: build
	./.venv/bin/python -m twine upload --repository testpypi dist/* --config-file ~/.pypirc
