FROM rabbitmq:latest

ENV RABBITMQ_PID_FILE /var/lib/rabbitmq/mnesia/rabbitmq
COPY ./init.sh /usr/local/bin/
RUN rabbitmq-plugins enable --offline rabbitmq_management
CMD ['/usr/local/bin/init.sh']