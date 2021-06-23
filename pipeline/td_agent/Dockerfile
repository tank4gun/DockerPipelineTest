FROM fluent/fluentd:v1.12.1-1.0 
USER root
COPY ./td-agent.conf /fluentd/etc/
RUN gem install fluent-plugin-elasticsearch
