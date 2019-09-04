codestyle:
	pycodestyle setup.py
	pycodestyle pysigsci/__init__.py
	pycodestyle pysigsci/sigsciapi/__init__.py
	pycodestyle pysigsci/sigsciapi/sigsciapi.py
	pycodestyle pysigsci/powerrules/__init__.py
	pycodestyle pysigsci/powerrules/powerrules.py
	pycodestyle pysigsci/releases/__init__.py
	pycodestyle pysigsci/releases/releases.py
	pycodestyle pysigsci/bin/pysigsci
	pycodestyle pysigsci/bin/pysigscia
	pycodestyle example.py

fix-codestyle:
	autopep8 --in-place --aggressive setup.py
	autopep8 --in-place --aggressive pysigsci/__init__.py
	autopep8 --in-place --aggressive pysigsci/sigsciapi/__init__.py
	autopep8 --in-place --aggressive pysigsci/sigsciapi/sigsciapi.py
	autopep8 --in-place --aggressive pysigsci/powerrules/__init__.py
	autopep8 --in-place --aggressive pysigsci/powerrules/powerrules.py
	autopep8 --in-place --aggressive pysigsci/releases/__init__.py
	autopep8 --in-place --aggressive pysigsci/releases/releases.py
	autopep8 --in-place --aggressive pysigsci/bin/pysigsci
	autopep8 --in-place --aggressive pysigsci/bin/pysigscia
	autopep8 --in-place --aggressive example.py

lint:
	pylint pysigsci/__init__.py
	pylint pysigsci/sigsciapi/__init__.py
	pylint pysigsci/sigsciapi/sigsciapi.py
	pylint pysigsci/powerrules/__init__.py
	pylint pysigsci/powerrules/powerrules.py
	pylint pysigsci/releases/__init__.py
	pylint pysigsci/releases/releases.py
	pylint pysigsci/bin/pysigsci
	pylint pysigsci/bin/pysigscia
	pylint example_with_api_token.py
	pylint example_without_api_token.py

env:
	virtualenv .env
	. .env/bin/activate \
	&& pip install --upgrade pip \
	&& pip install --upgrade setuptools \
	&& pip install --upgrade -r requirements.txt

update_env:
	# FOR DEVELOPMENT ONLY
	cp pysigsci/bin/pysigsci .env/bin/pysigsci
	cp pysigsci/sigsciapi/sigsciapi.py .env/lib/python2.7/site-packages/pysigsci/sigsciapi/
	cp pysigsci/releases/__init__.py .env/lib/python2.7/site-packages/pysigsci/releases/
	cp pysigsci/releases/releases.py .env/lib/python2.7/site-packages/pysigsci/releases/

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