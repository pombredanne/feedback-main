FROM python:3.7

ENV PYTHONUNBUFFERED 1
WORKDIR /opt/api

COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt

COPY ./utils/nltk_downloader.py /opt/api/utils/nltk_downloader.py
RUN PYTHONPATH=/opt/api python -c "import utils.nltk_downloader"

EXPOSE 5000
