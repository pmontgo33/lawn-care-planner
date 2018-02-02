#!/bin/bash

echo "Provisioning virtual machine..."

echo "Installing necessary packages..."
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get -y install build-essential libpq-dev python-dev
sudo apt-get -y install postgresql postgresql-contrib
sudo apt-get -y install python-virtualenv

echo "Creating database..."
psql -c 'create database lcp_db;' -U postgres

echo "Creating virtual environment"
cd /code
virtualenv myvenv --always-copy

echo "Activating virtual environment and installing project dependencies..."
source myvenv/bin/activate
pip install -r requirements.txt

echo "Migrating database and collecting static files..."
python manage.py migrate
python manage.py collectstatic