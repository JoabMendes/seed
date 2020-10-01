dev-setup:
	python setup.py develop
	pip install flake8
	pip install .
	pip install pytest coveralls collective.dist
	pip install --pre `python -c "import sys; print('coverage>4.0a1' if sys.version_info > (3,3) else 'coverage<4')"`
	touch .nocleanup

ci-setup:
	python setup.py develop
	pip install flake8
	pip install .
	pip install pytest coveralls collective.dist
	pip install --pre `python -c "import sys; print('coverage>4.0a1' if sys.version_info > (3,3) else 'coverage<4')"`
	git config --global user.email 'user@test.com'
	git config --global user.name 'Test User'
	echo "[server-login]\nusername:testuser\npassword:testpass" > ~/.pypirc
	touch .nocleanup

test-coverage:
	coverage run -p --source=seed --omit=docs/*,seed/vcs/*,*__init__.py runtests.py

test-style:
	flake8 seed seed_tests --exclude=*/docs

test: test-coverage test-style

clean:
	rm .coverage*
