run:
	python main.py

install:
	pip install -r requirements.tx

test:
	PYTHONPATH=. pytest tests