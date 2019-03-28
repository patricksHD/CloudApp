# Air Quality Service
RUNNING ON GCP


## Usage


### Set compute region
 


-`gcloud config set compute/zone europe-west4-b export PROJECT_ID="$(gcloud config get-value project -q)` 
 

### Install the environment requirements


- `python -m pip install -U -r requirements.txt ` 

- `sudo pip install -r requirements.txt `


### Activate the virtual environment

- `python3 -m venv flask_venv source flask_venv/bin/activate`

- `source flask_venv/bin/activate`




### Database

**Open the cqlsh**

-`kubectl exec -it cassandra-b2tn9 cqlsh`



**Create user database**

- `cqlsh> CREATE KEYSPACE users WITH REPLICATION ={'class' : 'SimpleStrategy', 'replication_factor' : 2};`  
- `cqlsh> CREATE TABLE users.stats (username text PRIMARY KEY, password text);`  
- `SELECT * FROM users.stats`  


**Create location database**

- `cqlsh> CREATE KEYSPACE location WITH REPLICATION ={'class' : 'SimpleStrategy', 'replication_factor' : 2};`  
- `cqlsh> CREATE TABLE users.stats (username text PRIMARY KEY, password text);`  
- `cqlsh> CREATE TABLE location.stats (location_name text PRIMARY KEY, lat text,lng text,start text,end text);`  


**How to drop/delete/insert into table**


- `cqlsh> DROP TABLE location.stats;`  
- `cqlsh> DESCRIBE location.stats;`  
- `cqlsh> DESCRIBE users.stats;` 
- `cqlsh> "INSERT INTO location.stats (location_name,lat,lng,start,end) VALUES ('Maryland','39.045753','-76.641273','2019-03-17T07:00:00Z','2019-03-18T07:00:00Z')"` 




### Deployment


**configure external IP of the pod**


- `kubectl expose pod cassandra-clnj9 --name cassandra-9042 --type LoadBalancer --port 9042 --protocol TCP`  




**build and push**

- `docker build -t gcr.io/maximal-cider-229310/locationn:v1 .`
- `docker push  gcr.io/maximal-cider-229310/locationn:v1`



**run and loadbalancing**

- `kubectl run locationnn --image=gcr.io/maximal-cider-229310/locationn:v1 --port 8080`

- `kubectl expose deployment locationnn --type=LoadBalancer --port 80 --target-port 8080`






### Route and response 

Readme file


**response**
<h2>README.md</h2>


 
@app.route('/hello')

**response**
 
<h2>Hello world!</h2>




@app.route('/air/location_name')



**response**

<h2>Time: 2019-03-17T07:00:00Z</h2>

<h2>Quality Catergory: Excellent air quality</h2>

<h2>Dominant_pollutant: o3 </h2>

<h2>AQI: 83</h2>



...




 







