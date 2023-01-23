format:
	isort app --profile 'black'
	black app

lint:
	mypy --disallow-untyped-defs --ignore-missing-imports app
	black app --check
	isort app --profile 'black' --check
	flake8 app

