import { config } from '../config.js';
import * as common from '../common/common.js';
import * as utils from './utils.js';
import Stopwatch from '../common/stopwatch.js';

const hostname = window.location.hostname;
const port = window.location.port;
const canvas = document.getElementById('fieldCanvas');
let stopwatch = new Stopwatch('stopwatchDisplay', config.maxTimeMilliseconds);
let teamSelected = '';
let useFinalDataSelected = false;
let ws;

function updateTeamList(teams) {
    const selectElement = document.getElementById('teamSelect');
    selectElement.innerHTML = '';
    // add initial empty option
    selectElement.appendChild(document.createElement('option'));

    teams.forEach(team => {
        const option = document.createElement('option');
        option.value = team;
        option.textContent = team;
        selectElement.appendChild(option);
    });
}

// Function to handle team selection from the dropdown
function onEventApplySettings() {
    const selectElement = document.getElementById('teamSelect');
    const useFinalData = document.getElementById('checkboxSelectFinal').checked;
    var team = selectElement.value;
    console.log("Selected team:", team);
    // Update the server with the selected team
    updateSettings(team, useFinalData);
}

function updateSettings(team, useFinalData) {
    teamSelected = team;
    useFinalDataSelected = useFinalData
    // reset sentPositionsList
    setPositionsList([]);
    if (team === '') {
        common.displaySelectedTeamName("Select a Team ...");
        stopwatch.updateStopwatch(false, 0);
    } else {
        common.displaySelectedTeamName(team);
    }

    if (ws.readyState === WebSocket.OPEN) {
        const data = {
            teamSelected: team,
            useFinalData: useFinalData
        };
        ws.send(JSON.stringify(data));
    } else {
        console.error('WebSocket connection is not open.');
    }
}

function updateTaskSelected(task) {
    if (ws.readyState === WebSocket.OPEN) {
        const data = {
            taskSelected: task
        };
        ws.send(JSON.stringify(data));
    } else {
        console.error('WebSocket connection is not open.');
    }
}

function createPositionEntryElement(ordinate, value) {
    // Add a space if positive value to align positive and negative values
    var valueString;
    if (value >= 0) {
        valueString = `&nbsp;${value.toFixed(3)}`;
    } else {
        valueString = `${value.toFixed(3)}`;
    }

    const entry = document.createElement('span');
    entry.className = 'sentPositionItem';
    entry.id = `sentPositionItem${ordinate.toUpperCase()}`;
    entry.innerHTML = `${ordinate}: ${valueString}`;
    return entry;
}

function setPositionsList(positions) {
    const listElement = document.getElementById('sentPositionsList');
    listElement.innerHTML = ''; // reset the list first

    positions.forEach(({ x, y }) => {
        const sentPositionItem = document.createElement('div');
        sentPositionItem.className = 'sentPositionItem';

        sentPositionItem.appendChild(createPositionEntryElement('x', x));
        sentPositionItem.appendChild(createPositionEntryElement('y', y));

        listElement.appendChild(sentPositionItem);
    });
}

function createLegend() {
    const legendContainer = document.getElementById('legend-container');

    let listContainer = legendContainer.querySelector('ul');

    if (!listContainer) {
        listContainer = document.createElement('ul');
        listContainer.style.display = 'flex';
        listContainer.style.flexDirection = 'row';
        listContainer.style.margin = 0;
        listContainer.style.padding = 0;

        legendContainer.appendChild(listContainer);
    }

    let items = [];

    // Add symbols and colors
    items.push({
        text: 'Real position of weeds',
        symbol: 'O',
        symbolColor: 'black',
        fontColor: '#666',
    });
    items.push({
        text: 'Correct reported position of weeds',
        symbol: 'X',
        symbolColor: 'green',
        fontColor: '#666',
    });
    items.push({
        text: 'Incorrect reported position of weeds',
        symbol: 'X',
        symbolColor: 'red',
        fontColor: '#666',
    });

    items.forEach(item => {
        const li = document.createElement('li');
        li.style.alignItems = 'center';
        li.style.cursor = item.cursor ?? 'pointer';
        li.style.display = 'flex';
        li.style.flexDirection = 'row';
        li.style.marginLeft = '30px';

        // Symbol
        const symbolSpan = document.createElement('span');
        symbolSpan.textContent = item.symbol;
        symbolSpan.style.color = item.symbolColor;
        symbolSpan.style.fontSize = '34px';
        symbolSpan.style.fontWeight = 'bold';
        symbolSpan.style.marginRight = '10px';

        // Text
        const textContainer = document.createElement('p');
        textContainer.style.color = item.fontColor;
        textContainer.style.margin = 0;
        textContainer.style.padding = 0;
        textContainer.style.textDecoration = item.hidden ? 'line-through' : '';
        textContainer.style.textAlign = item.textAlign ?? 'left';
        textContainer.style.fontSize = '34px';

        const text = document.createTextNode(item.text);
        textContainer.appendChild(text);

        li.appendChild(symbolSpan);
        li.appendChild(textContainer);
        legendContainer.appendChild(li);
    });
}

function initWebSocket() {
    ws = new WebSocket('ws://' + hostname + ':' + port);

    // Define WebSocket Event Handlers
    ws.onopen = function () {
        console.log('WebSocket connection established');
        updateTaskSelected('task3');
        updateSettings(teamSelected, useFinalDataSelected);
    };

    ws.onmessage = function (event) {
        const data = JSON.parse(event.data);
        console.log('Received data:', data);

        // Update team list
        if (data.teams) {
             // Init team list
            if (teamSelected === '') {
                updateTeamList(data.teams);
            }
        }
        if (data.stopwatchState) {
            stopwatch.updateStopwatch(data.stopwatchState.running, data.stopwatchState.elapsedTime)
        }
        // Drawings based on the received data
        if (data.task3PositionsGroundTruth) {
            utils.drawField(canvas); // Redraw the field to clear previous drawings
            data.task3PositionsGroundTruth.forEach(({ x, y }) => utils.drawFlowerGroundTruth(canvas, x, y));
        }
        if (data.task3Positions) {
            // draw current positions of flowers from the selected team
            data.task3Positions.forEach(({ x, y }) => utils.drawX(canvas, x, y, data.task3PositionsGroundTruth));
            setPositionsList(data.task3Positions);
        }
        if (data.robot) {
            utils.drawRobot(canvas, data.robot.x, data.robot.y);
        }
    };

    ws.onerror = function (error) {
        console.error('WebSocket error:', error);
    };

    ws.onclose = function (event) {
        console.log('WebSocket connection closed:', event);
        // Try to reconnect every 3 seconds
        setTimeout(() => {
            console.log('WebSocket: Trying to reconnect ...')
            initWebSocket();
        }, 3000);
    };
}

// Initialize the canvas and set up the event listener for server-sent events
function initializeApp() {
    const teamSelectBox =  document.getElementById('teamSelect');
    const selectFinalCheckbox = document.getElementById('checkboxSelectFinal');
    teamSelectBox.addEventListener('change', onEventApplySettings)
    selectFinalCheckbox.addEventListener('change', onEventApplySettings)

    createLegend();
    initWebSocket();

    // Hide or show the list of sent positions based on the config
    if (!config.task3.showSentPositionsList) {
        document.getElementById('sentPositionsDisplayContainer').style.display = 'none';
    }

    // Initializes the canvas and sets up the event listener for server-sent events.
    utils.drawField(canvas);
}

// Call initializeApp when the DOM content is loaded
document.addEventListener('DOMContentLoaded', initializeApp);
