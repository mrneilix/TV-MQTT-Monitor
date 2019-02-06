#!/bin/bash
ping -c 1 TELEVISION_IP_ADDRESS>/dev/null
STATUS=$?
if [ $STATUS -ne 0 ]; then
  echo "OFF"
else
  echo "ON"
fi
