FROM python:3.12-slim

#set directory
WORKDIR /usr/src/app

#copy requirements
COPY ./requirements.txt /usr/src/app/requirements.txt

#install requirements
RUN pip install --no-cache-dir -r requirements.txt

#copy the code
COPY . /usr/src/app

RUN adduser --disabled-password appuser
USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


