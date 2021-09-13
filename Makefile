.PHONY: black
black:	## blackify code
	black .

.PHONY: test
test:  ## run tests quickly with the default Python
	py.test -vv

.PHONY: test-coverage
test-coverage:  ## check code coverage
	coverage run -m pytest
	coverage report -m
	coverage xml -o coverage-reports/report.xml
