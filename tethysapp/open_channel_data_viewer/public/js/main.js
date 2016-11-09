var resize_chart;
resize_chart = function(){
    $(Highcharts.charts).each(function(i,chart){
        if(chart != undefined) {
            chart.reflow();
        }
    });
}

$(document).ready(function(){
//    $("#sediment-transport-tab").on("click", resize_chart);
//    $("#velocity-time").on("focus", resize_chart);
//    $("#depth-tab").on("click", resize_chart);
//    $("#flow-tab").on("click", resize_chart);
});