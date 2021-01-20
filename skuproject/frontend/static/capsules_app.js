Vue.component('sizeschart', {
  props:['sizes_dict'],
  data: function () {
    return {
      sizesChartData : {
  type: 'line',
  data: {
//    labels: ['122', '128', '134', '140', '146', '152', '158', '164'],
    datasets: [
      { // another line graph
        label: 'Продано',
//        data: [4.8, 12.1, 12.7, 6.7, 139.8, 116.4, 50.7, 49.2],
        data: this.sizes_dict,
        backgroundColor: [
          'rgba(0, 0,0,0)', // Green
        ],
        borderColor: [
          'rgba(255,255,255,1)',
        ],
        borderWidth: 3,
        pointBorderColor :'rgba(255,255,255,1)'
      }
    ]
  },
  options: {
    responsive: false,
    animation: {duration: 0},
    layout: {padding: 0},
    legend: {
            display: false},
    scales: {
        xAxes: [{
            type: 'category',
            labels: ['122', '128', '134', '140', '146', '152', '158', '164'],
            gridLines: {
              display: false,
              zeroLineColor: 'rgba(255,255,255,1)',
              color:'rgba(255,255,255,1)',
              zeroLineWidth: 3,
              drawBorder: true,
              },
            ticks: {fontColor: 'rgba(255,255,255,1)'}
              }],
        yAxes: [{
            gridLines: {
              display: false,
              color: 'rgba(219,219,219,0.3)',
              zeroLineColor: 'rgba(255,255,255,0.7)',
              drawBorder: false, // <---

              zeroLineWidth: 1
            },
            ticks: {
                beginAtZero: true,
                display: false
            }
        }]
    }
  }
}
    }
  },
  methods: {
  createChart(chartId, chartData) {
    const ctx = document.getElementById(chartId);
    const myChart = new Chart(ctx, {
      type: chartData.type,
      data: chartData.data,
      options: chartData.options,
    });
  },

  sizes_for_x_axis(){
  let values=[];
  for (var key in this.sizes_dict){
    values.push(key)
  };


    console.log(values);
    return values
  }





},
mounted() {
  this.createChart('sizes-chart', this.sizesChartData);
},

  template: '<canvas id="sizes-chart"></canvas>'
})



new Vue({
    el:'#capsulesapp',
    data: {
        sortParam: '',
        capsules_data: [],
        checked : false
        },

    created() {
        const vm=this;
        axios.get('/api/capsules/',
        {params: {season: season_number}})
        .then(function(response){

        vm.capsules_data = response.data
        })
    },
    filters: {
    // Выводим сумму в формате с пробелами между разрядами
        format: val => `${val}`.replace(/(\d)(?=(\d{3})+([^\d]|$))/g, '$1 ')
    },
    computed: {
        sortedCapsulesData: function() {
            switch(this.sortParam){
                case 'capsule_firstletters': return this.capsules_data.sort(sortByCapsuleFirstletters);
                case 'sku_sellsumm_sold': return this.capsules_data.sort(sortBySkuSellsummSold).reverse();
                case 'sku_costsumm_instock': return this.capsules_data.sort(sortBySkuCostsummInstock).reverse();
                case 'sku_income': return this.capsules_data.sort(sortBySkuIncome).reverse();
                case 'sku_margin_percent': return this.capsules_data.sort(sortBySkuMarginPercent).reverse();

                default: return this.capsules_data.sort(sortByCapsuleFirstletters);
                }
                }
                }

    });

var sortByCapsuleFirstletters = function(d1, d2) {return (d1.capsule_firstletters > d2.capsule_firstletters) ? 1 : -1;};
var sortBySkuSellsummSold = function(d1, d2) {return (d1.sku_sellsumm_sold > d2.sku_sellsumm_sold) ? 1 : -1;};
var sortBySkuCostsummInstock = function(d1, d2) {return (d1.sku_costsumm_instock > d2.sku_costsumm_instock) ? 1 : -1;};
var sortBySkuIncome = function(d1, d2) {return (d1.sku_income > d2.sku_income) ? 1 : -1;};
var sortBySkuMarginPercent = function(d1, d2) {return (d1.sku_margin_percent > d2.sku_margin_percent) ? 1 : -1;};
