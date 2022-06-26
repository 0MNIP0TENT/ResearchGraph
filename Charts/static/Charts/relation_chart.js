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
function getRandomColorHex() {
  var hex = "0123456789ABCDEF",
  color = "#";
  for (var i = 1; i <= 6; i++) {
    color += hex[Math.floor(Math.random() * 16)];
  }
      return color;
}

var chart = new Chart("canv", {
  type: "bar",
  data: {
    datasets: [{
      labels: null,
      backgroundColor : [
        getRandomColorHex(),
        getRandomColorHex(),
        getRandomColorHex(),
        getRandomColorHex(),
        getRandomColorHex()
      ],

    }], 
  },
  options: {
    title: {
      display: true,
      text: '# of edges',
    },
   legend: {
        display: false
    },
    tooltips: {
        callbacks: {
           label: function(tooltipItem) {
                  return tooltipItem.yLabel;
           }
        }
    }
}
  
});
