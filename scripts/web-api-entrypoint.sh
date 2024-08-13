#!/bin/sh
exec contribution run-web-api "$@" 1>> /var/log/contribution/web-api.log
