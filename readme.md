to run minio server you can use 'docker-compose up' or directly run below command

./minio server ./data --address 'localhost:9006' --console-address "localhost:9005"


to reset docker database run these commands:
docker-compose up -d db
docker-compose exec db bash
psql -U postgres
DROP DATABASE "negare-database";
CREATE DATABASE "negare-database";

to create superuser in docker:
docker-compose up -d web
docker-compose exec web bash
cd negare
python manage.py createsuperuser