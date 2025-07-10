FROM python:3.9.13

WORKDIR /app

COPY . .

RUN pip install -r requirments.txt

CMD ["python", "main.py"]