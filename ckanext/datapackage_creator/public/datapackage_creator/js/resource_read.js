var appElem = document.getElementById('#vue-app')
if(appElem) {
    var app = new Vue({
        delimiters: ['[[', ']]'],
        el: '#vue-app',
        data: {
            resource: {
                id: '',
                index: 1,
                file: null,
                show: true,
                fields: [],
                name: '',
                description: '',
                format: '',
                type: '',
                encoding: '',
                show_fields: true,
                inference: null,
                resource: null,
                current_field: [],
                has_error: false,
                error_summary: [],
                errors: {},
                extras: [],
                package: {}
            }
        },
        mounted () {
            this.resource.id = this.$refs.resourceId.value
            this.getResource()
        },
        methods: {
            getResource() {
                const url = `/datapackage-creator/show-datapackage-resource/${this.resource.id}`
                axios.get(url).then(res => {
                    this.resource = JSON.parse(res.data.datapackage_resource.data)
                    this.resource.package = res.data.package
                })
            }
        }
    })
}