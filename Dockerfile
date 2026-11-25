FROM python:3.12-slim
WORKDIR /app
COPY app.py gym-rules.md ./
ENV PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["python", "app.py"]
