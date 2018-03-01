#!/usr/bin/python

import mysql.connector
import simplejson as json
from mysql.connector import errorcode
import requests

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

agentData = {'name': 'mysql_agent'}

urlResp = requests.post('http://ec2-52-16-53-220.eu-west-1.compute.amazonaws.com:8080/iris/schema/getAgentUrl', data=json.dumps(agentData), headers=headers)

endpoint = urlResp.json()['url']

config = {
    'user': 'root',
    'password': 'iris',
    'host': '127.0.0.1',
    'database': 'iris'
}

cnx = cur = None
try:
    cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Something is wrong with your user name or password')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cur = cnx.cursor()
    cur.execute('SELECT table_schema AS "databaseName", ROUND(SUM(data_length + index_length) / 1024 /  1024, 2) as "memoryMB" FROM information_schema.TABLES GROUP BY table_schema;')
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    for result in rv:
        resp = requests.post(endpoint, data=json.dumps(dict(zip(row_headers,result))), headers=headers)
        print resp.json()
finally:
    if cur:
        cur.close()
    if cnx:
        cnx.close()
