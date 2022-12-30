var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#additional-app',
    data: {
        package_id: '',
        additionals: [],
        contributors: []
    },
    mounted () {
        this.package_id = this.$refs.packageId.value
        this.getPackage()
    },
    methods: {
        getPackage() {
            const url = `/datapackage-creator/show-datapackage/${this.package_id}`
            axios.get(url).then(res => {
                let data = JSON.parse(res.data.datapackage.data)
                this.additionals.push({
                    key: 'Frequency',
                    value: data.frequency
                })
                this.contributors = data.contributors
            })
        }
    }
})