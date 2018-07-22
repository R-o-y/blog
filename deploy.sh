source env/bin/activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
sudo env/bin/python manage.py collectstatic --noinput

touch royl8/wsgi.py