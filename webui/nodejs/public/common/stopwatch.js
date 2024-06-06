export default class Stopwatch {
    constructor(elementId, maxTimeMilliseconds) {
        this.elementId = elementId;
        this.stopwatchInterval = null;
        this.elapsedTime = 0;
        this.maxTimeMilliseconds = maxTimeMilliseconds;
    }

    displayStopwatch() {
        // If the stopwatch has reached the max time, stop the interval and display the max time instead
        const timeIsUpMessageElement = document.getElementById('timeIsUpMessage');
        if (this.elapsedTime >= this.maxTimeMilliseconds) {
            clearInterval(this.stopwatchInterval);
            this.elapsedTime = this.maxTimeMilliseconds;
            timeIsUpMessageElement.style.display = 'block';
        } else {
            timeIsUpMessageElement.style.display = 'none';
        }

        const stopwatchElementMinutes = document.getElementById('stopwatchDisplayMinutes');
        const stopwatchElementSeconds = document.getElementById('stopwatchDisplaySeconds');
        const stopwatchElementMilliseconds = document.getElementById('stopwatchDisplayMilliseconds');
        document.getElementById('stopwatchPrefix').textContent = 'Timer:';
        
        const minutes = Math.floor(this.elapsedTime / 60000);
        const seconds = Math.floor((this.elapsedTime % 60000) / 1000);
        const milliseconds = Math.floor((this.elapsedTime % 1000) / 10);
        
        stopwatchElementMinutes.textContent = `${minutes.toString().padStart(1, '0')}:`;
        stopwatchElementSeconds.textContent = `${seconds.toString().padStart(2, '0')}`;
        stopwatchElementMilliseconds.textContent = `.${milliseconds.toString().padStart(2, '0')}`;
    }

    updateStopwatch(running, newElapsedTime) {
        clearInterval(this.stopwatchInterval);
        if (running) {
            let startTime = new Date().getTime() - newElapsedTime;
            this.stopwatchInterval = setInterval(() => {
                this.elapsedTime = new Date().getTime() - startTime;
                this.displayStopwatch();
            }, 10);
        } else {
            this.elapsedTime = newElapsedTime;
            this.displayStopwatch();
        }
    }
}
