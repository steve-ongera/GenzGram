
$(document).ready(function() {
    var chartData = {{ chart_data|safe }};

    // Transform chartData for Morris.js
    var morrisData = chartData.map(function(item) {
        return {
            y: item.year,
            a: item.total_students
        };
    });

    // Bar Chart
    Morris.Bar({
        element: 'bar-charts',
        data: morrisData,
        xkey: 'y',
        ykeys: ['a'],
        labels: ['Total Students'],
        barColors: ['#f43b48'],
        resize: true,
        redraw: true
    });
    
    // Line Chart
    Morris.Line({
        element: 'line-charts',
        data: morrisData,
        xkey: 'y',
        ykeys: ['a'],
        labels: ['Total Students'],
        lineColors: ['#f43b48'],
        lineWidth: '1px',
        resize: true,
        redraw: true
    });
});