# Description and examples on how to use the API

## Accessing the API
| Address             | Service                                    |
|---------------------|--------------------------------------------|
| API base address    | http://localhost:8000/fre2024/             |
| Swagger UI          | http://localhost:8000/fre2024/docs         |
| OpenAPI Description | http://localhost:8000/fre2024/openapi.json |

To access the API from a remote computer the IP Address of the server has to be used instead of localhost.

## Example groups and API-Keys for testing
| Group name     | API-Key                          |
|----------------|----------------------------------|
| HSOS Fighters  | i7apIK29KHa6YFuicZDlMBskco4cag0P |
| THGA ROWDIES   | Ml4WtCTktmewrnFLITcTyhqFkfbN2BoW |
| UNI OS Racers  | HDhq3zdzVQr9SebLDx8tDifXqH5JVgMC |

The group names are only used in the backend.
To interact with the API only the API-Key is used.

## Sending request to the API using curl
This are the example curl commands to send requests or data to the API. To use them with another configuration or host set the **x-api-key** and the **URL** to the new values.

**Note 1: The curl commands with the current arguments only work for demo or dev deployment on localhost.**

### Task 2: Add row
```bash
curl -X 'POST' \
  'http://localhost:8000/fre2024/task2/add-row' \
  -H 'x-api-key: i7apIK29KHa6YFuicZDlMBskco4cag0P' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"plant_count": 0, "row_number": 1}'
```

### Task 2: Start
```bash
curl -X 'POST' \
  'http://localhost:8000/fre2024/task2/start' \
  -H 'x-api-key: i7apIK29KHa6YFuicZDlMBskco4cag0P' \
  -H 'accept: application/json'
```

### Task 2: Stop
```bash
curl -X 'POST' \
  'http://localhost:8000/fre2024/task2/start' \
  -H 'x-api-key: i7apIK29KHa6YFuicZDlMBskco4cag0P' \
  -H 'accept: application/json'
```

### Task 3: add position
```bash
curl -X 'POST' \
  'http://localhost:8000/fre2024/task3/add-position' \
  -H 'x-api-key: i7apIK29KHa6YFuicZDlMBskco4cag0P' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"x": 0, "y": 0}'
```

### Task 3: Start
```bash
curl -X 'POST' \
  'http://localhost:8000/fre2024/task3/start' \
  -H 'x-api-key: i7apIK29KHa6YFuicZDlMBskco4cag0P' \
  -H 'accept: application/json'
```
### Task 3: Stop
```bash
curl -X 'POST' \
  'http://localhost:8000/fre2024/task3/start' \
  -H 'x-api-key: i7apIK29KHa6YFuicZDlMBskco4cag0P' \
  -H 'accept: application/json'
```

### Task 4: get positions
```bash
curl -X 'GET' \
  'http://localhost:8000/fre2024/task4/get-positions' \
  -H 'accept: application/json'
```

### Healthcheck: ping
```bash
curl -X 'GET' \
  'http://localhost:8000/fre2024/health/ping' \
  -H 'accept: application/json'
```
