FROM python:2-alpine
EXPOSE 5000
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD python app.py

