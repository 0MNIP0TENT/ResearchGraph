var xValues = [];
var yValues = [];
var barColors = [];

function lick(data) { 
var input = document.getElementById("select_box").value;
if(input in data) {
  chart.data.datasets[0].data.push(data[input]);
  chart.data.labels.push(input);

  chart.update();
  }
}

var chart = new Chart("canv", {
  type: "bar",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {}
});
