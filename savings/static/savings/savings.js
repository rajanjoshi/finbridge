
document.addEventListener("DOMContentLoaded", function () {
  const charts = document.querySelectorAll("canvas[data-chart]");
  charts.forEach(canvas => {
    const dataset = JSON.parse(canvas.dataset.chart);
    new Chart(canvas, {
      type: "line",
      data: {
        labels: dataset.labels,
        datasets: [{
          label: "Contributions Over Time",
          data: dataset.data,
          borderColor: "rgba(0, 123, 255, 1)",
          fill: false,
          tension: 0.2
        }]
      }
    });
  });
});
