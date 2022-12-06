var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vue-app',
    data: {
        form: {
            title: '',
            description: '',
            organization: 1,
            visibility: null,
            license: null,
            type: 'Tabular',
            source: '',
            version: '',
            tags: '',
            contributors: [
                {
                    type: 'Publisher',
                    name: '',
                    email: '',
                    url: ''
                },
                {
                    type: 'Author',
                    name: '',
                    email: '',
                    url: ''
                }
            ],
            frequency: '',
            extras: [
                {
                    key: '',
                    value: ''
                }
            ]
        },
        contributorTypeOptions: [
            'Publisher',
            'Author',
            'Contributor',
            'Maintainer',
            'Data Wrangler'
        ],
        visibilityOptions: [
            'Private',
            'Public'
        ],
        licenseOptions: [
            'No',
            'MIT',
            'GPL'
        ],
        organizationOptions: [
            {
                id: 1,
                name: 'Stefanini'
            },
            {
                id: 2,
                name: 'Organização 2'
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
        console.log(userName)
        console.log(userEmail)
        this.form.contributors[0].name = userName
        this.form.contributors[0].email = userEmail
    },
    methods: {
        addContributor() {
            this.form.contributors.push({
                name: '',
                type: 'Contributor',
                email: '',
                url: ''
            })
        },
        submit() {

        }
    }
})