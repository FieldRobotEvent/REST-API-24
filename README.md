# REST-API-24

<p align="middle">
  <a href="https://fieldrobot.nl/event/"><img src="docs/static/logos/FRE-logo.png" height="160" alt="International Field Robot Event"></a>
</p>
<p align="middle">
  <a href="https://www.hs-osnabrueck.de/"><img src="docs/static/logos/HS-OS-Logo.png" height="160" style="margin: 10px;" alt="Hochschule Osnabrueck"></a>
</p>
<p align="middle">
  <a href="https://editor.swagger.io/?url=https://raw.githubusercontent.com/FieldRobotEvent/REST-API-24/main/docs/static/openapi.json"><img src="https://img.shields.io/badge/open--API-V3.1-brightgreen.svg?style=flat&label=OpenAPI" alt="OpenAPI"/></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white" alt="Python 3.11"/></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?style=flat&logo=FastAPI&logoColor=white" alt="FastAPI"/></a>
  <a href="https://www.gnu.org/licenses/gpl-3.0"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License: GPL v3"/></a>
</p>

> **&#9888; API changed to version 2!** <br>
Look the [changelog](changelog.md) for information.

## Description
REST-API code for task 2, 3 and 4 of the 2024 Field Robot Event.

REST Communication and Interface

Tasks 2, 3 and 4 require data exchange with a central benchmark and validation server (BVS). The
BVS will provide a REST API and its definition will be published as an OpenAPI (https://www.openapis.org/) definition in
May. A test BVS will be up and running by midst of May. For the communication, the organizing
team will provide an access point which has to be fixed on the field robot, e.g. by Velcro band.
The field robot has to send its data via ethernet cable to the access point, no additional WLAN is
required by the teams.

## Usage
To interact with a running instance of the API the OpenAPI description is provided [here](docs/static/openapi.json).\
For description on how to interact with the API and examples using ```curl``` look [here](docs/api-example.md).

## Requirements
- Docker with compose plugin

## Build the API
Before the API can be used the containers have to be build first.
To build the containers issue the following command in the same folder as the ```docker-compose.yml```:

```
docker compose --env-file=dev.env build
```

**Note: To build the containers the first time an connection to the internet is required.**

## Starting the API
To start the API the following command needs to be issued in the same folder as the ```docker-compose.yml```:

```
docker compose --env-file=<env_file> up -d --wait
```
There are three pre-supplied env files available:
- ```demo.env``` - Starts the API in demo mode (only user endpoints)
- ```dev.env``` - Fully starts API with pre-configured settings (user and admin endpoints)
- ```competition.env``` - Boilerplate for own configuration (see [here](#configuring-the-api-for-the-competition))

**Note: For just testing the API use ```demo.env``` the dev.env is meant for development.**

## Stopping the API
To simply stop the services while keeping the database data the following command can be issued in the same folder as the ```docker-compose.yml```:

```
docker compose --env-file=<env_file> down
```

To also remove the database data run the command with the ```-v``` flag:

```
docker compose --env-file=<env_file> down -v
```

**Beware: Using the ```-v``` flag will clear the database and all by doing so delete all data for the groups.**

## Configuring the API for the competition

<details>
    <summary> Expand</summary>

To configure for competition the following entries in the ```competition.env``` have to be populated with the data for the competition.
- All entries are expected to be JSON formatted.
- Currently unused ```TASK``` entries can be set as empty arrays.
- ```ADMIN_API_KEY``` and ```FRE_POSTGRES_PASSWD``` have to be set before first run or the stack will fail to start.

### Group entries:
A group entry consists of a name and an API-Key.
The following rules apply:
- Group ```name``` must be unique and should not contain special characters aside of space.
- The ```api-key``` should be unique and consist only of characters (upper and lower case) and numbers.
- The ```api-key``` should be at least 21 characters long.

```
GROUPS='[
    {
        "name": <name of the first group>,
        "api-key": <api key for the first group>
    },
    {
        "name": <name of the second group>,
        "api-key": <api key for the second group>
    },
    {
        "name": <name of the nth group>,
        "api-key": <api key for the nth group>
    }
]'
```

### Task 2 solution
For task 2 solutions following rules apply:
- ```row_number``` starts at 1.
- ```plant_count``` should be positive or 0.
- must be keep secret.

```
TASK2_ROWS_SOLUTION='[
    {
        "row_number": 1,
        "plant_count": <plant count first row>
    },
    {
        "row_number": 2,
        "plant_count": <plant count second row>
    },
    {
        "row_number": <n>, 
        "plant_count": <plant count nth row>
    }
]'
```

### Task 3 solution
For task 3 solutions following rules apply:
- ```x``` and ```y``` are in metre.
- must be keep secret.

```
TASK3_POSITIONS_SOLUTION='[
    {
        "x": <x float value first point>,
        "y": <y float value first point>
    },
    {
        "x": <x float value second point>,
        "y": <y float value second point>
    },
    {
        "x": <x float value nth point>,
        "y": <y float value nth point>
    }
]'
```

### Task 4 positions
For task 3 solutions following rules apply:
- ```x``` and ```y``` are in metre.

```
TASK4_POSITIONS='[
    {
        "x": <x float value first point>,
        "y": <y float value first point>
    },
    {
        "x": <x float value second point>,
        "y": <y float value second point>
    },
    {
        "x": <x float value nth point>,
        "y": <y float value nth point>
    }
]'
```

### Admin API key
For the admin API key the following rules apply:
- Must consist only of characters (upper and lower case) and numbers.
- Should be at least 21 characters long.
- Must be keep secret.

```
ADMIN_API_KEY=<admin API-Key>
```

### Postgres key
For the postgres key the following rules apply:
- Must consist only of characters (upper and lower case) and numbers.
- Should be at least 21 characters long.

```
FRE_POSTGRES_PASSWD=<Postgres database key>
```


## Starting the for competition
After configuring the competition.dev the stack can be started by running the following command in the same folder as the ```docker-compose.yml```:

```
docker compose --env-file=competition.env up -d --wait
```

If the ```competition.env``` is changed afterwards the stack has to be recreated by running the start command again.

**Beware: The Posgres key can not be changed once it has been set. To recover from an faulty postgres key the stack has to be stopped using the ```-v``` flag, clearing the entire database, and then restarted using the upper start command**

</details>

## Advanced

<details>
    <summary> Expand</summary>

## Backup database
To create an backup of the database run the following command in the same folder as the ```docker-compose.yml```:

```
docker compose --env-file=<env_file> exec postgres pg_dump -d fre -f /backups/fre.sql
```

Use the same env file you used to start the server.
The backup will be an SQL database dump called ```fre.sql``` in the backups folder.

**Note 1: Because the ```fre.sql``` file is created by the container you might have to claim ownership of the file depending on your filesystem.**

**Note 2: Calling the backup function multiple times will override the previous backup.**

## Debugging
For debugging purposes the logs of the for the containers can be printed out using:

```
docker compose --env-file=<env_file> logs <service_name>
```

Currently available service names are:
- ```api```
- ```postgres```
</details>
