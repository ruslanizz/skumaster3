Vue.component('sizeschart', {

  props:{'sizes_list': Array,
         'labels_list': Array,
         'mychartid': String},

  data: function () {
    return {
      sizesChartData : {
        type: 'line',

        data: {
            labels:this.labels_list,
            datasets:[{
                label: 'Продано',
                data: this.sizes_list,
                backgroundColor: ['rgba(0, 0,0,0)'],
                borderColor: ['rgba(255,255,255,1)'],
                borderWidth: 3,
                pointBorderColor :'rgba(255,255,255,1)'
            }]
        },

        options: {
            responsive: false,
            animation: {duration: 0},
            layout: {
                    padding: {
                        left: 0,
                        right: 0,
                        top: 0,
                        bottom: 0
                    }
                },

        legend: {
                display: false,
                },

        scales: {
            xAxes: [{
                type: 'category',
                scaleLabel:{display: false,
                            labelString: 'Размер',
                            padding : 2,
                            fontColor: 'rgba(255,255,255,1)'},
                gridLines: {
                  display: true,
                  zeroLineColor: 'rgba(255,255,255,1)',
                  color:'rgba(255,255,255,1)',
                  drawBorder: true,
                  drawOnChartArea: false,
                  drawTicks: false,
                  zeroLineWidth: 3,
                  drawBorder: true,
                  },
                ticks: {fontColor: 'rgba(255,255,255,1)',
                        padding: 5,}
                  }],
            yAxes: [{
                  scaleLabel:{display: false,
                            labelString: 'Шт.',
                            padding : 1,
                            fontColor: 'rgba(255,255,255,1)'},
                  gridLines: {
                  display: true,
                  color: 'rgba(255,255,255,1)',
                  zeroLineColor: 'rgba(255,255,255,1)',
                  drawBorder: true,
                  drawOnChartArea: false,
                  drawTicks: false,
                  zeroLineWidth: 1
                },
                ticks: {
                    fontColor: 'rgba(255,255,255,1)',
                    beginAtZero: false,
                    display: true,
                    padding: 5,

                    precision: 0
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
  },

  mounted() {
      this.createChart(this.mychartid, this.sizesChartData);
    },

    template: '<canvas v-bind:id="mychartid"></canvas>'

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
    // Format summ with spaces between thousands
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
                case 'total_rating': return this.capsules_data.sort(sortByTotalRating);
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
var sortByTotalRating = function(d1, d2) {return (d1.rating_total > d2.rating_total) ? 1 : -1;};