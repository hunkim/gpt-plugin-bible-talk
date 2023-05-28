VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3
UVICORN = $(VENV)/bin/uvicorn

# Need to use python 3.9 for aws lambda
$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

run: $(VENV)/bin/activate
	$(UVICORN) main:app --reload --port 10004

bible: $(VENV)/bin/activate
	$(PYTHON) bible_search.py

clean:
	rm -rf __pycache__
	rm -rf $(VENV)

