FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

# The below lines are needed to enable ssh-ing into the container
# for heroku deployment. These should not effect local docker
# deployments. Please do not remove.
ADD ./.profile.d /app/.profile.d
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update -y
RUN apt-get install openssh-client -y
RUN apt-get install openssh-server -y

CMD gunicorn wwcodesvtools.wsgi:application --bind 0.0.0.0:$PORT