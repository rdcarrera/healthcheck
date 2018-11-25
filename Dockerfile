# HEALTHCHECK
#
# VERSION: develop

FROM alpine:latest
LABEL maintener "Ruben D. Carrera <@rdcarrera>"
LABEL version develop

#Install the python
RUN apk add --update python3 

#Update pip
RUN python3 -m pip install --upgrade pip

#Install pipenv
RUN python3 -m pip install pipenv

#Create the healthcheck
RUN mkdir /healthcheck

#ADD 777 perms to the healthcheck
RUN chmod 777 /healthcheck

#ADD work USER
RUN adduser --system workuser

#Expose the port 8080
#EXPOSE 8080

#User apache user
USER workuser

#Move to the healthcheck
WORKDIR /healthcheck

#Install the dependency of the env
RUN python3 -m pipenv install termcolor PyYAML python-dateutil

#COPY EVERYTHING
#COPY ./index.html /healthcheck/index.html
COPY ./healthcheck /healthcheck/healthcheck
COPY ./modules/ /healthcheck/modules/
COPY ./templates/ /healthcheck/templates/

#Healthceck verification
#HEALTHCHECK --interval=5m --timeout=3s \
# CMD curl -f http://localhost:8080/ || exit 1

#ENV with the path of the config
ENV CONFIG_PATH /healthcheck/templates/Healthcheck.yml

#Execute the apache2
CMD python3 -m pipenv run python /healthcheck/healthcheck -c  $CONFIG_PATH
