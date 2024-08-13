#!/bin/sh
exec contribution run-event-consumer "$@" 1>> /var/log/contribution/event-consumer.log
