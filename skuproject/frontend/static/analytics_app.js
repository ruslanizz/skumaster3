new Vue({
    el:'#analyticsapp',
    data: {
        capsules_data: [],
        },

    created() {
        const vm=this;
        axios.get('/api/analytics/',
        {params: {season: season_number}})
        .then(function(response){

        vm.capsules_data = response.data
        })
    },

    filters: {
    // Format summ with spaces between thousands
        format: val => `${val}`.replace(/(\d)(?=(\d{3})+([^\d]|$))/g, '$1 ')
    }

    });

