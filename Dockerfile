FROM python:3.10
RUN addgroup --gid 1001 --system dash &&                 adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group dash
WORKDIR /app
COPY /src/app.py ./app.py
COPY /requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
USER dash
COPY --chown=dash:dash . ./
CMD gunicorn -b 0.0.0.0:80 src.app:server
