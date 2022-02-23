RUN COMMAND IN DOCKER-COMPOSE
gunicorn --bind 0.0.0.0:8000 --workers 2 "app:create_app()"

Testing the new build
