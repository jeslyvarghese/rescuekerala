FROM fnndsc/ubuntu-python3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get update && DEBIAN_FRONTEND=noninteractive  apt-get install -y libssl1.0.0 postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3
USER postgres
RUN /etc/init.d/postgresql start &&\
  psql --command "CREATE USER rescueuser WITH SUPERUSER PASSWORD 'password';" && createdb -O rescueuser rescuekerala
USER root
COPY . .
ENV SECRET_KEY secret
ENV ALLOWED_HOSTS localhost,127.0.0.1
ENV DEBUG 1
ENV B_DATABASE_URL postgresql://rescueuser:password@localhost/rescuekerala
ENTRYPOINT service postgresql start && python manage.py migrate && python manage.py collectstatic &&  /bin/bash


