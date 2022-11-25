var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vue-app',
    data: {
        file: null,
        package_id: '',
        fields: [],
        name: '',
        description: '',
        format: '',
        show_fields: true,
        inference: null,
        resource: null,
        current_field: [],
        has_error: false,
        error_summary: '',
        errors: {},
        typeOptions: [
            'integer',
            'string',
            'number',
            'boolean',
            'object',
            'array',
            'date',
            'time',
            'datetime',
            'year',
            'yearmonth',
            'duration',
            'geopoint',
            'geojson',
            'any',
        ],
        defaultFormatOptions: [
            'default'
        ],
        stringFormatOptions: [
            'default',
            'email',
            'uri',
            'binary',
            'uuid'
        ],
        booleanOptions: [
            {
                'text': 'NÃO',
                'value': false
            },
            {
                'text': 'SIM',
                'value': true
            }
        ]
    },
    computed: {
        isDataResource() {
            try {
                console.log(this.inference != null)
                console.log(this.inference.metadata.profile === 'data-resource')
            } catch(ex){
            }
            return this.inference != null && this.inference.metadata.profile === 'data-resource'
        }
    },
    mounted () {
        this.package_id = this.$refs.packageName.value
    },
    methods: {
        uploadFile() {
            this.file = this.$refs.file.files[0]
            this.submitFile()
        },
        submitFile() {
            const formData = new FormData()
            formData.append('file', this.file)
            const headers = { 'Content-Type': 'multipart/form-data' }
            axios.post("/datapackage-creator/inference", formData, { headers }).then((res) => {
                this.inference = res.data
                try {
                    this.fields = res.data.metadata.schema.fields
                } catch (error) {
                    this.fields = []
                }
            })
        },
        editMetadata(field) {
            this.current_field = field
            this.show_fields = false
        },
        getFormatOptions(type) {
            if(type === 'string') {
                return this.stringFormatOptions
            } else {
                return this.defaultFormatOptions
            }
        },
        saveMetadata(field) {
            this.current_field = null
            this.show_fields = true
        },
        saveResource() {
            const formData = new FormData()
            formData.append('upload', this.file)
            const headers = { 'Content-Type': 'multipart/form-data' }
            formData.append('package_id', this.package_id)
            formData.append('description', this.description)
            formData.append('format', this.format)
            formData.append('metadata', JSON.stringify(this.fields))
            axios.post("/datapackage-creator/save-resource", formData, { headers }).then((res) => {
                this.has_error = res.data.has_error
            })
        },
        deleteResource(field) {

        }
    }
})