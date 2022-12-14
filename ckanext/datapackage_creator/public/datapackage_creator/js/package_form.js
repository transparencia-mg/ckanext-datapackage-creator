var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vue-app',
    data: {
        has_error: false,
        error_summary: '',
        contributor_index: 2,
        extra_index: 0,
        form: {
            title: '',
            pkg_name: '',
            name: '',
            notes: '',
            organization: '',
            visibility: true,
            license: '',
            type: 'Tabular',
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
                    url: ''
                },
                {
                    index: 2,
                    canDelete: false,
                    type: 'Author',
                    name: '',
                    email: '',
                    url: ''
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
            'Tabular',
            'Not Tabular'
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
        // this.form.pkg_name = this.$refs.pkgName.value
    },
    methods: {
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
                url: ''
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
            formData.append('title', this.form.title)
            formData.append('name', this.form.name)
            formData.append('notes', this.form.notes)
            formData.append('license_id', this.form.license)
            formData.append('tag_string', this.form.tags)
            formData.append('owner_org', this.form.organization)
            formData.append('private', this.form.visibility)
            formData.append('url', this.form.source)
            formData.append('version', this.form.version)
            formData.append('author', this.form.contributors[0].name)
            formData.append('author_email', this.form.contributors[0].email)
            formData.append('maintainer', this.form.contributors[1].name)
            formData.append('maintainer_email', this.form.contributors[1].email)
            formData.append('metadata', JSON.stringify(this.form))
            axios.post("/datapackage-creator/save-package", formData, { headers }).then((res) => {
                this.error_summary = res.data.error_summary
                if(!this.has_error) {
                    window.location = `/dataset/${this.form.name}/resource/new`
                }
            })
        }
    }
})