#!/bin/bash

pcks="django dj_database_url gunicorn psycopg2-binary Pillow mutagen"

for p in $pcks
do
   echo "installing $p"
   pip3 install $p
done

echo "creating requirements"
pip3 freeze --local > requirements.txt
