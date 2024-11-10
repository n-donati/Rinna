'use strict';

/* Chart.js docs: https://www.chartjs.org/ */

window.chartColors = {
	green: '#ff651d',
	gray: '#a9b5c9',
	text: '#252930',
	border: '#e7e9ed'
};

/* Random number generator for demo purpose */
var randomDataPoint = function(){ return Math.round(Math.random()*10000)};


//Chart.js Line Chart Example 

var lineChartConfig = {
    type: 'line',
    data: {
        labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
       
        datasets: [{
            label: 'Esta semana',
            fill: false,
            backgroundColor: window.chartColors.green,
            borderColor: window.chartColors.green,
            data: [92, 92.5, 93, 93.2, 93.5, 93.8, 94],
        }, {
            label: 'Semana pasada',
            borderDash: [3, 5],
            backgroundColor: window.chartColors.gray,
            borderColor: window.chartColors.gray,
           
            data: [97, 96, 95, 94, 93, 92.5, 92],
            fill: false,
        }]
    },
    options: {
        responsive: true,  
        aspectRatio: 1.5,
       
        legend: {
            display: true,
            position: 'bottom',
            align: 'end',
        },
       
        title: {
            display: true,
            text: 'Porcentaje por día de la semana',
           
        },
        tooltips: {
            mode: 'index',
            intersect: false,
            titleMarginBottom: 10,
            bodySpacing: 10,
            xPadding: 16,
            yPadding: 16,
            borderColor: window.chartColors.border,
            borderWidth: 1,
            backgroundColor: '#fff',
            bodyFontColor: window.chartColors.text,
            titleFontColor: window.chartColors.text,
            callbacks: {
                label: function(tooltipItem, data) {
                    return tooltipItem.value + '%';
                }
            },
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                gridLines: {
                    drawBorder: false,
                    color: window.chartColors.border,
                },
                scaleLabel: {
                    display: false,
               
                }
            }],
            yAxes: [{
                display: true,
                gridLines: {
                    drawBorder: false,
                    color: window.chartColors.border,
                },
                scaleLabel: {
                    display: false,
                },
                ticks: {
                    beginAtZero: false,
                    userCallback: function(value, index, values) {
                        return value.toFixed(1) + '%';
                    },
                    min: 90,
                    max: 100
                },
            }]
        }
    }
};



// Chart.js Bar Chart Example 
var barChartConfig = {
    type: 'bar',
    data: {
        labels: ['0.5%', '0.4%', '0.3%', '0.2%', '0.1%'],
        datasets: [{
            label: 'Tasa de Interés Actual',
            backgroundColor: [
                window.chartColors.red,
                window.chartColors.blue,
                window.chartColors.green,
                window.chartColors.yellow,
                window.chartColors.purple
            ],
            borderColor: window.chartColors.border,
            borderWidth: 1,
            maxBarThickness: 16,
           
            data: [
                14,
                12,
                9,
                7,
                5
            ]
        }]
    },
    options: {
        responsive: true,
        aspectRatio: 1.5,
        legend: {
            position: 'bottom',
            align: 'end',
        },
        title: {
            display: true,
            text: 'Tasa de interés'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
            titleMarginBottom: 10,
            bodySpacing: 10,
            xPadding: 16,
            yPadding: 16,
            borderColor: window.chartColors.border,
            borderWidth: 1,
            backgroundColor: '#fff',
            bodyFontColor: window.chartColors.text,
            titleFontColor: window.chartColors.text,
            callbacks: {
                label: function(tooltipItem, data) {
                    return tooltipItem.value + '%';
                }
            }
        },
        scales: {
            xAxes: [{
                display: true,
                gridLines: {
                    drawBorder: false,
                    color: window.chartColors.border,
                },
            }],
            yAxes: [{
                display: true,
                gridLines: {
                    drawBorder: false,
                    color: window.chartColors.border,
                },
                ticks: {
                    beginAtZero: true,
                    max: 30,
                    callback: function(value) {
                        return value + '%';
                    }
                }
            }]
        }
    }
};


// Generate charts on load
window.addEventListener('load', function(){
	
	var lineChart = document.getElementById('canvas-linechart').getContext('2d');
	window.myLine = new Chart(lineChart, lineChartConfig);
	
	var barChart = document.getElementById('canvas-barchart').getContext('2d');
	window.myBar = new Chart(barChart, barChartConfig);
	

});	
	
