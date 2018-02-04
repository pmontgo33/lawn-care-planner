#!/bin/bash

echo "Provisioning virtual machine..."

echo "Installing necessary packages..."
sudo apt-get update
sudo apt-get -y install python3-pip
sudo apt-get -y install build-essential libpq-dev python-dev
sudo apt-get -y install postgresql postgresql-contrib
sudo apt-get -y install python-virtualenv

echo "Installing Firefox and geckodriver for testing..."
sudo apt-get -y install firefox
wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/

echo "Installing xvfb for headless testing..."
sudo apt-get -y install xvfb
Xvfb :1 -screen 0 1600x1200x16 &
echo "export DISPLAY=:1" >> /home/vagrant/.bashrc

echo "Creating database..."
sudo -u postgres psql -c "CREATE USER u_vagrant WITH PASSWORD 'password';"
sudo su - postgres -c "createdb vagrant_db --owner u_vagrant"
sudo -u postgres psql -c "ALTER USER u_vagrant CREATEDB;"

echo "Creating virtual environment"
virtualenv -p python3 myvenv --always-copy

echo "Activating virtual environment and installing project dependencies..."
source myvenv/bin/activate
cd app
pip install -r requirements.txt

echo "Migrating database and collecting static files..."
python manage.py migrate
python manage.py collectstatic --noinput

echo "Loading initial database data from fixtures"
python manage.py loaddata planner/fixtures/*.json