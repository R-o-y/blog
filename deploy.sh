# assume in python virtual environment

python manage.py makemigrations
python manage.py migrate
sudo env/bin/python manage.py collectstatic

sudo service memcached restart
sudo service apache2 restart
