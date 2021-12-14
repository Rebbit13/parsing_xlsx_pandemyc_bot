FROM python:3.9.1

COPY . /app
RUN make /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "bot.py"]
