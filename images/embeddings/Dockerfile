FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src /app/
CMD ["python", "resume_chatbot/main.py"]
