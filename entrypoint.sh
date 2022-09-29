#!/bin/bash

# SIGTERM-handler
term_handler() {
  service cron stop
  exit 0
}


if [ ! -f /data/crontab ]; then
  randomMinute=$(( ( RANDOM % 60 ) + 1 ))
  echo -e "$randomMinute */2 * * * /workingdir/crawl.py -c /data/myHisConfig.cfg\n" > /data/crontab
  chmod 777 /data/crontab
else
  crontab /data/crontab
fi

chmod +x /workingdir/crawl.py

if [ ! -f /data/myHisConfig.cfg ]; then
  /workingdir/crawl.py -c /data/myHisConfig.cfg
  chmod 777 /data/myHisConfig.cfg
  echo "Konfigurationsdatei in /data/myHisConfig.cfg wurde erstellt"
  exit 0
else
  /workingdir/crawl.py -c /data/myHisConfig.cfg
fi

service cron start


trap 'kill ${!}; term_handler' INT
trap 'kill ${!}; term_handler' SIGTERM

# wait forever
while true
do
    tail -f /dev/null & wait ${!}
done
