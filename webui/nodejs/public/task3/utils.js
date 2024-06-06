// Utility Functions for drawing on the canvas

import { config } from '../config.js';

/**
 * Changes the canvas size based on the window size.
 * @param {HTMLCanvasElement} canvas - The canvas to resize.
 * @returns {void}
 */
export function changeCanvasSize(canvas) {
    // Set the canvas size dynamically based on the window size
    const size = Math.min(window.innerWidth * 0.70, window.innerHeight * 0.70);
    canvas.width = size;
    canvas.height = size;
}

/**
 * Converts logical coordinates to canvas pixels.
 * @param {HTMLCanvasElement} canvas - The canvas to draw on.
 * @param {number} x - The x-coordinate in the logical system.
 * @param {number} y - The y-coordinate in the logical system.
 * @returns {Object} The canvas coordinates { canvasX, canvasY }.
 */
export function coordinatesToCanvasPixels(canvas, x, y) {
    const canvasX = ((x - config.task3.coordinateRange.minX) / (config.task3.coordinateRange.maxX - config.task3.coordinateRange.minX)) * canvas.width;
    const canvasY = canvas.height - ((y - config.task3.coordinateRange.minY) / (config.task3.coordinateRange.maxY - config.task3.coordinateRange.minY)) * canvas.height;
    return { canvasX, canvasY };
}

/**
 * Checks whether a given point is inside one of ground truth circles with a given accuracy.
 * @param {number} x - The x-coordinate of the point.
 * @param {number} y - The y-coordinate of the point.
 * @param {Array} positionsGroundTruth - Array of groundTruth positions.
 * @returns {boolean} True if the point is inside the circle, false otherwise.
 */
export function isPointInsideGroundTruthRadius(x, y, positionsGroundTruth) {
    // Loop through each groundTruth position
    for (const position of positionsGroundTruth) {
        // Calculate the distance between the given point and the groundTruth position
        const distance = Math.sqrt(Math.pow(x - position.x, 2) + Math.pow(y - position.y, 2));
        // If the distance is less than or equal to the flower accuracy, the point is inside the circle
        if (distance <= config.task3.requiredAccuracy) {
            return true;
        }
    }
    // If the loop completes without finding a point inside the circle, return false
    return false;
}


/**
 * Draws the field background.
 * @param {HTMLCanvasElement} canvas - The canvas to draw on.
 */
export function drawField(canvas) {
    changeCanvasSize(canvas);
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = 'gainsboro';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (config.task3.drawRobot) {
        // Initially draw the robot at starting position
        drawRobot(canvas, 0, 0.2, true);
    }
}

export function drawFlowerGroundTruth(canvas, x, y) {
    let { canvasX, canvasY } = coordinatesToCanvasPixels(canvas, x, y);
    // Assuming the outer circle's radius in the coordinate system is the accuracy defined in config
    const outerCircleRadius = (config.task3.requiredAccuracy / (config.task3.coordinateRange.maxX - config.task3.coordinateRange.minX)) * canvas.width;
    const ctx = canvas.getContext('2d');
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 5; // Adjust the line width as needed
    ctx.beginPath();
    ctx.arc(canvasX, canvasY, outerCircleRadius, 0, 2 * Math.PI);
    ctx.stroke();
}

/**
 * Draws a 'X' at specified field coordinates.
 * The color of the flower is green if the flower is inside a ground truth radius, red otherwise.
 * @param {HTMLCanvasElement} canvas - The canvas to draw on.
 * @param {number} x - The x-coordinate in the field coordinate system.
 * @param {number} y - The y-coordinate in the field coordinate system.
 * @param {Array} positionsGroundTruth - Array of groundTruth positions to check against.
 */
export function drawX(canvas, x, y, positionsGroundTruth) {
    let { canvasX, canvasY } = coordinatesToCanvasPixels(canvas, x, y);

    // Calculate the radius of the 'X' relative based on the canvas size
    const scaleFactor = Math.min(canvas.width, canvas.height) * 0.01;
    const radius = scaleFactor * (config.task3.positionXSize / (config.task3.coordinateRange.maxX - config.task3.coordinateRange.minX));

    // Draw the 'X'
    const ctx = canvas.getContext('2d');
    if (isPointInsideGroundTruthRadius(x, y, positionsGroundTruth)) {
        ctx.strokeStyle = 'green';
    } else {
        ctx.strokeStyle = 'red';
    }
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(canvasX - radius, canvasY - radius);
    ctx.lineTo(canvasX + radius, canvasY + radius);
    ctx.moveTo(canvasX + radius, canvasY - radius);
    ctx.lineTo(canvasX - radius, canvasY + radius);
    ctx.stroke();
}

/**
 * Draws the robot at specified field coordinates.
 * @param {HTMLCanvasElement} canvas - The canvas to draw on.
 * @param {number} x - The x-coordinate in the field coordinate system.
 * @param {number} y - The y-coordinate in the field coordinate system.
 */
export function drawRobot(canvas, x, y, initialRobotPosition = false) {
    // don't draw robot if disabled in config
    if (config.task3.drawRobot === false) {
        return;
    }

    const ctx = canvas.getContext('2d');
    const { canvasX, canvasY } = coordinatesToCanvasPixels(canvas, x, y);
    
    // Load the robot image
    const robotImage = new Image();
    robotImage.src = '../images/robot.png';

    // Draw the image once it is loaded
    robotImage.onload = function() {
        // Calculate the robot size relative to the canvas size
        const robotWidth = canvas.width * 0.15;
        const robotHeight = canvas.height * 0.15;
        
        // Draw the robot image centered on the logical coordinates
        ctx.drawImage(robotImage, canvasX - robotWidth / 2, canvasY - robotHeight / 2, robotWidth, robotHeight);

        if (initialRobotPosition) {
            // Draw the "Start" label above the robot
            ctx.font = '24px Arial'; // Set font size and family
            ctx.fillStyle = 'black'; // Set text color
            ctx.textAlign = 'center'; // Center the text horizontally
            ctx.fillText('START', canvasX, canvasY - robotHeight / 2 - 10); // Position text above the robot
        }
    };
}