# CKAN 2.10 Source Code Instalation

We follow the [CKAN documentation steps](https://docs.ckan.org/en/2.9/maintaining/installing/install-from-source.html#installing-ckan-from-source).

- [Install the required packages](https://docs.ckan.org/en/2.9/maintaining/installing/install-from-source.html#install-the-required-packages):
  - Documentation do not say to run `apt-get update`, that is necessary.

```
sudo apt-get update
sudo apt-get install python3-dev postgresql libpq-dev python3-pip python3-venv git-core openjdk-8-jdk redis-server graphviz
```

- configuração global do proxy para o git:

````
# Both http.proxy and https.proxy have the same value starting with http://
$ git config --global http.proxy http://user:pass@my.proxy.server:8080
$ git config --global https.proxy http://user:pass@my.proxy.server:8080
$ git config --list
````

- Proxy configuration:

````
echo export HTTP_PROXY=user:pass@my.proxy.server:8080 >> ~/.bash_profile
echo export HTTPS_PROXY=user:pass@my.proxy.server:8080 >> ~/.bash_profile
source ~/.bash_profile
echo $HTTP_PROXY
````

- JAVA Update

````
$ sudo apt update
$ sudo apt install default-jdk
$ sudo apt update
$ sudo apt install default-jre
````

- [Install CKAN into a Python virtual environment](https://docs.ckan.org/en/2.9/maintaining/installing/install-from-source.html#install-ckan-into-a-python-virtual-environment):

```
mkdir -p ~/ckan/lib
sudo ln -s ~/ckan/lib /usr/lib/ckan
mkdir -p ~/ckan/etc
sudo ln -s ~/ckan/etc /etc/ckan

# Create a Virtual Env
sudo mkdir -p /usr/lib/ckan/default
sudo chown `whoami` /usr/lib/ckan/default

# Check python version
python3 --version
```

- Virtual env criation and setuptools instalation

```
python3 -m venv /usr/lib/ckan/default
. /usr/lib/ckan/default/bin/activate
pip install setuptools==44.1.0
pip install --upgrade pip

# To check installation
pip list
```

- CKAN 2.10 clone

````
$ git clone https://github.com/ckan/ckan.git ckan_source
$ cd ckan_source/
$ git checkout dev-v2.10
$ pip install -r requirements.txt
$ python setup.py install
````

- Postgres:

```
sudo service postgresql start
sudo su postgres
createuser -S -D -R -P ckan_default
# password needed. We recomend to use: ckan_default
createdb -O ckan_default ckan_default -E utf-8

# to exit postgres user just type:
exit
```

- Create a CKAN config file:

```
sudo mkdir -p /etc/ckan/default
sudo chown -R `whoami` /etc/ckan/
ckan generate config /etc/ckan/default/ckan.ini

# Check if the file was created
cat /etc/ckan/default/ckan.ini
```

- Setup Solr

Download the binary version [https://solr.apache.org/downloads.html](https://solr.apache.org/downloads.html).

```
# This could take a while
wget https://www.apache.org/dyn/closer.lua/solr/solr/9.1.0/solr-9.1.0.tgz?action=download
tar -xvzf 'solr-9.1.0.tgz?action=download'
```

- Solr core creation

```
./solr-9.1.0/bin/solr start
./solr-9.1.0/bin/solr create -c ckan
```

- Check if proxy configuration are `off` inside `/etc/wgetrc` file:

````
$sudo vim /etc/wgetrc
````

- Test if it's running 

````
$ wget http://localhost:8983/solr
````

- Update schema (folder where ckan_source was installed)

```
cp ckan_source/ckan/config/solr/schema.xml solr-9.1.0/server/solr/ckan/conf/managed-schema.xml
```

- Redis

```
sudo service redis-server start
```

- Configurar o banco dados no ckan.ini

```
vim /etc/ckan/default/ckan.ini
```

- Change `sqlalchemy.url` configuration on `ckan.ini` file:

```
sqlalchemy.url = postgresql://ckan_default:ckan_default@localhost/ckan_default
```

- Create tables

```
ckan -c /etc/ckan/default/ckan.ini db init

# workaround if no proxy is required
$ NO_PROXY="*" ckan -c /etc/ckan/default/ckan.ini db init
```

- Create folder storage and `ckan.ini` update

```
mkdir /etc/ckan/default/storage
vim /etc/ckan/default/ckan.ini
```

- Update `ckan.storage_path` password:

```
ckan.storage_path = /etc/ckan/default/storage
```

- Create admin user:

```
$ ckan -c /etc/ckan/default/ckan.ini sysadmin add admin

# email and password (with at least 8 characters will be required)
```

- Supervisor Install

```
sudo apt install supervisor
```

- Supervisor configuration

```
sudo vim /etc/supervisor/conf.d/ckan.conf
```

- Add the following information inside the open file:

```
[program:ckan]
command= usr/lib/ckan/default/bin/ckan -c /etc/ckan/default/ckan.ini run
environment=NO_PROXY="*"
directory=/usr/lib/ckan/default/src/ckan
user=<user>
stdout_logfile=/usr/lib/ckan/default/gunicorn_supervisor_ckan.log
redirect_stderr=true
```

- Restart supervisor

```
sudo service supervisor start
sudo supervisorctl reread
sudo supervisorctl reload
```

- nginx:

```
sudo apt install nginx
sudo rm /etc/nginx/sites-enabled/default
sudo vim /etc/nginx/sites-enabled/ckan.conf
```

- Add the following information inside the open file:

```
server {
    listen 80;
    server_name <link without http://>;
    client_max_body_size 200m;
    access_log /usr/lib/ckan/default/src/ckan/nginx-access-ckan.log;
    error_log /usr/lib/ckan/default/src/ckan/nginx-error-ckan.log;
    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://127.0.0.1:5000;
            break;
        }
    }
}
```

- Add dominito to ckan.ini

````
$ sudo vim /etc/ckan/default/ckan.ini

ckan.site_url = <link with http://>
````

- Reload:

````
$ sudo supervisorctl reload
$ sudo supervisorctl reread
$ sudo supervisorctl restart ckan
$ sudo supervisorctl status
````











