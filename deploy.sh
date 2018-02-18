source env/bin/activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
sudo env/bin/python manage.py collectstatic --noinput

sudo service memcached restart
sudo service apache2 restart
