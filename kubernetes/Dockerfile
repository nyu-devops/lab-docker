FROM python:3.6-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
