FROM python:3.11-slim-buster

ENV OPENAI_API_KEY=""
ENV TELEGRAM_TOKEN=""

RUN apt-get update && apt-get install build-essential -y
# ENV LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1

WORKDIR /app
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python"]
CMD ["bot.py"]
