window.addEventListener('load', () => {

    const hoverImageSpace = document.getElementById('hover-image-space')
    let imageForms = document.querySelectorAll('.image-form')
    let imageContainer = document.getElementById('image-cards-container')
    let totalFormsElement = document.getElementById('id_postitem_set-TOTAL_FORMS')

    let nextFormIndex = imageForms.length - 1

    hoverImageSpace.setAttribute('for', `id_postitem_set-${nextFormIndex}-image`)

    function addForm() {
        e.preventDefault()

        let newForm = imageForms[0].cloneNode(true)
        let formRegex = RegExp(`postitem_set-(\\d){1}-`, 'g')

        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `postitem_set-${nextFormIndex}-`)
        imageContainer.append(newForm)
        hoverImageSpace.setAttribute('for', `id_postitem_set-${nextFormIndex}-image`)

        nextFormIndex++
        totalFormsElement.setAttribute('value', `${nextFormIndex}`)
    }

    function handleImageChange(e) {

    }
})

// let birdForm = document.querySelectorAll(".bird-form")
// let container = document.querySelector("#form-container")
// let addButton = document.querySelector("#add-form")
// let totalForms = document.querySelector("#id_form-TOTAL_FORMS")

// let formNum = birdForm.length-1
// addButton.addEventListener('click', addForm)

// function addForm(e){
//     e.preventDefault()

//     let newForm = birdForm[0].cloneNode(true)
//     let formRegex = RegExp(`form-(\\d){1}-`,'g')

//     formNum++
//     newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
//     container.insertBefore(newForm, addButton)
    
//     totalForms.setAttribute('value', `${formNum+1}`)
// }

