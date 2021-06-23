FROM curlimages/curl:7.77.0
USER root
COPY ./logstash* /fluentd/
COPY ./kibana_settings.ndjson /kibana_settings.ndjson
COPY ./create_indices.sh /fluentd/
RUN chmod 777 /fluentd/create_indices.sh
