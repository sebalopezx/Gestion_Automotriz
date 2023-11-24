pip install virtualenv
python3 -m virtualenv venv

call .\venv\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata data.json 

cmd