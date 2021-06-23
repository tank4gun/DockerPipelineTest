# syntax=docker/dockerfile:1

FROM python:3.7
USER root 
WORKDIR .
ENV FLASK_APP=create_app.py
ENV TD_AGENT_HOST=td-agent
# EXPOSE 5100
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
COPY templates/ /templates/

#CMD ["sleep", "10000"]
CMD [ "python3", "create_app.py"]

