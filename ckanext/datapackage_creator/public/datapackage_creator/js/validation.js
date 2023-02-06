let validations = document.getElementsByClassName('frictionless-validation')
for (let index = 0; index < validations.length; index++) {
    const element = validations[index]
    console.log(element.innerHTML)
    let jsonObj = JSON.parse(element.innerHTML)
    var jsonPretty = JSON.stringify(jsonObj, null, '\t')
    element.innerHTML = jsonPretty
}
