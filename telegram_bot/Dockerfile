FROM python:3.12

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt


WORKDIR /app/bot
COPY /bot/ .

CMD ["python", "main.py"]