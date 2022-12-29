var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vue-app',
    data: {
        package_id: '',
        resource_index: 1,
        success_message: '',
        allowed_add_resource: true,
        resources: [
            {
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
        ],
        typeFieldOptions: [
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
                'text': 'NO',
                'value': false
            },
            {
                'text': 'YES',
                'value': true
            }
        ],
        typeOptions: [
            {
                text: 'Select type',
                value: ''
            },
            {
                text: 'Tabular Data Resource',
                value: 'tabular-data-resource'
            },
            {
                text: 'Data Resource',
                value: 'data-resource'
            }
        ],
        metadataTypeOptions: [
            {
                value: '',
                name: 'Select'
            },
            {
                value: 'max_min',
                name: 'Max / Min'
            },
            {
                value: 'list',
                name: 'List'
            },
            {
                value: 'enum',
                name: 'Enum'
            }
        ],
        metadataResourceOptions: [
            {
                value: '',
                name: 'Select'
            },
            {
                value: 'mediatype',
                name: 'Media Type'
            },
            {
                value: 'bytes',
                name: 'Bytes'
            },
            {
                value: 'hash',
                name: 'Hash'
            },
            {
                value: 'sources',
                name: 'Sources'
            },
            {
                value: 'licenses',
                name: 'Licenses'
            }
        ]
    },
    mounted () {
        this.package_id = this.$refs.packageName.value
        let resourceId = this.$refs.resourceId.value
        if(resourceId) {
            this.allowed_add_resource = false
            this.resources[0].id = resourceId
            this.getResource()
        }
    },
    methods: {
        getResource() {
            const url = `/datapackage-creator/show-datapackage-resource/${this.resources[0].id}`
            axios.get(url).then(res => {
                this.package_id = res.data.resource.package_id
                this.resources[0].description = res.data.resource.description
                this.resources[0].format = res.data.resource.format
                this.resources[0].encoding = res.data.resource.encoding
                this.resources[0].type = res.data.resource.type
            })
        },
        isDataResource(resource) {
            return resource.type === 'data-resource'
        },
        uploadFile(resource) {
            resource.file = this.$refs[`file_${resource.index}`][0].files[0]
            this.submitFile(resource)
        },
        submitFile(resource) {
            const formData = new FormData()
            formData.append('file', resource.file)
            const headers = { 'Content-Type': 'multipart/form-data' }
            axios.post("/datapackage-creator/inference", formData, { headers })
                .then((res) => {
                    resource.error_summary = []
                    resource.inference = res.data
                    resource.name = resource.inference.metadata.name
                    resource.encoding = resource.inference.metadata.encoding
                    resource.format = resource.inference.metadata.format
                    resource.type = resource.inference.metadata.profile
                    try {
                        resource.fields = res.data.metadata.schema.fields
                    } catch (error) {
                        resource.fields = []
                    }
                })
                .catch(() => {
                    resource.error_summary = ['Unable to upload the file']
                })
        },
        editMetadata(resource, field) {
            resource.current_field = field
            resource.show_fields = false
            // let resourceModal = this.$refs[`modal_${resource.index}`]
            // let modalInstance = new bootstrap.Modal(resourceModal)
            // modalInstance.show()
        },
        getFormatOptions(type) {
            if(type === 'string') {
                return this.stringFormatOptions
            } else {
                return this.defaultFormatOptions
            }
        },
        saveMetadata(resource, field) {
            resource.current_field = null
            resource.show_fields = true
        },
        saveResource(resource) {
            const formData = new FormData()
            formData.append('upload', resource.file)
            const headers = { 'Content-Type': 'multipart/form-data' }
            formData.append('package_id', this.package_id)
            formData.append('description', resource.description)
            formData.append('format', resource.format)
            formData.append('encoding', resource.encoding)
            formData.append('type', resource.type)
            formData.append('id', resource.id)
            formData.append('metadata', JSON.stringify(resource.fields))
            axios.post("/datapackage-creator/save-resource", formData, { headers }).then((res) => {
                resource.has_error = res.data.has_error
                resource.errors = res.data.errors
                resource.error_summary = []
                if (res.data.error_summary) {
                    for(const property in res.data.error_summary) {
                        resource.error_summary.push(`${property}: ${res.data.error_summary[property]}`)
                    }
                }
                resource.id = res.data.resource.id
                if(!resource.has_error) {
                    this.success_message = 'Successfully saved resource!'
                    setTimeout(() => {
                        this.success_message = ''
                    }, 5000)
                }
            })
        },
        deleteResource(resource) {
            this.resources = this.resources.filter(function(value, index, arr){
                return value.index != resource.index
            })
        },
        addResource() {
            this.resource_index += 1
            this.resources.push(
                {
                    id: '',
                    index: this.resource_index,
                    show: true,
                    file: null,
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
                    errors: {}
                }
            )
        },
        toggleResource(resource) {
            resource.show = !resource.show
        },
        addMetadaData(field) {
            field.extras.push({
                type: '',
                max: 0,
                min: 0,
                title: '',
                value: ''
            })
        },
        addResourceMetadadata(resource) {
            resource.extras.push({
                title: '',
                value: ''
            })
        },
        publishPackage() {
            const formData = new FormData()
            const headers = { 'Content-Type': 'multipart/form-data' }
            formData.append('id', this.package_id)
            axios.post("/datapackage-creator/publish-package", formData, { headers }).then((res) => {
                this.success_message = 'Successfully published Package!'
                setTimeout(() => {
                    this.success_message = ''
                }, 5000)
            })
        }
    }
})