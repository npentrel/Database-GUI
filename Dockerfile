# our base image
FROM python:3.6-alpine

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# copy files required for the app to run
COPY app.py /usr/src/app/
ADD templates /usr/src/app/templates/

# outside Heroku you will generally have to expose a port under which you will
# then be able to access your application
EXPOSE 9001

# run the application
CMD python /usr/src/app/app.py $PORT
