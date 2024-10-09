FROM python:3.12-alpine

WORKDIR /api

COPY . .

RUN python3.12 -m venv ./venv 
RUN source ./venv/bin/activate
RUN pip install -r ./requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000"]