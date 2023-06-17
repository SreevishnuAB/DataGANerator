FROM python:3.9-bullseye

USER root

RUN groupadd -g 20 appgroup && useradd -D -u 501 appgroup appuser

USER appuser

WORKDIR /worker

COPY --chown=appuser:appgroup . ./

VOLUME [ "/worker/logs", "/worker/files" ]

RUN chown -R appuser:appgroup ./* && \
    pip install -r requirements.txt

CMD ["python", "worker.py"]