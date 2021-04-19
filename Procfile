% prepara el repositorio para su despliegue. 
release: sh -c 'python manage.py migrate'
% especifica el comando para lanzar Groomeet
web: sh -c 'cd groomeet && daphne groomeet.asgi:application --port $PORT --bind 0.0.0.0'
