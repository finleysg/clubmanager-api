#!/usr/bin/env bash

FILE=bhmc.sql.`date + "%Y%m%d"`

mysqldump -u finleysg -h finleysg.mysql.pythonanywhere-services.com 'finleysg$bhmc' > ${FILE}

gzip ${FILE}

echo "${FILE}.gz created:"
ls -l ${FILE}.gz
