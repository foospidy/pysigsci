codestyle:
	pycodestyle setup.py
	pycodestyle pysigsci/__init__.py
	pycodestyle pysigsci/sigsciapi/__init__.py
	pycodestyle pysigsci/sigsciapi/sigsciapi.py
	pycodestyle pysigsci/bin/pysigsci
	pycodestyle pysigsci/bin/pysigscia
	pycodestyle example.py

fix-codestyle:
	autopep8 --in-place --aggressive setup.py
	autopep8 --in-place --aggressive pysigsci/__init__.py
	autopep8 --in-place --aggressive pysigsci/sigsciapi/__init__.py
	autopep8 --in-place --aggressive pysigsci/sigsciapi/sigsciapi.py
	autopep8 --in-place --aggressive pysigsci/bin/pysigsci
	autopep8 --in-place --aggressive pysigsci/bin/pysigscia
	autopep8 --in-place --aggressive example.py

lint:
	pylint pysigsci/__init__.py
	pylint pysigsci/sigsciapi/__init__.py
	pylint pysigsci/sigsciapi/sigsciapi.py
	pylint pysigsci/bin/pysigsci
	pylint pysigsci/bin/pysigscia
	pylint example.py

env:
	virtualenv .env
	. .env/bin/activate \
	&& pip install --upgrade pip \
	&& pip install --upgrade setuptools \
	&& pip install --upgrade -r requirements.txt

install:
	pip install -r requirements.txt

wheel:
	python setup.py bdist_wheel --universal

publish:
	twine upload --skip-existing dist/*

clean:
	find . -name "*.pyc" -type f -delete
	rm -rf dist
	rm -rf build