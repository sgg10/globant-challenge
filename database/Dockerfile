FROM liquibase/liquibase

USER root

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY set-db.sh /docker-entrypoint-initdb.d/set-db.sh

RUN chmod +x /docker-entrypoint-initdb.d/set-db.sh

COPY . /liquibase/changelog

ENTRYPOINT ["/docker-entrypoint-initdb.d/set-db.sh"]