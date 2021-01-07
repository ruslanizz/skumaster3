new Vue({
    el:'#capsulesapp',
    data: {
        sortParam: '',
        capsules_data: []

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
