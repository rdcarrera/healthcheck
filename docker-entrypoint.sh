#!/bin/sh
if [ $# == 0 ];then
    exec /bin/bash
else
    if [ $1 == "healthcheck" ];then
        if [ ${DOCKER_CONFIG} == "/healthcheck/examples/Healthcheck.yml" ];then
            if env | grep DB_ 2> /dev/null > /dev/null;then
                sed -i "s/#//g" ${DOCKER_CONFIG}
                for _iterator in `env |grep DB_`;do 
                    _tmpVarName=`echo ${_iterator} |awk -F= '{ print $1 }'`
                    _tmpVarValue=`echo ${_iterator} |awk -F= '{ print $2 }'`
                    sed -i "s/${_tmpVarName}/${_tmpVarValue}/g" `dirname ${DOCKER_CONFIG}`/LocalMysql.yml
                done
            fi
        fi
        python3 -m pipenv run python -u /healthcheck/healthcheck -c  $DOCKER_CONFIG
    else
        exec $@
    fi
fi
exit $?