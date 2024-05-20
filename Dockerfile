FROM python:3.9-slim

WORKDIR /app

RUN pip3 install fastapi uvicorn
RUN pip3 install pydantic mysql-connector-python

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
