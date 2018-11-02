# HEALTHCHECK
#
# VERSION: develop

FROM alpine:latest
LABEL maintener "Ruben D. Carrera <@rdcarrera>"
LABEL version develop

#Install the python
RUN apk add --update python curl py-yaml py-dateutil

#Create the workdir
RUN mkdir /workdir

#ADD 777 perms to the workdir
RUN chmod 777 /workdir

#ADD work USER
RUN adduser --system --no-create-home workuser

#Expose the port 8080
EXPOSE 8080

#User apache user
USER workuser

#Move to the workdir
WORKDIR /workdir

#COPY index
COPY ./index.html /workdir/index.html

#Healthceck verification
HEALTHCHECK --interval=5m --timeout=3s \
 CMD curl -f http://localhost:8080/ || exit 1

#Execute the apache2
CMD ["/usr/bin/python", "-m" , "SimpleHTTPServer",  "8080"]
