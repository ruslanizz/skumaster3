new Vue({
    el:'#analyticsapp',
    data: {
        sortParam: '',
        capsules_data: [],
        season_data: [],
        },

    created() {
        const vm=this;
        axios.get('/api/analytics/',
        {params: {season: season_number}})
        .then(function(response){

        vm.capsules_data = response.data
        }),

        axios.get('/api/analytics_season/',
        {params: {id: season_number}})
        .then(function(response){

        vm.season_data = response.data
        })

    },

    filters: {
    // Format summ with spaces between thousands
        format: val => `${val}`.replace(/(\d)(?=(\d{3})+([^\d]|$))/g, '$1 ')
    },
    computed: {
        sortedCapsulesData: function() {
            return this.capsules_data.sort(sortByCapsuleFirstletters);
                }
                }

    });

var sortByCapsuleFirstletters = function(d1, d2) {return (d1.capsule_firstletters > d2.capsule_firstletters) ? 1 : -1;};


