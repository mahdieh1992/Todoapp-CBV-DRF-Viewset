FROM python:3.10.9
ENV PYTHONWRITEBYTECODE 1
ENV PYTHONUNBUFFRED 1
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./ code
CMD ['python','manage.py','runserver','0.0.0.0:8000']



