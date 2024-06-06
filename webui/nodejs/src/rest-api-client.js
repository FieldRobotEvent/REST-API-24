import axios from 'axios';
import { config } from './server-config.js';

const REST_API_BASE_URL = config.restApiBaseUrl;
const headers = {
    'x-api-key': config.restApiAdminKey,
};

/**
 * Fetches the list of teams from the REST API.
 * @returns {Promise<Array>} A promise that resolves with the list of teams.
 * @throws {Error} If there's an error fetching the teams list.
 */
export async function getTeamsList() {
    try {
        const response = await axios.get(`${REST_API_BASE_URL}/admin/teams`, { headers });
        return response.data;
    } catch (error) {
        throw new Error(`Error fetching teams list: ${error.message}`);
    }
}

/**
 * Fetches the ground truth count for each row of task 2 from the REST API.
 * @returns {Promise<Array>} A promise that resolves with the ground truth count of task 2.
 * @throws {Error} If there's an error fetching the ground truth count.
 */
export async function getTask2CountGroundTruth() {
    try {
        const response = await axios.get(`${REST_API_BASE_URL}/admin/task2/count-ground-truth`, { headers });
        return response.data;
    } catch (error) {
        throw new Error(`Error fetching task2 count ground truth: ${error.message}`);
    }
}

/**
 * Fetches the submitted counts for each row of task 2 for a specific team from the REST API.
 * @param {string} teamName - The full name of the team.
 * @param {bool} isFinal - Toggle to define is standard or final result should be queried.
 * @returns {Promise<Array>} A promise that resolves with the count of task 2 for the specified team.
 * @throws {Error} If there's an error fetching the count of task 2.
 */
export async function getTask2Count(teamName, isFinal) {
    try {
        const response = await axios.get(`${REST_API_BASE_URL}/admin/task2/count`, {
            headers,
            params: { group: teamName, final: isFinal },
        });
        return response.data;
    } catch (error) {
        throw new Error(`Error fetching task2 count from team ${teamName}: ${error.message}`);
    }
}

/**
 * Fetches the ground truth positions of task 3 from the REST API.
 * @returns {Promise<Array>} A promise that resolves with the ground truth positions of task 3.
 * @throws {Error} If there's an error fetching the ground truth positions.
 */
export async function getTask3PositionsGroundTruth() {
    try {
        const response = await axios.get(`${REST_API_BASE_URL}/admin/task3/positions-ground-truth`, { headers });
        return response.data;
    } catch (error) {
        throw new Error(`Error fetching task3 positions ground truth: ${error.message}`);
    }
}

/**
 * Fetches the submitted positions of task 3 for a specific team from the REST API.
 * @param {string} teamName - The name of the team.
 * @param {bool} isFinal - Toggle to define is standard or final result should be queried.
 * @returns {Promise<Array>} A promise that resolves with the positions of task 3 for the specified team.
 * @throws {Error} If there's an error fetching the positions of task 3.
 */
export async function getTask3Positions(teamName, isFinal) {
    try {
        const response = await axios.get(`${REST_API_BASE_URL}/admin/task3/positions`, {
            headers,
            params: { group: teamName, final: isFinal },
        });
        return response.data;
    } catch (error) {
        throw new Error(`Error fetching task3 positions from team "${teamName}": ${error.message}`);
    }
}

/**
 * Fetches the stopwatch data for a specific team from the REST API.
 * @param {string} task - The name of the task ("task2" or "task3").
 * @param {string} teamName - The name of the team.
 * @returns {Promise<Array>} A promise that resolves with the stopwatch data for the specified team.
 * @throws {Error} If there's an error fetching the stopwatch data.
 */
export async function getStopwatchData(task, teamName) {
    try {
        const response = await axios.get(`${REST_API_BASE_URL}/admin/${task}/start-stop`, {
            headers,
            params: { group: teamName },
        });
        return response.data;
    } catch (error) {
        throw new Error(`Error fetching stopwatch data from team "${teamName}": ${error.message}`);
    }
}
