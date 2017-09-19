FROM python:3.5

WORKDIR /usr/src/habr-proxy-test

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8080", "server:app"]