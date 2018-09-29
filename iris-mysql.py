#!/usr/bin/python

import mysql.connector
import simplejson as json
from mysql.connector import errorcode
import requests

headers = {'Content-type': 'application/json', 
           'Accept': 'text/plain',
           'X-Auth-Token': 'eyJhbGciOiJIUzI1NiJ9.eyJwcmluY2lwYWwiOiJINHNJQUFBQUFBQUFBSlZTdjBcL2JRQlIrRG9rb1FpcFFpVW9NZENuZGtDUEJtS21ndEJLeVFrV2FoVXF0THZiREhKenZ6TjBaa2dWbGdpRURxQzFTSlZaR1wvaE5ZK2dkVVpXQmw3dHAzaHVEQWdyakpmdmY1K1wvVjhmZ01WbzJFeDFvd0w0NmNpaTduMFRhcTVqQTJHbWVhMjYyY0dkWVEyUjN6TWdTMmF3TzN4U3VBRlVPS1JoVmZCRnR0bFZjRmtYRjF0YjJGb2F4ME5DMHJIZDR3Ym1pVzRwXC9TMmY4OGRLbzBQQkFwcTc2d0VvK3N3eGNKUVpkSTJsS3gzVXE0eFdvZkpZaGFvY051TnBrTzZRV2s1RTJZWU9vcVN0UVZHQVl5enpHNHFVdVZvTEV6Y21zMHNGOVVtMmxvQUwxSm1ETGw3bEtScG5YVjM3MnhLU3JBRCsxRHVwQjRkNnU2ZGdcL3FPeDE5V1FsQnFycVNaYThsRVJYeURPM0hpNzgxK1wvMzEwMm11VkFLaVQrYWVcL0tlWXpTOUM3K1BydlRWNjBGMXA0UFdTOWdOVTZLYm1aS3BnXC9hM1RLZjM1OStuRnljXC9obGhKUWQ0c1B6OXpIM1wvcTY1N3JKS1VxYVpWVU03SXRxOXNuc204cVdueVFkYjZQcE5ucVFDNlkrU0ZxTjdpWUtZNHBhMUVvTytMWXl0clFiMWI2MW1mYzI5VlZpVWNFbWlMXC9QTWJsbCtvR2hWXC9ldmp5Nk8zZjRsZ0JTcTdUR1JJbFU4V29FYVd0RkVmbkpcL01qdis4NnVjQkJqXC96ZjFtZmFkb1FBd0FBIiwic3ViIjoiYWRtaW4iLCJyb2xlcyI6WyJST0xFX1VTRVIiXSwiZXhwIjoxNTIwNDI2NDM4LCJpYXQiOjE1MjA0MjI4Mzh9.D-Ky6RgRQZrbfd4I5W642cV2ymJXwlWSIUG-rVWBo3o' }

agentData = {'name': 'mysql_agent'}

urlResp = requests.post('http://ec2-52-16-53-220.eu-west-1.compute.amazonaws.com:8080/iris/schema/getAgentUrl', data=json.dumps(agentData), headers=headers)

endpoint = urlResp.json()['url']

with open('./conf.json') as conf_file:
    config = json.load(conf_file)["database"]

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
            print(resp.json())
    finally:
        if cur:
            cur.close()
        if cnx:
            cnx.close()
