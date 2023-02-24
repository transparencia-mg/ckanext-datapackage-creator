var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vue-app',
    data: {
        package_id: '',
        resource_index: 1,
        success_message: '',
        allowed_add_resource: true,
        allowed_publish: false,
        settings: null,
        loading_message: 'Loading...',
        loading: false,
        package: {},
        file_icons: {
            pdf: 'pdf.png',
            jpg: 'jpg.png',
            jpeg: 'jpg.png',
            png: 'png.png',
            doc: 'doc.png',
            docx: 'doc.png',
            json: 'json.png',
            txt: 'txt.png',
            rar: 'rar.png',
            zip: 'zip.png'
        },
        resources: [
            {
                id: '',
                index: 1,
                file: null,
                show: false,
                fields: [],
                name: '',
                title: '',
                description: '',
                format: '',
                type: '',
                encoding: '',
                show_fields: true,
                inference: null,
                current_field: [],
                has_error: false,
                error_summary: [],
                errors: {},
                extras: [],
                file_icon: 'default.png'
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
            'any'
        ],
        dataTypeFieldOptions: [
            'date',
            'time',
            'datetime',
            'year',
            'yearmonth'
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
                name: 'Maximum / Minimum'
            },
            {
                value: 'length',
                name: 'Maximum Length / Minimum Length'
            },
            {
                value: 'pattern',
                name: 'Pattern'
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
            this.getResource(resourceId)
        } else {
            this.getPackage()
        }
        axios.get('/datapackage-creator/show-settings').then(res => {
            this.settings = res.data
        })
    },
    methods: {
        getPackage() {
            const url = `/datapackage-creator/show-datapackage/${this.package_id}`
            axios.get(url).then(res => {
                this.package.title = res.data.package.title
                this.package.name = res.data.package.name
                this.package.notes = res.data.package.notes
                this.package.license = res.data.package.license_id
                this.package.tags = res.data.package.tag_string
                this.package.organization = res.data.package.owner_org
                this.package.visibility = res.data.package.private
                this.package.source = res.data.package.url || ''
                this.package.version = res.data.package.version
                let datapackage = JSON.parse(res.data.datapackage.data_json)
                this.package.contributors = datapackage.contributors
                this.package.tags = datapackage.tags
                this.package.frequency = datapackage.frequency
                this.package.tags = datapackage.tags
                this.package.metadata = datapackage
            })
        },
        getResource(resourceId) {
            const url = `/datapackage-creator/show-datapackage-resource/${resourceId}`
            this.loading = true
            axios.get(url).then(res => {
                this.loading = false
                this.package_id = res.data.resource.package_id
                this.resources = []
                this.resources.push(JSON.parse(res.data.datapackage_resource.data))
                this.resources[0].id = resourceId
                this.getPackage()
            }).catch(() => {
                this.loading = false
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
            this.loading = true
            axios.post("/datapackage-creator/inference", formData, { headers })
                .then((res) => {
                    this.loading = false
                    if(res.data.has_error) {
                        resource.error_summary = [res.data.error_summary]
                        resource.has_error = true
                    } else {
                        resource.show = true
                        resource.error_summary = []
                        resource.has_error = false
                        resource.inference = res.data
                        console.log(res.data)
                        resource.name = resource.inference.metadata.name
                        resource.encoding = resource.inference.metadata.encoding
                        resource.format = resource.inference.metadata.format
                        resource.type = resource.inference.metadata.profile
                        try {
                            resource.fields = res.data.metadata.schema.fields
                        } catch (error) {
                            resource.fields = []
                        }
                    }
                })
                .catch(() => {
                    this.loading = false
                    resource.has_error = true
                    resource.error_summary = ['Unable to upload the file']
                    setTimeout(() => {
                        resource.has_error = false
                        resource.error_summary = ['']
                    }, 8000)
                })
        },
        editMetadata(resource, field) {
            resource.current_field = field
            resource.show_fields = false
        },
        getFormatOptions(type) {
            if(type === 'string') {
                return this.stringFormatOptions
            } else {
                return this.defaultFormatOptions
            }
        },
        checkMetadata(field) {
            const closeButton = this.$refs[`modal_close_${field.name}`][0]
            let valid = true
            field.extras.forEach(extra => {
                if(extra.type == 'enum' || extra.type == 'pattern') {
                    if(extra.value === '') {
                        extra.pattern_error = true
                        valid = false
                    } else {
                        extra.pattern_error = false
                    }
                } else if(extra.type == 'max_min') {
                    if(!extra.min) {
                        extra.min_error = true
                        valid = false
                    } else {
                        extra.min_error = false
                    }
                    if(!extra.max) {
                        extra.max_error = true
                        valid = false
                    } else {
                        extra.max_error = false
                    }
                } else if(extra.type == 'length') {
                    if(!extra.min_length) {
                        extra.min_length_error = true
                        valid = false
                    } else {
                        extra.min_length_error = false
                    }
                    if(!extra.max_length) {
                        extra.max_length_error = true
                        valid = false
                    } else {
                        extra.max_length_error = false
                    }
                }
            })
            if(valid) {
                closeButton.click()
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
            formData.append('name', resource.name)
            formData.append('title', resource.title)
            formData.append('description', resource.description)
            formData.append('format', resource.format)
            formData.append('encoding', resource.encoding)
            formData.append('type', resource.type)
            formData.append('id', resource.id)
            formData.append('metadata', JSON.stringify(resource))
            this.loading = true
            axios.post("/datapackage-creator/save-resource", formData, { headers }).then((res) => {
                this.loading = false
                resource.has_error = res.data.has_error
                resource.errors = res.data.errors
                resource.error_summary = []
                if (res.data.error_summary) {
                    for(const property in res.data.error_summary) {
                        resource.error_summary.push(`${property}: ${res.data.error_summary[property]}`)
                    }
                    setTimeout(() => {
                        resource.has_error = false
                        resource.errors = []
                    }, 5000)
                } else {
                    resource.id = res.data.resource.id
                    this.success_message = 'Successfully saved resource!'
                    setTimeout(() => {
                        this.success_message = ''
                    }, 5000)
                }
            }).catch(() => {
                this.loading = false
            })
        },
        deleteResource(resource) {
            if(resource.id) {
                this.loading = true
                axios.delete(`/datapackage-creator/delete-resource/${resource.id}`).then((res) => {
                    this.loading = false
                    if(!this.allowed_add_resource) {
                        window.location = `/dataset/${this.package_id}`
                    }
                    this.resources = this.resources.filter(function(value, index, arr){
                        return value.index != resource.index
                    })
                }).catch(() => {
                    this.loading = false
                    resource.has_error = true
                    resource.error_summary = ['Unable to delete the resource']
                })
            } else {
                this.resources = this.resources.filter(function(value, index, arr){
                    return value.index != resource.index
                })
            }
        },
        addResource() {
            this.resource_index += 1
            this.resources.forEach(resource => {
                resource.show = false
            })
            this.resources.push(
                {
                    id: '',
                    index: this.resource_index,
                    show: false,
                    file: null,
                    fields: [],
                    name: '',
                    title: '',
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
                max_length: 0,
                min_length: 0,
                value: '',
                min_error: false,
                max_error: false,
                min_length_error: false,
                max_length_error: false,
                pattern_error: false
            })
        },
        deleteMetadata(field, extra) {
            field.extras = field.extras.filter(function(value, index, arr){
                return value.type != extra.type
            })
        },
        addResourceMetadadata(resource) {
            resource.extras.push({
                title: '',
                value: ''
            })
        },
        validate(){
            this.$refs["success-message"].scrollIntoView({ behavior: "smooth" })
            this.allowed_publish = true
            this.resources.forEach(resource => {
                this.saveResource(resource)
            })
        },
        publishPackage() {
            let ok = true
            if(!this.packageValid) {
                ok = confirm('One or more invalid resources, do you want to publish anyway?')
            }
            if(ok) {
                const formData = new FormData()
                const headers = { 'Content-Type': 'multipart/form-data' }
                formData.append('id', this.package_id)
                formData.append('metadata', JSON.stringify(this.package))
                console.log(this.package)
                this.loading = true
                axios.post("/datapackage-creator/publish-package", formData, { headers }).then((res) => {
                    this.loading = false
                    window.location = `/dataset/${this.package_id}`
                }).catch(() => {
                    this.loading = false
                })
            }
        },
        isDateType(field) {
            return this.dataTypeFieldOptions.includes(field.type)
        },
        changeType(field) {
            let isDate = this.dataTypeFieldOptions.includes(field.type)
            if(!isDate) {
                field.format = 'default'
            } else {
                field.format = ''
            }
        },
        isReadonly(field_name) {
            let readonly = false
            if(this.settings != null && this.settings.resource && this.settings.resource.readonly) {
                readonly = this.settings.resource.readonly.includes(field_name)
            }
            return readonly
        },
        isRequired(field_name) {
            let required = false
            if(this.settings != null && this.settings.resource && this.settings.resource.required) {
                required = this.settings.resource.required.includes(field_name)
            }
            return required
        },
        filterMetadataTypeOptions(field) {
            return this.metadataTypeOptions.filter(function(value, index, arr){
                if(value.value == 'pattern') {
                    return field.type == 'string'
                } else if(value.value == 'length') {
                    return ['array', 'string', 'object'].includes(field.type)
                } else if(value.value == 'max_min') {
                    return ['integer', 'number', 'date', 'time', 'datetime', 'year', 'yearmonth'].includes(
                        field.type
                    )
                }
                return true
            })
        },
        getFileIcon(format) {
            let icon =  this.file_icons[format]
            return icon ? icon : 'default.png'
        }
    },
    computed: {
        packageValid() {
            return this.allowed_publish && this.resources.reduce(function(accumulator, curValue) {
                return accumulator && !curValue.has_error
            }, true)
        }
    }
})