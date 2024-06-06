import express from 'express';
import { v4 as uuidv4 } from 'uuid';
import cors from 'cors';
import { WebSocketServer, WebSocket } from 'ws';
import http from 'http';
import proxy from 'express-http-proxy';

import { config } from './server-config.js';
import * as api from './rest-api-client.js';
import * as stopwatchUtil from './stopwatch-util.js';

var app = express();

app.use(cors());
app.use(express.json());
app.use(express.static('public')); // Serve static files from public directory

// Initialize WebSocket Server
const server = http.createServer(app);
const wss = new WebSocketServer({ server });
let clients = []; // track connected clients

// Used to cache static data from REST API
let teams = [];
let task3PositionsGroundTruth = []; // ground truth position of flowers
let task2CountGroundTruth = []; // ground truth counts of plants per row
// let robot = { x: config.robotStartX, y: config.robotStartY }; // current robots position

wss.on('connection', function connection(ws) {
    const clientId = uuidv4();
    const client = {
        id: clientId,
        ws: ws,
        taskSelected: '',
        teamSelected: '',
        useFinalData: false,
    };
    clients.push(client);

    console.log(`Client connected: ${clientId}`);

    // Send initial data to the client
    const initialState = JSON.stringify({
        teams: teams,
        //task3PositionsGroundTruth: task3PositionsGroundTruth,
        //flowers: flowers,
        //robot: robot,
    });
    ws.send(initialState);

    ws.on('message', function incoming(message) {
        console.log(`Received message from ${clientId}: ${message}`);
        // Update client's selected task and team when sent from the client
        const data = JSON.parse(message);
        console.log('data:', data);

        if (data.taskSelected) {
            client.taskSelected = data.taskSelected;
            console.log(`Client ${clientId} updated task to: ${data.taskSelected}`);
        }
        if (data.teamSelected || data.teamSelected === '') {
            client.teamSelected = data.teamSelected;
            console.log(`Client ${clientId} updated team to: ${data.teamSelected}`);
        }
        if (typeof data.useFinalData === "boolean") {
            client.useFinalData = data.useFinalData;
            console.log(`Client ${clientId} updated useFinalData to: ${data.useFinalData}`);
        }

        // Update client with new data when a team is selected or task switched
        if (client.teamSelected === '') {
            // only send ground truth data when no team is selected
            switch (client.taskSelected) {
                case 'task2':
                    client.ws.send(JSON.stringify({
                        task2CountGroundTruth: task2CountGroundTruth,
                    }));
                    break;
                case 'task3':
                    client.ws.send(JSON.stringify({
                        task3PositionsGroundTruth: task3PositionsGroundTruth,
                    }));
                    break;
            }
        } else {
            // Team is selected; Send data from REST API the specific web client
            fetchData(client.taskSelected, client.teamSelected, client.useFinalData).then(fetchedData => {
                sendDataToClients(client.taskSelected, client.teamSelected, client.useFinalData, fetchedData, client);
            });
            // Also send current stopwatch data to clients
            api.getStopwatchData(client.taskSelected, client.teamSelected).then(stopwatchData => {
                const stopwatchState = stopwatchUtil.calculateStopwatchState(stopwatchData);
                sendStopwatchStateToClients(client.taskSelected, client.teamSelected, stopwatchState, client);
            });
        }
    });

    ws.on('close', function () {
        console.log(`Client disconnected: ${clientId}`);
        clients = clients.filter(client => client.id !== clientId);
    });
});

function sendDataToClients(task, team, isFinal, data, client = null) {
    // If a specific client is provided, send data only to that client
    if (client) {
        client.ws.send(JSON.stringify(data));
    } else {
    // Iterate through all connected WebSocket clients and send them the updated data
        clients.filter(
            (x) =>
                x.taskSelected === task &&
                x.teamSelected === team &&
                x.ws.readyState === WebSocket.OPEN
            ).forEach(wsClient => {
                if(data.task3Positions || data.task2Count) {
                    if(wsClient.useFinalData === isFinal) {
                        wsClient.ws.send(JSON.stringify(data));
                    }
                } else {
                    wsClient.ws.send(JSON.stringify(data));
                }
        });
    }
}

async function fetchData(task, team, isFinal) {
    switch (task) {
        case 'task2':
            try {
                const task2Count = await api.getTask2Count(team, isFinal);
                return {
                    task2CountGroundTruth: task2CountGroundTruth,
                    task2Count: task2Count,
                };
            } catch (error) {
                console.log(error);
            }

        case 'task3':
            try {
                const task3Positions = await api.getTask3Positions(team, isFinal);
                return {
                    task3PositionsGroundTruth: task3PositionsGroundTruth,
                    task3Positions: task3Positions,
                };
            } catch (error) {
                console.log(error);
            }
        default:
            return Promise.reject(new Error(`Unsupported task: ${task}`));
    }
}

function sendStopwatchStateToClients(task, team, stopwatchState, client = null) {
    const data = {
        stopwatchState: stopwatchState,
    };
    sendDataToClients(task, team, false, data, client);
}

function initRestApiWebSocket() {
    // Connect to websocket of REST API server to receive notifications about data updates
    // The REST API websocket server will notify this server when new data is added
    var wsRestApi = new WebSocket(config.restApiWebSocketUrl + '?x_api_key=' + config.restApiAdminKey);

    wsRestApi.onopen = function () {
        console.log('WebSocket connection to REST API server established');
    };

    wsRestApi.on('message', function message(message) {
        // somehow I need to parse twice wtf!
        var data = JSON.parse(message);
        data = JSON.parse(data);

        // Fetch new data from REST API and send updates to web clients
        if (data.event === 'add_data') {
            fetchData(data.task, data.group, false).then(fetchedData => {
                sendDataToClients(data.task, data.group, false, fetchedData);
            });
            fetchData(data.task, data.group, true).then(fetchedData => {
                sendDataToClients(data.task, data.group, true, fetchedData);
            });
        }
        // Fetch new stopwatch data from REST API and send updates to web clients
        if (data.event === 'start_task' || data.event === 'stop_task') {
            api.getStopwatchData(data.task, data.group).then(stopwatchData => {
                const stopwatchState = stopwatchUtil.calculateStopwatchState(stopwatchData);
                sendStopwatchStateToClients(data.task, data.group, stopwatchState);
            });
        }
    });

    wsRestApi.onclose = function (event) {
        console.log('WebSocket connection to REST API server closed');
        // Try to reconnect every 3 seconds
        setTimeout(() => {
            console.log('WebSocket: Trying to reconnect to REST API server ...')
            initRestApiWebSocket();
        }, 3000);
    };
}

app.get('/:task/results', proxy(config.restApiBaseUrl, {
    proxyReqOptDecorator: function (proxyReqOpts, srcReq) {
      proxyReqOpts.headers = {'x-api-key': config.restApiAdminKey};
      return proxyReqOpts;
    },
    proxyReqPathResolver: function (req) {
        var queryString = req.url.split('?')[1];
        return `/fre2024/admin/${req.params.task}/results` + (queryString ? '?' + queryString : '');
    }
}))

server.listen(config.port, () => {
    // Fetch initial data from REST API once and cache it
    console.log('Fetching initial data from REST API...');
    Promise.all([api.getTeamsList(), api.getTask2CountGroundTruth(), api.getTask3PositionsGroundTruth()])
        .then(function (results) {
            teams = results[0];
            task2CountGroundTruth = results[1];
            task3PositionsGroundTruth = results[2];

            console.log('Fetched initial data from REST API');
            console.log('Server listening on port 3000');
        })
        .catch(function (error) {
            console.error(error);
            console.error('Failed to fetch initial data from REST API, please restart the server.');
        });

    initRestApiWebSocket();
});
