new Vue({
    el:'#skuapp',
    data: {
        sortParam: '',
        sku_data: [],
        checked: false,
        checked2: false,

           },

    created() {
        const vm=this;
        axios.get('/api/sku/',
        {params: {capsule: capsule_number}})
        .then(function(response){

        vm.sku_data = response.data
        })


    },

    methods: {
        cols_quantity: function (index) {
            return this.sku_data[index]["sizes_grid"][0].length;
                },

        size_fit_to_column: function (row,size){
//      Если двойной размер типа 110*116, то он не помещается в карточку. Сокращаем его до вида 110*, если больше 4 колонок в строке
            let postn = size.indexOf("*");
//            console.log('row:'+row+' length:'+row.length+' postn:'+postn);
            if (postn != -1 && row.length>4) {
//                console.log('NEED REDUCE');
                return size.slice(0,postn+1)}
            else {
//            console.log('LEAVE AS IS');
            return size};
        },


        just_instock_rows: function (full_grid){
        // Убираем из таблицы строки, в которой нет ни одного "INSTOCK"
            let newgrid = [];

            for (let row of full_grid) {
                let instock_counter = 0;
                for (let col of row) {
                    if (col[1]=='INSTOCK'){
                        instock_counter +=1;
                    }
                };
                if (instock_counter > 0) {
                    newgrid.push(row);
                    }

            } ;
            return newgrid
        },


        it_has_instock: function(full_grid){

            let instock_counter = 0;

            for (let row of full_grid) {

                for (let col of row) {
                    if (col[1]=='INSTOCK'){
                        instock_counter +=1;
                         }
                };
            };
            if (instock_counter > 0) {
                return true;
                 }
             else {
                return false;
            };

        }



    },

    filters: {
    // Выводим сумму в формате с пробелами между разрядами
        format: val => `${val}`.replace(/(\d)(?=(\d{3})+([^\d]|$))/g, '$1 ')
    },

    computed: {
        sortedSkuData: function() {
            switch(this.sortParam){
                case 'sku_firstletters': return this.sku_data.sort(sortBySkuFirstletters);
                case 'sizes_sellsumm_sold': return this.sku_data.sort(sortBySizesSellsummSold).reverse();
                case 'sizes_income': return this.sku_data.sort(sortBySizesIncome).reverse();
                case 'sizes_costsumm_instock': return this.sku_data.sort(sortBySizesCostsummInstock).reverse();
                case 'margin_percent': return this.sku_data.sort(sortByMarginPercent).reverse();

                default: return this.sku_data.sort(sortBySkuFirstletters);
                }
                },

//        cols_quantity: function (index) {
//            return this.sku_data[index]["sizes_grid"][0].length;
//                },

        rows_quantity: function(){
            let counter=0;
            for (let i of this.sku_data["sizes_grid"]){
            counter += 1;
            };

            return counter;
                },

                }





    });

var sortBySkuFirstletters = function(d1, d2) {return (d1.sku_firstletters > d2.sku_firstletters) ? 1 : -1;};
var sortBySizesSellsummSold = function(d1, d2) {return (d1.sizes_sellsumm_sold > d2.sizes_sellsumm_sold) ? 1 : -1;};
var sortBySizesIncome = function(d1, d2) {return (d1.sizes_income > d2.sizes_income) ? 1 : -1;};
var sortBySizesCostsummInstock = function(d1, d2) {return (d1.sizes_costsumm_instock > d2.sizes_costsumm_instock) ? 1 : -1;};
var sortByMarginPercent = function(d1, d2) {return (d1.margin_percent > d2.margin_percent) ? 1 : -1;};

