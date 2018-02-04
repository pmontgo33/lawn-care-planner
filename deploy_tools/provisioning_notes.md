=======================
Provisioning a new site
=======================

## Required packages:

* PostgreSQL:
    * build-essential, libpq-dev, python-dev
    * postgresql, postgresql-contrib
* nginx
* supervisor
* Python 3.5.2
* virtualenv + pip
* Git

On Ubuntu

Install Packages:

    sudo apt-get update
    sudo apt-get -y upgrade

    PostgreSQL:

        sudo apt-get -y install build-essential libpq-dev python-dev
        sudo apt-get -y install postgresql postgresql-contrib

    NGINX:

        sudo apt-get -y install nginx

    Supervisor:

        sudo apt-get -y install supervisor

        sudo systemctl enable supervisor
        sudo systemctl start supervisor

    Python Virtualenv

        sudo apt-get -y install python-virtualenv


Configure PostgreSQL:

    su - postgres

    createuser {% db_user %}
    createdb {% db_name %} --owner {% db_user %}
    psql -c "ALTER USER {% db_user %} WITH PASSWORD '{% db_password %}'"

    exit


Configure Application User:

    adduser lcp
    gpasswd -a lcp sudo
    su - lcp

Configure the Python Virtualenv:

    virtualenv -p python3 .
    source bin/activate

    git clone https://github.com/pmontgo33/lawn-care-planner.git


Current file structure:

    lcp/
     |-- bin/
     |-- lawn-care-planner/  <-- Django App (Git Repository)
     |-- include/
     |-- lib/
     |-- local/
     |-- pip-selfcheck.json
     +-- share/

 Install Project Requirements:

    cd lawn-care-planner
    pip install -r requirements.txt

    python manage.py migrate
    python manage.py collectstatic


Configure Gunicorn:

    sudo nano bin/gunicorn_start

    ** paste text from file guicorn_start **

    chmod u+x bin/gunicorn_start

    mkdir run

Configure Supervisor:

    mkdir logs
    touch logs/gunicorn-error.log

    sudo nano /etc/supervisor/conf.d/lawn-care-planner.conf

    *** paste text from file lawn-care-planner.conf ***

    sudo supervisorctl reread
    sudo supervisorctl update

    sudo supervisorctl status lawn-care-planner
    *** should say lawn-care-planner RUNNING ***

Configure NGINX:

    sudo nano /etc/nginx/sites-available/lawn-care-planner

    *** paste text from file lawn-care-planner ***

    sudo ln -s /etc/nginx/sites-available/lawn-care-planner /etc/nginx/sites-enabled/lawn-care-planner
    sudo rm /etc/nginx/sites-enabled/default
    sudo service nginx restart

    sudo reboot


Update to New Version:

    ssh lcp@ip.address

    source bin/activate
    cd lawn-care-planner
    git pull origin master
    python manage.py collectstatic
    python manage.py migrate
    sudo supervisorctl restart lawn-care-planner
    exit