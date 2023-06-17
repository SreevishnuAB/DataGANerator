FROM python:3.9-bullseye

USER root

RUN groupadd -g 20 appgroup && useradd -D -u 501 appgroup appuser

USER appuser

WORKDIR /api

COPY --chown=appuser:appgroup . ./

VOLUME [ "/api/files" ]

RUN chown -R appuser:appgroup ./* && \
    pip install -r requirements.txt

CMD ["flask", "--app", "app", "run"]