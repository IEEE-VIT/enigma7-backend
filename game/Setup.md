### Setting Up Rabbitmq and Celery .

#### Ubuntu :

##### Installing Rabbitmq

<pre>
sudo apt-get install -y erlang
sudo apt-get install rabbitmq-server
</pre>

##### Installing Celery and django-celery-beat

<pre>
pip install celery django-celery-beat 
</pre>

##### Add a shared task (<a href ='https://django-celery-beat.readthedocs.io/en/latest/'>Better explanation</a>)

<ul>
<li>Login to admin panel</li>
<li>Under django-celery-beat add a new task</li>
<li>Add a registered function with its periodicity as one hour</li>
</ul>


##### Starting the shared task (Server needs to keep running)

<pre>
celery -A enigma7_backend worker --beat --scheduler django --loglevel=info
</pre>