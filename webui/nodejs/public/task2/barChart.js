import { config } from '../config.js';
import '../chartjs/chart.js';
import '../chartjs/annotation-plugin.js';

export default class BarChart {
    constructor(context) {
        this.context = context;
        this.chart = null;
    }

    createBarChart(groundTruthData) {
        let labels = this.getChartLabels(groundTruthData);
        const groundTruth = groundTruthData.map(item => item.plant_count);

        // Reverse to display the rows as they are in the field (right to left)
        if (config.task2.reverseRows) {
            labels.reverse();
            groundTruth.reverse();
        }

        const annotations = {};
        
        // Create annotations (red horizontal line) for each row's ground truth
        groundTruth.forEach((value, index) => {
            const annotationId = `groundTruth_${index + 1}`;
            annotations[annotationId] = {
                type: 'line',
                yMin: value,
                yMax: value,
                xMin: index - 0.5,
                xMax: index + 0.5,
                borderColor: 'rgb(255, 0, 0)',
                borderWidth: 5,
            };
        });

        this.chart = new Chart(this.context, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Reported number of plants per row',
                    data: [],
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            font: {
                                size: 48,
                            },
                            //stepSize: 1,
                        },
                    },
                    x: {
                        ticks: {
                            font: {
                                size: 48,
                            }
                        }
                    }
                },
                plugins: {
                    annotation: {
                        annotations: annotations
                    },
                    legend: {
                        display: false,
                        labels: {
                            font: {
                                size: 34,
                            }
                        }
                    },
                    htmlLegend: {
                        containerID: 'chart-legend-container',
                    },
                }
            },
            plugins: [this.htmlLegendPlugin],
        });
    }

    getChartLabels(countGroundTruth) {
        return countGroundTruth.map((item, index) => `Row ${index + 1}`);
    }

    updateChart(counts) {
        // Reverse to display the rows as they are in the field (right to left)
        if (config.task2.reverseRows) {
            counts.reverse();
        }
        this.chart.data.datasets[0].data = counts;
        this.chart.update();
    }

    resetChart() {
        if (!this.chart) {
            return;
        }
        const zeros = Array(this.chart.data.labels.length).fill(0);
        this.chart.data.datasets[0].data = zeros;
        this.chart.update();
    }

    getOrCreateLegendList(chart, id) {
        const legendContainer = document.getElementById(id);
        let listContainer = legendContainer.querySelector('ul');

        if (!listContainer) {
            listContainer = document.createElement('ul');
            listContainer.style.display = 'flex';
            listContainer.style.flexDirection = 'row';
            listContainer.style.margin = 0;
            listContainer.style.padding = 0;

            legendContainer.appendChild(listContainer);
        }

        return listContainer;
    }

    htmlLegendPlugin = {
        id: 'htmlLegend',
        afterUpdate: (chart, args, options) => {
            const ul = this.getOrCreateLegendList(chart, options.containerID);

            // Remove old legend items
            while (ul.firstChild) {
                ul.firstChild.remove();
            }

            // Reuse the built-in legendItems generator
            const items = chart.options.plugins.legend.labels.generateLabels(chart);

            items.push({
                datasetIndex: 1,
                hidden: false,
                text: 'Real number of plants per row',
                fontColor: '#666',
                fillStyle: 'rgba(255, 0, 0, 0.5)',
                strokeStyle: 'rgba(255, 0, 0, 1)',
                lineWidth: 2,
                borderRadius: 0,
            });

            items.forEach(item => {
                const li = document.createElement('li');
                li.style.alignItems = 'center';
                li.style.cursor = item.cursor ?? 'pointer';
                li.style.display = 'flex';
                li.style.flexDirection = 'row';
                li.style.marginLeft = '30px';

                li.onclick = () => {
                    const { type } = chart.config;
                    if (type === 'pie' || type === 'doughnut') {
                        // Pie and doughnut charts only have a single dataset and visibility is per item
                        chart.toggleDataVisibility(item.index);
                    } else {
                        chart.setDatasetVisibility(item.datasetIndex, !chart.isDatasetVisible(item.datasetIndex));
                    }
                    chart.update();
                };

                // Color box
                const boxSpan = document.createElement('span');
                boxSpan.style.background = item.fillStyle;
                boxSpan.style.borderColor = item.strokeStyle;
                boxSpan.style.borderWidth = item.lineWidth + 'px';
                boxSpan.style.borderStyle = 'solid';
                boxSpan.style.display = 'inline-block';
                boxSpan.style.flexShrink = 0;
                boxSpan.style.height = '34px';
                boxSpan.style.marginRight = '10px';
                boxSpan.style.width = '34px';

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

                li.appendChild(boxSpan);
                li.appendChild(textContainer);
                ul.appendChild(li);
            });
        }
    };
}
