FROM ubuntu:latest
EXPOSE 80
USER root
RUN apt-get update 
RUN apt-get -y install python3-pip python3-dev
WORKDIR /app
COPY ./ /app
RUN chmod +x /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
RUN python3 -m spacy download es_core_news_sm
COPY ./openapi.json /openapi.json
CMD ["python3","app.py"] 