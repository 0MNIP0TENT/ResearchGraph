var xValues = [];
var yValues = [];
var barColors = [];
var backgroundColor = [];

function lick(data) { 
  chart.data.labels = [];
  chart.data.datasets[0].data = [];
  chart.update();
  var input = document.getElementById("select_box").value;
    var props = Object.keys(data[input]);
    var valuesArray = Object.values(data[input]);
    for(var prop = 0; prop < props.length; prop++) {
      chart.data.labels.push(props[prop]);
      backgroundColor.push(getRandomColorHex());
    }
   
    for(var value = 0; value < valuesArray.length; value++) {
      chart.data.datasets[0].data.push(valuesArray[value]);
    }
    chart.update();
}
function getRandomColorHex() {
  var hex = "0123456789ABCDEF",
  color = "#";
  for (var i = 1; i <= 6; i++) {
    color += hex[Math.floor(Math.random() * 16)];
  }
      return color;
}

chart = new Chart(document.getElementById("canv"), {
    type: 'pie',
    data: {
      labels: [],
      datasets: [{
	backgroundColor: backgroundColor,
      }]
    },
    options: {
      title: {
        display: true,
        text: 'Out Edge Relations'
      }
    }
});
