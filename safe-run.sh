ru
docker-compose up
# INIT
# docker-compose -f create-certs.yml run --rm create_certs
# docker-compose up -d gleaky-index-01 gleaky-index-02
# docker exec es01 /bin/bash -c "bin/elasticsearch-setup-passwords auto --batch --url https://localhost:9200"
# or
# docker run --rm -v es_certs:/certs --network=es_default docker.elastic.co/elasticsearch/elasticsearch:7.6.2 curl --cacert /certs/ca/ca.crt -u elastic:PleaseChangeMe https://gleaky-index-01:9200

# TEARDOWN EVERYTHING
# docker-compose down -v
