FROM gocd/gocd-agent-ubuntu-18.04:v20.10.0
EXPOSE 5100
USER root
ENV TD_AGENT_HOST=td-agent
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends python3.7 wget
RUN apt-get install python-pip -y && pip install -r requirements.txt
RUN wget https://dvc.org/deb/dvc.list -O /etc/apt/sources.list.d/dvc.list
RUN wget -qO - https://dvc.org/deb/iterative.asc | apt-key add -
RUN apt-get update
RUN apt-get install dvc
