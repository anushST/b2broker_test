FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /project

COPY ./requirements.txt /project/requirements.txt
RUN pip install --no-cache-dir -r /project/requirements.txt

COPY . /project/
RUN chmod +x /project/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
