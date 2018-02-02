sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get -y install build-essential libpq-dev python-dev
sudo apt-get -y install postgresql postgresql-contrib
sudo apt-get -y install python-virtualenv

psql -c 'create database lcp_db;' -U postgres
#sudo su - postgres
#createuser {% db_user %}
#createdb {% db_name %} --owner {% db_user %}
#psql -c "ALTER USER {% db_user %} WITH PASSWORD '{% db_password %}'"

#exit

cd /code
virtualenv myvenv --always-copy
source myvenv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py collectstatic

