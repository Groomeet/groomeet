% prepara el repositorio para su despliegue. 
release: sh -c 'python manage.py migrate'
% especifica el comando para lanzar Groomeet
web: sh -c 'cd groomeet && gunicorn groomeet.wsgi --log-file -'