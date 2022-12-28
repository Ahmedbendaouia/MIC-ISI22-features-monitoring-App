var ctxL = document.getElementById("image_proccess_1").getContext('2d');
var myLineChart = new Chart(ctxL, {
    type: 'line',
    data: {
        labels: ["10", "20", "30", "40", "50", "60", "70"],
        datasets: [{
                label: "VX",
                data: [65, 59, 80, 81, 56],
                backgroundColor: [
                    'rgba(105, 0, 132, .2)',
                ],
                borderColor: [
                    'rgba(200, 99, 132, .7)',
                ],
                borderWidth: 2
            },
            {
                label: "VZ",
                data: [28, 48, 40, 19, 86, 27, 90],
                backgroundColor: [
                    'rgba(0, 137, 132, .2)',
                ],
                borderColor: [
                    'rgba(0, 10, 130, .7)',
                ],
                borderWidth: 2
            },
            {
                label: "VY",
                data: [40, 76, 88, 55, 35, 89, 64],
                backgroundColor: [
                    'rgba(0, 124, 12, .2)',
                ],
                borderColor: [
                    'rgba(0, 15, 90, .7)',
                ],
                borderWidth: 2
            }
        ]
    },
    options: {
        responsive: true
    }
});