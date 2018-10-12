<div style="background-image:url(./images/iris_jumbo_bg.png); background-color:black;">
    <div style="position: relative; left: 0; top: 0;">
        <img src="./images/iris_logo_colour.png" style="position: relative; top: 0; left: 0;"/>
    </div>
</div>

# Iris MySQL Agent

This repository contains the MySQL agent for my final year project [Iris](https://github.com/DeanGaffney/iris). This agent uses a python script to get the memory usage of a specific database. The memory usage and database name is then sent to Iris where it is displayed on a chart in real time. This agent was deployed on the same EC2 instance as the Iris web application and was run every day using cron to keep track of Iris' database memory.

## Running the Agent

### Prerequisites
* Make sure Iris is running.
* Configre MySQL for Iris by creating a MySQL database called **'iris'**.
* Configure Elasticsearch for Iris by adding an Endpoint in Iris which points to your Elasticsearch url.
* Create a schema in Iris for the mysql agent which looks like the following:
  ```json
  {
    "databaseName": "<YOUR STRING>",
    "memoryMB": "<YOUR FLOAT>"
  }
  ```
  This can be done by using the Schema builder in iris and matching the keys and data types to the json schema you see above.
* Once the Schema is saved you may create a dashboard with charts that are associated with the schema.
* Rename the ***conf.template.json*** file in the root of the agents directory to ***conf.json*** and fill out the missing details for your iris agent. The url for the "iris.agent.url" can be found by inspecting the URI section on your newly created Schema from the Schema page in Iris. Example images can be found below.

### Running with Docker

* Run the following command to build the docker image:
  ```bash
  $ docker build -t iris-mysql .
  ```
* Run the following command to run the container:
  ```bash
  $ docker run -it --rm --name iris-mysql iris-mysql
  ```
  If you are testing the container locally set the network argument so the command looks like the following:
  ```bash
  $ sudo docker run -it --rm --network="host" --name iris-mysql iris-mysql
  ```

## Agent Schema
The following is the schema that was created in Iris for the agent.
![Iris UI Schema](./images/iris-mysql-schema.PNG)

## Agent Dashboard
The following image shows the dashboard for the agent inside Iris where it is keeping track of the Iris database memory.
![Iris Dashboard](./images/iris-mysql-dashboard.PNG)

## Agent Transformation Rule
This agent has no transformation rule, please see the [Node.js Agent](https://github.com/DeanGaffney/iris-node) for an example of a transformation rule.

## Other Iris agents
* [Selenium](https://github.com/DeanGaffney/iris-selenium)
* [Node.js](https://github.com/DeanGaffney/iris-node)
* [Android](https://github.com/DeanGaffney/iris-android)
* [Crypto Currency Rates](https://github.com/DeanGaffney/iris-crypto-rates)

## Built With

- Python

## Authors

* **Dean Gaffney**

See also the list of [contributors](https://github.com/DeanGaffney/iris-mysql/graphs/contributors) who participated in this project.