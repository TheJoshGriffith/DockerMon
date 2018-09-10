$(document).on('click', 'a', function (e) {
    e.preventDefault();
    res = jQuery.getJSON('http://' + window.location.host + '/api/get_container_stats/' + $(this).attr('href'), function(data) {
        display = "<table class='table'><tr><th>Time</th><th>CPU</th><th>Mem</th><th>NTX</th><th>NRX</th></tr>";
        var allindex = [];
        var cpu = [];
        var mem = {};
        var ntx = {};
        var nrx = {};
        $.each(data, function(index, row) {
            console.log(row);
            allindex.push(index);
            display += "<tr><td>";
            display += index;
            display += "</td><td>";
            display += row[0];
            cpu.push(row[0]);
            display += "</td><td>";
            display += row[1];
            mem[index] = row[1];
            display += "</td><td>";
            display += row[2];
            ntx[index] = row[2];
            display += "</td><td>";
            display += row[3];
            nrx[index] = row[3];
            display += "</td></tr>";
        });
        display += "</table><canvas id=\"myChart\" width=\"400\" height=\"400\"></canvas>\n";
        $('#content').html(display);
        var ctx = document.getElementById("myChart");
        var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: allindex,
        datasets: [{
            label: '# of CPU Ticks',
            data: cpu,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        },
        responsive: false
    }
});
    });
    console.log(res);
});