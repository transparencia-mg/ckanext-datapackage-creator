var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vue-app-package',
    data: {
        has_error: false,
        error_summary: [],
        contributor_index: 2,
        extra_index: 0,
        allowed_add_data: false,
        settings: null,
        form: {
            title: '',
            id: '',
            name: '',
            notes: '',
            organization: '',
            visibility: true,
            license: '',
            type: 'tabular-data-package',
            source: '',
            version: '',
            tags: '',
            contributors: [
                {
                    index: 1,
                    canDelete: false,
                    type: 'Publisher',
                    name: '',
                    email: '',
                    url: '',
                    editable: false,
                },
                {
                    index: 2,
                    canDelete: false,
                    type: 'Author',
                    name: '',
                    email: '',
                    url: '',
                    editable: true
                }
            ],
            frequency: '',
            extras: []
        },
        contributorTypeOptions: [
            '',
            'Publisher',
            'Author',
            'Contributor',
            'Maintainer',
            'Data Wrangler'
        ],
        visibilityOptions: [
            {
                text: 'Private',
                value: true
            },
            {
                text: 'Public',
                value: false
            }
        ],
        licenseOptions: [
            {
                value: '', text: 'Please select the license',
            },
            {
                value: "cc-by", text: "Creative Commons Atribuição"
            },
            {
                value: "cc-by", text: "Creative Commons Atribuição"
            },
            {
                value: "cc-by-sa", text: "Creative Commons Atribuição e Compartilhamento pela mesma Licença"
            },
            {
                value: "cc-zero", text: "Creative Commons CCZero"
            },
            {
                value: "cc-nc", text: "Creative Commons Não-Comercial (Qualquer)"
            },
            {
                value: "odc-odbl", text: "Licença Aberta para Bases de Dados (ODbL) do Open Data Commons"
            },
            {
                value: "gfdl", text: "Licença GNU para Documentação Livre"
            },
            {
                value: "odc-by", text: "Licença de Atribuição do Open Data Commons"
            },
            {
                value: "odc-pddl", text: "Licença e Dedicação ao Domínio Público do Open Data Commons (PDDL)"
            },
            {
                value: "notspecified", text: "Licença não especificada"
            },
            {
                value: "uk-ogl", text: "Open Government Licence do Reino Unido (OGL)"
            },
            {
                value: "other-open", text: "Outra (Aberta)"
            },
            {
                value: "other-at", text: "Outra (Atribuição)"
            },
            {
                value: "other-pd", text: "Outra (Domínio Público)"
            },
            {
                value: "other-closed", text: "Outra (Não Aberta)"
            },
            {
                value: "other-nc", text: "Outra (Não-Comercial)"
            }
        ],
        typeOptions: [
            {
                text: 'Tabular',
                value: 'tabular-data-package'
            },
            {
                text: 'Not Tabular',
                value: 'data-package'
            }
        ],
        frequencyOptions: [
            {
                value: '',
                name: 'Select'
            },
            {
                value: 'daily',
                name: 'Daily'
            },
            {
                value: 'weekly',
                name: 'Weekly'
            },
            {
                value: 'fortnightly',
                name: 'Fortnightly'
            },
            {
                value: 'monthly',
                name: 'Monthly'
            },
            {
                value: 'bi-monthly',
                name: 'Bi-monthly'
            },
            {
                value: 'quarterly',
                name: 'Quarterly'
            },
            {
                value: 'annual',
                name: 'Annual'
            },
            {
                value: 'on-demand',
                name: 'On Demand'
            }
        ]
    },
    mounted () {
        let userName = this.$refs.userName.value
        let userEmail = this.$refs.userEmail.value
        this.form.contributors[0].name = userName
        this.form.contributors[0].email = userEmail
        this.form.organization = this.$refs.organizationId.value
        this.form.id = this.$refs.packageId.value
        axios.get('/datapackage-creator/show-settings').then(res => {
            this.settings = res.data
        })
        if(this.form.id !== '') {
            this.getPackage()
        }
    },
    methods: {
        getPackage() {
            const url = `/datapackage-creator/show-datapackage/${this.form.id}`
            axios.get(url).then(res => {
                this.form.title = res.data.package.title
                this.form.name = res.data.package.name
                this.form.notes = res.data.package.notes
                this.form.license = res.data.package.license_id
                this.form.tags = res.data.package.tag_string
                this.form.organization = res.data.package.owner_org
                this.form.visibility = res.data.package.private
                this.form.source = res.data.package.url || ''
                this.form.version = res.data.package.version
                this.form.extras = res.data.package.extras
                let datapackage = JSON.parse(res.data.datapackage.data)
                this.form.contributors = datapackage.contributors
                this.form.frequency = datapackage.frequency
                this.form.tags = datapackage.tags
            })
        },
        slugifyTitle() {
            const slug = this.form.title.toString()
                .normalize('NFD')
                .replace(/[\u0300-\u036f]/g, '')
                .toLowerCase()
                .trim()
                .replace(/\s+/g, '-')
                .replace(/[^\w-]+/g, '')
                .replace(/--+/g, '-')
            this.form.name = slug
        },
        addContributor() {
            this.contributor_index += 1
            this.form.contributors.push({
                index: this.contributor_index,
                canDelete: true,
                name: '',
                type: '',
                email: '',
                url: '',
                editable: true
            })
        },
        deleteContributor(contributor) {
            this.form.contributors = this.form.contributors.filter(function(value, index, arr){
                return value.index != contributor.index
            })
        },
        addExtra() {
            this.extra_index += 1
            this.form.extras.push({
                index: this.extra_index,
                key: '',
                value: ''
            })
        },
        deleteExtra(extra) {
            this.form.extras = this.form.extras.filter(function(value, index, arr){
                return value.index != extra.index
            })
        },
        submit() {
            const formData = new FormData()
            const headers = { 'Content-Type': 'multipart/form-data' }
            if(this.form.id) {
                formData.append('id', this.form.id)
            }
            formData.append('title', this.form.title)
            formData.append('name', this.form.name)
            formData.append('notes', this.form.notes)
            formData.append('license_id', this.form.license)
            formData.append('tag_string', this.form.tags)
            formData.append('owner_org', this.form.organization)
            formData.append('private', this.form.visibility)
            formData.append('url', this.form.source)
            formData.append('version', this.form.version)
            formData.append('author', this.form.contributors[1].name)
            formData.append('author_email', this.form.contributors[1].email)
            formData.append('frequency', this.form.frequency)
            formData.append('metadata', JSON.stringify(this.form))
            axios.post("/datapackage-creator/save-package", formData, { headers }).then((res) => {
                this.error_summary = []
                if (res.data.error_summary) {
                    for(const property in res.data.error_summary) {
                        this.error_summary.push(`${property}: ${res.data.error_summary[property]}`)
                    }
                }
                this.has_error = res.data.has_error
                if(!this.has_error) {
                    window.location = `/dataset/${this.form.name}/resource/new`
                }
                this.$refs["success-message"].scrollIntoView({ behavior: "smooth" })
            })
        },
        isRequired(field_name) {
            let required = false
            if(this.settings != null && this.settings.package && this.settings.package.required) {
                required = this.settings.package.required.includes(field_name)
            }
            return required
        },
        deletePackage() {

        }
    },
    computed: {
        allowedAddData() {
            return this.form.title && this.form.notes && this.form.license && this.form.tags &&
            this.form.contributors[1].name && this.form.contributors[1].email
        }
    }
})