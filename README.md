<p align="center"><img src="https://raw.githubusercontent.com/IEEE-VIT/enigma7-frontend/master/src/images/enigma.svg"/></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg?style=flat-square)
[![GitHub Issues](https://img.shields.io/github/issues/aryan9600/IEEE-CTF-Questions.svg)](https://github.com/IEEE-VIT/enigma7-backend/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg?style=flat-square)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![All Contributors](https://img.shields.io/badge/all_contributors-3-yellow.svg?style=flat-square)](#contributors-)

## About
Enigma is an online cryptic hunt organized by the IEEE-VIT Student Chapter anually. Enigma 7.0 was live from 4th December 4:20 PM (IST) to 6th December 4:20 PM (IST). Like all of it's previous editions, it remained undefeated with nobody being able to solve all the challenges.

This repository contians the codebase for the backend used for Enigma 7.0.

## Architecture

<p align="center"><img src="https://raw.githubusercontent.com/IEEE-VIT/enigma7-backend/master/enigma_flow.png"/></p>

## Tools and Technologies

* Django
* PostgreSQL
* Redis
* Celery
* HAProxy
* Docker/docker-compose
* GCP

## Getting Started
Please refer to the above list of tools and make sure you're familiar with the ones that concern you before you actually start working.

To get started:
* Clone the repo.
`git clone https://github.com/ieee-vit/enigma7-backend`
* Install the dependencies (inside a virtual environment preferably).
`pip install -r requirements.txt`
* Create a PostgreSQL database.
`createdb enigma7`
* Create a `.env` at the root of the project directory and populate it by referring to the `.env.template`.

##### Running a dev server
* Generate migrations and apply them.
`python manage.py makemigrations`
`python manage.py migrate`
* Run the server.
`python manage.py runserver`

##### Running the Celery workers
* We need a message queue for Celery. We went ahead with Redis, but we can also use RabbitMQ. To run Redis, first [install](https://redis.io/download) it and run
`redis-server`
* Run the main Celery worker.
`celery -A enigma7_backend worker --loglevel=DEBUG`
* Run the Celery Beat worker for executing periodic tasks:
`celery -A enigma7_backend beat -l DEBUG --scheduler django_celery_beat.schedulers:DatabaseScheduler`

##### Using Docker
We include a `Dockerfile.dev` and `docker-compose.dev.yml` to spin up a dev server quickly. From the root of the project, run:
* `docker-compose up -f docker-compose.dev.yml`
> Note: Please make sure that your `.env` with all the correct values is present in the codebase inside the container filesystem. You can also use the [`--env-file`](https://docs.docker.com/compose/environment-variables/) flag as well.


## Contributing
To start contributing, check out [`CONTRIBUTING.md`](https://github.com/aryan9600/IEEE-CTF-Questions/tree/master/CONTRIBUTING.md) . New contributors are always welcome to support this project. If you want something gentle to start with, check out issues labelled as easy or good-first-issue.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/aryan9600"><img src="https://avatars0.githubusercontent.com/u/43110940?s=460&u=8a10a5d6d3407128d666fe58a181ebf6ca6ccb1b?v=4" width="100px;" alt=""/><br /><sub><b>Sanskar Jaiswal</b></sub></a><br /> <a href="https://github.com/ieee-vit/enigma7-backend/commits?author=aryan9600" title="Documentation">📖 <a href="https://github.com/ieee-vit/IEEE-CTF-Questions/commits?author=aryan9600" title="Code"> 💻 </a><a href="#infra-aryan9600" title="Infrastructure (Hosting, Build-Tools, etc)"> 🚇 </a>
    <td align="center"><a href="https://github.com/aryanshridhar"><img src="https://avatars.githubusercontent.com/u/53977614?v=4" width="100px;" alt=""/><br /><sub><b>Aryan Shridhar</b></sub></a><br /><a href="https://github.com/ieee-vit/enigma7-backend/commits?author=aryanshridhar" title="Code"> 💻 </a></td>
    <td align="center"><a href="https://github.com/hsrambo07 "><img src="https://avatars1.githubusercontent.com/u/60664245?s=460&u=1ac2ad98a7e07f0f3dc0734e1199c7a1586ce3b4&v=4" width="100px;" alt=""/><br /><sub><b>Harsh Singhal</b></sub></a><br /><a href="https://github.com/ieee-vit/enigma7-backend/commits?author=hsrambo07 " title="Code"> 💻 </a></td>
