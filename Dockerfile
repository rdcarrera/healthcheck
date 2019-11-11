# HEALTHCHECK
ARG IMAGE_REPOSITORY=registry.hub.docker.com/library
ARG IMAGE_NAME=alpine
ARG IMAGE_VERSION=latest
FROM ${IMAGE_REPOSITORY}/${IMAGE_NAME}:${IMAGE_VERSION}

LABEL maintener "Ruben D. Carrera <@rdcarrera>" \
      version "develop"


#ENV with the path of the config
ENV WORKDIR_PATH="/healthcheck" \
    BANNER="HealthCheck" \
    DOCKER_USER="workuser" \
    DOCKER_PORT="8080" \
    TZ=Europe/Madrid

ENV DOCKER_CONFIG="${WORKDIR_PATH}/examples/Healthcheck.yml"
ENV PS1="[${BANNER}] - \w \$ "

#COPY Everything
ADD ./bin/* /usr/bin/
COPY ./healthcheck ${WORKDIR_PATH}/

#Install the python
RUN apk add --update python3 \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install pipenv \
    && mkdir -p ${WORKDIR_PATH} \
    && chmod +x /usr/bin/docker-* \
    && chmod +x /usr/bin/healthcheck-* \
    && chmod 777 ${WORKDIR_PATH} \
    && adduser --system ${DOCKER_USER} \
    && chown -R ${DOCKER_USER} ${WORKDIR_PATH}

#Healthceck verification

#Expose the port 8080
#EXPOSE ${DOCKER_PORT}

#User apache user
USER ${DOCKER_USER}

#Move to the healthcheck
WORKDIR ${WORKDIR_PATH}

#Install the dependency of the env
RUN python3 -m pipenv install -r ${WORKDIR_PATH}/requirements.txt \
    && /usr/bin/healthcheck-requirements

#Healthceck verification
#HEALTHCHECK --interval=5m --timeout=3s \
# CMD curl -f http://localhost:8080/ || exit 1

ENTRYPOINT [ "/usr/bin/docker-entrypoint" ]

#Execute the apache2
CMD [ "healthcheck" ]
