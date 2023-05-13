# Python/Django Challenge

## Description
Python/Django implementation of the Santex challenge.

### Code organization

#### Data download
We create a class RequestSource in the module request_sources, this class implements methods
to obtain information from different api.football-data.org/v4/ apis. With this organization,
we can add other sources of data, implement their own methods following a common interface
and select the class to use with a parameter in settings and a factory class.

#### Views
The views that implement the endpoints are just common generic views, the most complex is
ImportLeagueView where we implement the data import, using the functions in RequestSource.
The post method in this view can be separated in other functions that put a format layer
between the data source and the view so this can be cleaner. That can be done in a second
version of this api.

#### Models
There are three models: Competition, Team, Player.

The Team reference a Competition in ManyToMany (Competitions have many teams and 
a team can be part of more than one competition). 

The Player can be just in one team at the same time, so we are using the data from the
last season by default.

#### Serializarers
The serializers just implement a generic ModelSerializer with some fields excluded.

### How to run the project
* Clone the project: `git clone https://github.com/droper/santex.git`
* Execute the docker-compose: `cd django-challenge; docker-compose up --build`

### Create two users
* Enter the bash of the web service: `docker-compose exec web bash`
* Create a superuser: `python manage.py createsuperuser`
* Login into `http://127.0.0.1:8000/admin/` and create a normal user.

### Invoke the endpoints

* To request the import_league endpoint: `curl -X POST -H "Content-Type: application/json" -d '{"league_code": "$CODE"}' http://127.0.0.1:8000/import_league`
* To request the players of a league: `http://127.0.0.1:8000/players?league_code=$CODE`
* To request a team data: `http://127.0.0.1:8000/team?tla=$TEAM_TLA&players=T`
* To request a team players data: `http://127.0.0.1:8000/team/players?team_code=$CODE`



