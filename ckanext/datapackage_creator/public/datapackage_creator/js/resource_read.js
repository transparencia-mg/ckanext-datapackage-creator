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
            extras: []
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
                this.package_id = res.data.resource.package_id
                this.resources.description = res.data.resource.description
                this.resources.format = res.data.resource.format
                this.resources.encoding = res.data.resource.encoding
                this.resources.type = res.data.resource.type
            })
        }
    }
})