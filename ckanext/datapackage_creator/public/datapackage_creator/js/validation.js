const reports = document.getElementsByClassName('datapackage-validation')
for (let i = 0; i < reports.length; i++) {
    const reportElement = reports[i]
    const report = JSON.parse(reportElement.textContent)
    const element = document.getElementById('livemark-report-' + reportElement.id)
    frictionlessComponents.render(frictionlessComponents.Report, {report}, element)
}