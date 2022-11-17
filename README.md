1. Error Handling
Basic errors will be returned with the HTTP status code 2xx. The JSON format will be as follows:
{
  "status": 2xx,
  "description": "<ERROR_DESCRIPTION>"
}

2. TOKEN Management
a. CREATE TOKEN (POST)
i.	URL: POST http://192.168.1.25:5000/generateToken 
ii.	Request Header
"content-type": "application/json"
iii.	Request Body (type=JSON):
{
"user_data": "this is test"
}
iv.	Response Body (type=JSON):
{
"JWT Token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE2Njg2NzY5MDcsImp0aSI6ImYxMGZiNWY0NzQ2MWRlNGRkOGM3NjExM2NhZDc4MDNiIiwicGF5bG9hZCI6eyJkYXRhIjoidGhpcyBpcyB0ZXN0IiwiZGF0ZSI6IjIwMjItMTEtMTcifX0.LgY1OHZamo0irNBb3uGQvWRzdFEiBfjmyBOKewPAvPGqmFJGh3HaqdzDMZyX3TzKdTV35a748Xz6hoPOIxPWrA"
}
v.	Valid Error Codes
202	Invalid content type
200	Success
b. VALIDATE TOKEN (GET)
i.	URL: GET http://192.168.1.25:5000/verifyToken
ii.	Request Header
"content-type": "application/json"
iii.	Request Body (type=JSON):
{
	"Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE2Njg2NjQ0NDYsImp0aSI6IjBlNWNkYzRiYzk2YTE5ZDdmZGIzMzFlYzgxMTNkYWQwIiwicGF5bG9hZCI6eyJkYXRhIjoidGhpcyBpcyB0ZXN0IiwiZGF0ZSI6IjIwMjItMTEtMTcifX0.HChW1vzHVA6dD_j4f0zTMt2w7eKW5ydbjXBgUdRsmd6M93BcIbeEtqI9JIDnZJGWoX4MnoaUsEdorzfEDsgDrQ",
	"Signing_key": "a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf"
}
iv.	Response Body (type-JSON):
{
   "Header":
	 {
	 "typ": "JWT",
	 "alg": "HS512"
	  }, 
   "Claims":
	 {
	  "iat": 1668664446, 
	   "jti": "0e5cdc4bc96a19d7fdb331ec8113dad0",
	   "payload": 
	        {
	        "data": "this is test", 
	        "date": "2022-11-17"
	         }
	},
   "Signature Verification": true
}
v.	Valid Error Codes
202	Invalid content type
203	Missing token in GET request body
204	Missing singing key in GET request body
3. Parameters
Parameter	Data Type	Description
User_data	String	Data string inserted by user
JWT token	String	JWT token in for as defined in https://datatracker.ietf.org/doc/html/draft-ietf-oauth-json-web-token-19

typ		Type of token (JWT)
alg		Algorithm used i.e. HMAC512
iat		The "iat" (issued at) claim identifies the time at which the JWT was issued.
jti		16byte long nonce
Data		User provided data
Date		Today’s date
4. Pre-requisite libraries and modules
The utmost care taken to not to use 3rd party libs as dependency on them is often risky and not recommended. The python flask APP uses following modules:
Module	Version	Remarks
Python	3.9	Tested on 3.9 and 3.6 with below modules
Flask 	2.1.1	Hosting python app
Flask-RESTful	0.3.9	Adding REST API interface to Flask framework
gunicorn	20.1.0	Wsgi server
hashlib, hmac, json, os, base64, datetime	Python v3.6 and v3.9	Default/in-built modules
5. Steps to run app using python file
i.	Step-1: Make sure you are using python v3.6 or above and another dependent module as mentioned in above table.
ii.	Step-2: gunicorn Web Server Gateway Interface server for hosting flask app.
iii.	Step-3: Open the python file (jwt_token.py) with editor of choice and modify the IP address (line 139) (optionally the port) and change the IP address (and port) to the IP address (and port) of your dev machine which is accessible via any REST command tool. You can set it to 127.0.0.1 or 0.0.0.0 as well.
iv.	Step-4: Save and close.
v.	Step-5: run the below command:
gunicorn -w 1 -b <new_ip>:5000 jwt_token:sessionManager
Output of this command should be like:
[2022-11-17 05:50:43 -0500] [356075] [INFO] Starting gunicorn 20.1.0
[2022-11-17 05:50:43 -0500] [356075] [INFO] Listening at: http://192.168.1.17:5000 (356075)
[2022-11-17 05:50:43 -0500] [356075] [INFO] Using worker: sync
[2022-11-17 05:50:43 -0500] [356078] [INFO] Booting worker with pid: 356078

6. Steps to run app using docker
i.	Step-1: unzip the provided tar file [‘castlabs_challenge_docker.tar.gz’]
ii.	Step-2: Go inside castlabs directory.
iii.	Step-3: Make sure that system is installed with docker compose version 2.2 or above.
iv.	Step-4: run the below command (from within castlabs directory):
$ docker-compose up –build

If the command is run for the first time, following logs will be required:

WARNING: Found orphan containers (castlabs_flaskapp_1, castlabs_code_1) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.
Building flaskcode
Sending build context to Docker daemon  8.704kB
Step 1/9 : FROM python:3.6-alpine
 ---> 3a9e80fa4606
Step 2/9 : RUN mkdir /flaskcode
 ---> Using cache
 ---> 3019e8acb405
Step 3/9 : WORKDIR /flaskcode
 ---> Using cache
 ---> 4406a7522a69
Step 4/9 : ADD jwt_token.py /flaskcode
 ---> ac0a7d56e7f6
Step 5/9 : RUN /usr/local/bin/python3 -m pip install --upgrade pip
 ---> Running in 75dcfa545b14
Requirement already satisfied: pip in /usr/local/lib/python3.6/site-packages (21.2.4)
Collecting pip
  Downloading pip-21.3.1-py3-none-any.whl (1.7 MB)
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 21.2.4
    Uninstalling pip-21.2.4:
      Successfully uninstalled pip-21.2.4
Successfully installed pip-21.3.1
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
Removing intermediate container 75dcfa545b14
 ---> d91aba53f4ed
Step 6/9 : RUN pip3 install flask_restful
 ---> Running in 627d9bd03477
Collecting flask_restful
  Downloading Flask_RESTful-0.3.9-py2.py3-none-any.whl (25 kB)
Collecting pytz
  Downloading pytz-2022.6-py2.py3-none-any.whl (498 kB)
Collecting Flask>=0.8
  Downloading Flask-2.0.3-py3-none-any.whl (95 kB)
Collecting aniso8601>=0.82
  Downloading aniso8601-9.0.1-py2.py3-none-any.whl (52 kB)
Collecting six>=1.3.0
  Downloading six-1.16.0-py2.py3-none-any.whl (11 kB)
Collecting Jinja2>=3.0
  Downloading Jinja2-3.0.3-py3-none-any.whl (133 kB)
Collecting click>=7.1.2
  Downloading click-8.0.4-py3-none-any.whl (97 kB)
Collecting Werkzeug>=2.0
  Downloading Werkzeug-2.0.3-py3-none-any.whl (289 kB)
Collecting itsdangerous>=2.0
  Downloading itsdangerous-2.0.1-py3-none-any.whl (18 kB)
Collecting importlib-metadata
  Downloading importlib_metadata-4.8.3-py3-none-any.whl (17 kB)
Collecting MarkupSafe>=2.0
  Downloading MarkupSafe-2.0.1-cp36-cp36m-musllinux_1_1_x86_64.whl (29 kB)
Collecting dataclasses
  Downloading dataclasses-0.8-py3-none-any.whl (19 kB)
Collecting typing-extensions>=3.6.4
  Downloading typing_extensions-4.1.1-py3-none-any.whl (26 kB)
Collecting zipp>=0.5
  Downloading zipp-3.6.0-py3-none-any.whl (5.3 kB)
Installing collected packages: zipp, typing-extensions, MarkupSafe, importlib-metadata, dataclasses, Werkzeug, Jinja2, itsdangerous, click, six, pytz, Flask, aniso8601, flask-restful
Successfully installed Flask-2.0.3 Jinja2-3.0.3 MarkupSafe-2.0.1 Werkzeug-2.0.3 aniso8601-9.0.1 click-8.0.4 dataclasses-0.8 flask-restful-0.3.9 importlib-metadata-4.8.3 itsdangerous-2.0.1 pytz-2022.6 six-1.16.0 typing-extensions-4.1.1 zipp-3.6.0
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
Removing intermediate container 627d9bd03477
 ---> 9f0593313bf4
Step 7/9 : RUN pip3 install flask
 ---> Running in fd7b91934770
Requirement already satisfied: flask in /usr/local/lib/python3.6/site-packages (2.0.3)
Requirement already satisfied: click>=7.1.2 in /usr/local/lib/python3.6/site-packages (from flask) (8.0.4)
Requirement already satisfied: itsdangerous>=2.0 in /usr/local/lib/python3.6/site-packages (from flask) (2.0.1)
Requirement already satisfied: Jinja2>=3.0 in /usr/local/lib/python3.6/site-packages (from flask) (3.0.3)
Requirement already satisfied: Werkzeug>=2.0 in /usr/local/lib/python3.6/site-packages (from flask) (2.0.3)
Requirement already satisfied: importlib-metadata in /usr/local/lib/python3.6/site-packages (from click>=7.1.2->flask) (4.8.3)
Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.6/site-packages (from Jinja2>=3.0->flask) (2.0.1)
Requirement already satisfied: dataclasses in /usr/local/lib/python3.6/site-packages (from Werkzeug>=2.0->flask) (0.8)
Requirement already satisfied: zipp>=0.5 in /usr/local/lib/python3.6/site-packages (from importlib-metadata->click>=7.1.2->flask) (3.6.0)
Requirement already satisfied: typing-extensions>=3.6.4 in /usr/local/lib/python3.6/site-packages (from importlib-metadata->click>=7.1.2->flask) (4.1.1)
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
Removing intermediate container fd7b91934770
 ---> bfe799309167
Step 8/9 : RUN pip3 install gunicorn
 ---> Running in a4248635edcf
Collecting gunicorn
  Downloading gunicorn-20.1.0-py3-none-any.whl (79 kB)
Requirement already satisfied: setuptools>=3.0 in /usr/local/lib/python3.6/site-packages (from gunicorn) (57.5.0)
Installing collected packages: gunicorn
Successfully installed gunicorn-20.1.0
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
Removing intermediate container a4248635edcf
 ---> f37ef4167110
Step 9/9 : CMD ["gunicorn", "-w 1", "-b", "0.0.0.0:8000", "jwt_token:flaskapp"]
 ---> Running in dfccb932676f
Removing intermediate container dfccb932676f
 ---> 6e2a8b881677
Successfully built 6e2a8b881677
Successfully tagged castlabs_flaskcode:latest
Recreating castlabs_flaskcode_1 ... done
Attaching to castlabs_flaskcode_1
flaskcode_1  | [2022-11-17 12:43:24 +0000] [1] [INFO] Starting gunicorn 20.1.0
flaskcode_1  | [2022-11-17 12:43:24 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
flaskcode_1  | [2022-11-17 12:43:24 +0000] [1] [INFO] Using worker: sync
flaskcode_1  | [2022-11-17 12:43:24 +0000] [8] [INFO] Booting worker with pid: 8
If the command is run for 2nd time, following logs will be delivered:
[root@localhost castlabs]# docker-compose up –build
WARNING: Found orphan containers (castlabs_flaskapp_1, castlabs_code_1) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.
Building flaskcode
Sending build context to Docker daemon  8.704kB
Step 1/9 : FROM python:3.6-alpine
 ---> 3a9e80fa4606
Step 2/9 : RUN mkdir /flaskcode
 ---> Using cache
 ---> 3019e8acb405
Step 3/9 : WORKDIR /flaskcode
 ---> Using cache
 ---> 4406a7522a69
Step 4/9 : ADD jwt_token.py /flaskcode
 ---> Using cache
 ---> ac0a7d56e7f6
Step 5/9 : RUN /usr/local/bin/python3 -m pip install --upgrade pip
 ---> Using cache
 ---> d91aba53f4ed
Step 6/9 : RUN pip3 install flask_restful
 ---> Using cache
 ---> 9f0593313bf4
Step 7/9 : RUN pip3 install flask
 ---> Using cache
 ---> bfe799309167
Step 8/9 : RUN pip3 install gunicorn
 ---> Using cache
 ---> f37ef4167110
Step 9/9 : CMD ["gunicorn", "-w 1", "-b", "0.0.0.0:8000", "jwt_token:flaskapp"]
 ---> Using cache
 ---> 6e2a8b881677
Successfully built 6e2a8b881677
Successfully tagged castlabs_flaskcode:latest
Starting castlabs_flaskcode_1 ... done
Attaching to castlabs_flaskcode_1
flaskcode_1  | [2022-11-17 12:54:08 +0000] [1] [INFO] Starting gunicorn 20.1.0
flaskcode_1  | [2022-11-17 12:54:08 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
flaskcode_1  | [2022-11-17 12:54:08 +0000] [1] [INFO] Using worker: sync
flaskcode_1  | [2022-11-17 12:54:08 +0000] [8] [INFO] Booting worker with pid: 8


7. Test the functionality:
7.1 Generating token:
7.1.1 CURL Request:
curl --location --request POST '192.168.1.17:8000/generateToken' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_data": "this is test3"
}'

7.1.2 CURL Response:
{"JWT Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE2Njg2OTAyMzMsImp0aSI6IjZiMDVkZmFjNGJhNjA2M2FjMzQxZDlkOWE3YmNjZWI4IiwicGF5bG9hZCI6eyJkYXRhIjoidGhpcyBpcyB0ZXN0MyIsImRhdGUiOiIyMDIyLTExLTE3In19.RPIUS8khOWVU91crsqHbIv_3dpWTisIFmbRo180Si9YunUxUIdxIUSE_Q2OGVthRxFt8xQ-RJ0CCetK18YEo3g"}

7.2 Verify Token:
7.2.1 CURL Request:
curl --location --request GET 'http://192.168.1.17:8000/verifyToken' \
--header 'Content-Type: application/json' \
--data-raw '{
    "Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE2Njg2Njg2NjIsImp0aSI6IjZlMTAyNTU1Y2U4NmFkNjk1MGYwYzkyOThiNTdhNzc5IiwicGF5bG9hZCI6eyJkYXRhIjoidGhpcyBpcyB0ZXN0MyIsImRhdGUiOiIyMDIyLTExLTE3In19.BEhKN0mRK8Umn_OciwUadr7fn0bEs2cnFPpk1nEE-YUUbVenvviHCdW_LpjyVU4a3C6cxbYRoTcxs0S7pfbSVA",
    "Signing_key": "a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf"
}'
7.2.2 CURL Response:
{"Header": {"typ": "JWT", "alg": "HS512"}, "Claims": {"iat": 1668668662, "jti": "6e102555ce86ad6950f0c9298b57a779", "payload": {"data": "this is test3", "date": "2022-11-17"}}, "Signature Verification": true}

