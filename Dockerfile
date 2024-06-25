FROM python:3.8.12-slim-buster


WORKDIR /prod

COPY requirements.txt requirements.txt

COPY project_waste project_waste
COPY setup.py setup.py
COPY model model
RUN pip install --upgrade pip
RUN pip install .
#RUN apt-get update && apt-get install -y libtbb2 libtbb-dev



COPY Makefile Makefile

EXPOSE 80


CMD uvicorn project_waste.api.fast:app --host 0.0.0.0 --port 80
