/**
* Calculate the current state of the stopwatch based on the stopwatch data.
* The calculation is server-side to avoid timezone issues.
* @param {Array} stopwatchData - Array of stopwatch entries (starts/stops) from the REST API
* @returns {Object} - Object containing the current "running" state and "elapsedTime" in milliseconds
*/
export function calculateStopwatchState(stopwatchData) {
    let running = false;
    let elapsedTime = 0;
 
    // Find the most recent start timestamp
    const startEntryIndex = stopwatchData.findIndex(entry => entry.running);
    if (startEntryIndex !== -1) {
        // Find the most recent stop timestamp before the start timestamp
        const startEntry = stopwatchData[startEntryIndex];
        const startTime = new Date(startEntry.timestamp + 'Z').getTime();
        const stopEntry = stopwatchData.slice(0, startEntryIndex).reverse().find(entry => !entry.running);
        if (stopEntry) {
            // Stopwatch has been stopped. Calculate elapsed time between start and stop
            running = false;
            const stopTime = new Date(stopEntry.timestamp + 'Z').getTime();
            elapsedTime = stopTime - startTime;
        } else {
            // Stopwatch still running. Calculate elapsed time from start to now so the client can continue the stopwatch
            running = true;
            const currentTime = new Date().getTime();
            elapsedTime = currentTime - startTime;
        }
    }
 
    return { running, elapsedTime };
 }
