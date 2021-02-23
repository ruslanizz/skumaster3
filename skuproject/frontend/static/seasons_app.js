new Vue({
    el:'#seasonsapp',
    data: {
        seasons_data: [],
        baseinfo_data: [],
        sortParam : ''
           },

    created() {
        const vm=this;
        axios.get('/api/seasons/')
        .then(function(response){

        vm.seasons_data = response.data
        }),
        axios.get('/api/baseinfo/')
        .then(function(response){

        vm.baseinfo_data = response.data
        })
    },

    computed: {
        cleandate: function(){
            // Formatting date
            var just_date = this.baseinfo_data[0]["upload_date"].split('T')[0]
            var clean_date = just_date.split('-').reverse().join('.')
            return clean_date},

    sortedSeasonData: function() {
        switch(this.sortParam){
            case 'capsules_sellsumm_sold': return this.seasons_data.sort(sortByCapsulesSellsummSold).reverse();
            case 'capsules_income': return this.seasons_data.sort(sortByCapsulesIncome).reverse();
            default: return this.seasons_data.sort(sortByCapsulesSellsummSold).reverse();
            }
            }
    },

    filters: {
        // Format summ with spaces between thousands
        format: val => `${val}`.replace(/(\d)(?=(\d{3})+([^\d]|$))/g, '$1 ')
    }
    });

var sortByCapsulesSellsummSold = function(d1, d2) {return (d1.capsules_sellsumm_sold > d2.capsules_sellsumm_sold) ? 1 : -1;};
var sortByCapsulesIncome = function(d1, d2) {return (d1.capsules_income > d2.capsules_income) ? 1 : -1;};