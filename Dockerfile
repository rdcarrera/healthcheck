# HEALTHCHECK
FROM alpine:latest

LABEL maintener "Ruben D. Carrera <@rdcarrera>" \
version "develop"


#ENV with the path of the config
ENV DOCKER_PATH="/healthcheck" \
DOCKER_USER="workuser" \
DOCKER_PORT="8080" \
PS1="[HEALTHCHECK] - \w \$ " \
TZ=Europe/Madrid

ENV DOCKER_CONFIG="${DOCKER_PATH}/examples/Healthcheck.yml"

#COPY Everything
COPY ./docker-entrypoint.sh /usr/bin/
COPY ./healthcheck ${DOCKER_PATH}/healthcheck
COPY ./modules/ ${DOCKER_PATH}/modules/
COPY ./examples/ ${DOCKER_PATH}/examples/

#Install the python
RUN apk add --update python3 && \
python3 -m pip install --upgrade pip && \
python3 -m pip install pipenv && \
mkdir -p ${DOCKER_PATH} && \
chmod 777 ${DOCKER_PATH} && \
adduser --system ${DOCKER_USER} && \
chmod 777 /usr/bin/docker-entrypoint.sh && \
chown -R ${DOCKER_USER} ${DOCKER_PATH}

#Expose the port 8080
#EXPOSE ${DOCKER_PORT}

#User apache user
USER ${DOCKER_USER}

#Move to the healthcheck
WORKDIR ${DOCKER_PATH}

#Install the dependency of the env
RUN python3 -m pipenv install termcolor PyYAML python-dateutil mysql-connector-python-rf

#Healthceck verification
#HEALTHCHECK --interval=5m --timeout=3s \
# CMD curl -f http://localhost:8080/ || exit 1

ENTRYPOINT [ "/usr/bin/docker-entrypoint.sh" ]

#Execute the apache2
CMD [ "healthcheck" ]
