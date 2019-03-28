from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import requests
from pprint import pprint
# import requests_cache
from cassandra.cluster import Cluster
import markdown
import os
 


cluster = Cluster(["35.234.153.193"])
session = cluster.connect()

# requests_cache.install_cache('air_api_cache', backend='sqlite', expire_after=36000)

app = Flask(__name__, instance_relative_config=True)


# config
app.config.from_object('config')
app.config.from_pyfile('config.py')

# login and redirect to the page 
@app.route('/login/<user>/<password>')
def login_how(user, password):
    rows = session.execute( "Select * From users.stats where username = '{}'".format(user))
    row = list(rows)
    if len(row) == 0:
        return('<h1>Username does not exist!</h1>')
    else:
        check_hash = check_password_hash(row[0].password, password)
        if check_hash:
            return redirect(url_for('hello'))
        return ('<h1>Sorry! wrong password, please type in again!</h1>')


# register username and password as hash in the db
@app.route('/register/<username>/<password>')
def regsiter_user(username, password):

    session.execute("INSERT INTO users.stats (username, password) VALUES ('{}', '{}');".format(username, generate_password_hash(password)))

    return('<h2>User Created<h2/>')



#  testing route / hello world
@app.route('/hello')
def hello():
    name = request.args.get("name", "World")
    return('<h1>Hello, {}!</h1>'.format(name))


# the route to readme file
@app.route('/')
def index_index():
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        content = markdown_file.read()
        return markdown.markdown(content)


air_url_template = 'https://api.breezometer.com/air-quality/v2/historical/hourly?lat={lat}&lon={lng}&key={API_KEY}&start_datetime={start}&end_datetime={end}'


# see the Air_quality info
@app.route('/air/<location_name>', methods=['GET'])
def airchart(location_name):
    rows = session.execute("Select * From location.stats where location_name='{}'".format(location_name))

    for i in rows:
        my_latitude = request.args.get('lat', str(i.lat))
        my_longitude = request.args.get('lng', str(i.lng))
        my_start = request.args.get('start', str(i.start))
        my_end = request.args.get('end', str(i.end))
        air_url = air_url_template.format(lat=my_latitude, lng=my_longitude, API_KEY=app.config['MY_API_KEY'], start=my_start, end=my_end)

        resp = requests.get(air_url)

        if resp.ok:
            resp = requests.get(air_url)
            pprint(resp.json())

        else:
            print(resp.reason)

    info = {
        "theday": resp.json()["data"][0]["datetime"],
        "catergory": resp.json()["data"][0]["indexes"]["baqi"]["category"],
        "AQI": resp.json()["data"][0]["indexes"]["baqi"]["aqi"],
        "dominant_pollutant": resp.json()["data"][0]["indexes"]["baqi"]["dominant_pollutant"]
        }

    return render_template('htmlplaceholder.html', info=info)


# create new record
@app.route('/air/set/<location_name>/<lat>/<lng>/<start>/<end>')
def writenew(location_name, lat, lng, start, end):
    session.execute("INSERT INTO location.stats (location_name,lat,lng,start,end) VALUES ('{}', '{}', '{}', '{}', '{}');".format(location_name, lat, lng, start, end))

    return("Record Created")

# delete a record
@app.route('/air/remove/<location_name>')
def remove(location_name):
    session.execute("DELETE FROM location.stats WHERE location_name ='{}' IF EXISTS;".format(location_name))

    return("Record Deleted")


if __name__== "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
