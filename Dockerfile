FROM python:3.11-slim

RUN mkdir /booking

WORKDIR /booking

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod a+x /booking/docker/*.sh

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]