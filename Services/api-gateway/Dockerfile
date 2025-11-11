FROM python:3.12-slim

#set directory
WORKDIR /usr/src/app

COPY requirements.txt .
#COPY ./requirements.txt /usr/src/app/requirements.txt

#install requirements
RUN pip install --no-cache-dir -r requirements.txt

#copy the code
COPY . .
COPY ./.env /usr/src/app/.env
#ENV PYTHONPATH=/usr/src/app

#RUN adduser --disabled-password appuser
#USER appuser

#CMD["cd Services/api-gateway"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["cd Services/api-gateway", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

