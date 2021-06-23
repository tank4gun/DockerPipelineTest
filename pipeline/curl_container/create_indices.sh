#!/bin/sh
curl -X PUT "http://elasticsearch:9200/logstash_app_log?pretty" -H 'Content-Type: application/json' -d @fluentd/logstash_app_log.json
curl -X PUT "http://elasticsearch:9200/logstash_train_log?pretty" -H 'Content-Type: application/json' -d @fluentd/logstash_train_log.json
curl -X POST "http://kibana:5601/api/saved_objects/_import" -H "kbn-xsrf: true" --form file=@kibana_settings.ndjson
