import { config } from '../config.js';
import * as common from '../common/common.js';
import BarChart from './barChart.js';
import Stopwatch from '../common/stopwatch.js';

const hostname = window.location.hostname;
const port = window.location.port;
let ws;
let teamSelected = '';
let useFinalDataSelected = false;
let barChart;
let stopwatch = new Stopwatch('stopwatchDisplay', config.maxTimeMilliseconds);


export function onEventApplySettings() {
    const team = document.getElementById('teamSelect').value;
    const useFinalData = document.getElementById('checkboxSelectFinal').checked;
    console.log("Selected team:", team);
    updateSettings(team, useFinalData);
}

export function updateSettings(team, useFinalData) {
    teamSelected = team;
    useFinalDataSelected = useFinalData
    common.displaySelectedTeamName(team);
    if (team === '') {
        common.displaySelectedTeamName("Select a Team ...");
        stopwatch.updateStopwatch(false, 0);
        if (barChart) {
            barChart.resetChart();
        }
    }
    resetRowCounts();

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

export function updateTeamList(teams) {
    const selectElement = document.getElementById('teamSelect');
    selectElement.innerHTML = '';
    selectElement.appendChild(document.createElement('option'));

    teams.forEach(team => {
        const option = document.createElement('option');
        option.value = team;
        option.textContent = team;
        selectElement.appendChild(option);
    });
}

export function updateTaskSelected(task) {
    if (ws.readyState === WebSocket.OPEN) {
        const data = {
            taskSelected: task
        };
        ws.send(JSON.stringify(data));
    } else {
        console.error('WebSocket connection is not open.');
    }
}

function initRowCounts(countGroundTruth) {
    const rowsContainer = document.getElementById('rowsCountContainer');
    if (rowsContainer.children.length > 0) {
        return;
    }

    countGroundTruth.forEach((item, index) => {
        const rowNumber = index + 1;
        const row = document.createElement('div');
        row.className = 'row';
        row.id = `row_${rowNumber}`;

        const label = document.createElement('label');
        label.id = `row_label_${rowNumber}`;
        label.textContent = `Row ${rowNumber}:`;
        row.appendChild(label);

        const textSpanCount = document.createElement('span');
        textSpanCount.id = `row_count_${rowNumber}`;
        textSpanCount.textContent = '';
        row.appendChild(textSpanCount);

        rowsContainer.appendChild(row);
    });
}

function updateRowCounts(countData, countGroundTruth) {
    // Initialize array for counts for bar chart (default 0 if not set yet)
    let counts = Array(countGroundTruth.length).fill(0);

    // Reverse count data so that new data can override old data
    countData.reverse();

    // Update counts array with actual data where available, 0 otherwise
    countData.forEach((item) => {
        const rowIndex = item.row_number - 1;
        counts[rowIndex] = item.plant_count;

        // Update text content for the corresponding row count element
        const textSpanCount = document.getElementById(`row_count_${item.row_number}`);
        if (textSpanCount) {
            textSpanCount.textContent = item.plant_count;
        }
    });

    // Update the chart with the counts
    if (barChart) {
        barChart.updateChart(counts);
    }
}


function resetRowCounts() {
    const rowsContainer = document.getElementById('rowsCountContainer');
    const rowCounts = rowsContainer.querySelectorAll('[id^="row_count_"]');
    rowCounts.forEach((row) => {
        row.textContent = '';
    });
}

function initWebSocket() {
    ws = new WebSocket('ws://' + hostname + ':' + port);

    // Define WebSocket Event Handlers
    ws.onopen = function () {
        console.log('WebSocket connection established');
        updateTaskSelected('task2');
        updateSettings(teamSelected, useFinalDataSelected);
    };

    ws.onmessage = function (event) {
        const data = JSON.parse(event.data);
        console.log('Received data:', data);

        if (data.teams) {
            // Init team list
            if (teamSelected === '') {
                updateTeamList(data.teams);
            }
        }
        if (data.stopwatchState) {
            stopwatch.updateStopwatch(data.stopwatchState.running, data.stopwatchState.elapsedTime)
        }
        if (data.task2CountGroundTruth) {
            if (!barChart) {
                barChart = new BarChart(document.getElementById('barChart').getContext('2d'));
                barChart.createBarChart(data.task2CountGroundTruth);
            }
            initRowCounts(data.task2CountGroundTruth);
        }
        if (data.task2Count) {
            updateRowCounts(data.task2Count, data.task2CountGroundTruth);
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

function initializeApp() {
    const teamSelectBox =  document.getElementById('teamSelect');
    const selectFinalCheckbox = document.getElementById('checkboxSelectFinal');
    teamSelectBox.addEventListener('change', onEventApplySettings)
    selectFinalCheckbox.addEventListener('change', onEventApplySettings)

    initWebSocket();

    // Hide or show the list of sent counts based on the config
    if (!config.task2.showSentCountsList) {
        document.getElementById('rowsCountContainer').style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', initializeApp);
