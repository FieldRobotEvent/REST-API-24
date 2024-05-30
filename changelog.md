# Changelog
## V2
### Container breaking changes
- **API Container:** <br>
The API container added Pandas and xlsx-writer as dependencies an has to be rebuild to work correctly

- **Database Container:** <br>
The database for task2 and task3 have been modified to differentiate between final results and data for the audience. Therefore it is needed to drop old databases using the docker compose down command with the -v flag so that the database will be rebuild with the new indices.

### New competitor endpoints
- ```task3/add-final-positions```: <br>
In a FRE leader meeting a new endpoint was requested to publish the final positions of the the
detected weed since the robot may get a better estimate of the position by detecting it multiple times
an correcting it in the software. Therefore this endpoint is provided to send the corrected data to the server
while the ```task3/add-position``` should be used to provide the audience with the robots first estimate of the positions.

    - **This endpoint can be called several times.**
    - **Already committed data will not be overridden.**
    - **All data committed on this endpoint is assumed to be final and will be graded.**
    - **Consequences of not providing data to this endpoint or only to ```task3/add-position``` have not been determined as of now.**

- ```task2/add-final-rows```: <br>
Same as ```task3/add-final-positions```.

### New admin endpoints
- ```admin/task2/results```: <br>
This endpoint lets the jury download the results for task2 as either an xlsx file or a zip file of csv files. The timestamps are converted from utc to local time Europe/Berlin for convenience.

- ```admin/task3/results```: <br>
Same as admin/task2/results