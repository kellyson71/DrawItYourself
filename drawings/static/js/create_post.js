window.addEventListener('load', () => {

    // const hoverImageSpace = document.getElementById('hover-image-space')
    // let imageForms = document.querySelectorAll('.image-form')
    // let imageContainer = document.getElementById('image-cards-container')
    // let totalFormsElement = document.getElementById('id_postitem_set-TOTAL_FORMS')

    // let nextFormIndex = imageForms.length - 1

    // hoverImageSpace.setAttribute('for', `id_postitem_set-${nextFormIndex}-image`)

    // function addForm() {
    //     e.preventDefault()

    //     let newForm = imageForms[0].cloneNode(true)
    //     let formRegex = RegExp(`postitem_set-(\\d){1}-`, 'g')

    //     newForm.innerHTML = newForm.innerHTML.replace(formRegex, `postitem_set-${nextFormIndex}-`)
    //     imageContainer.append(newForm)
    //     hoverImageSpace.setAttribute('for', `id_postitem_set-${nextFormIndex}-image`)

    //     nextFormIndex++
    //     totalFormsElement.setAttribute('value', `${nextFormIndex}`)
    // }

    // function handleImageChange(e) {

    // }
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

// previnir funçao padrao do navegador
function preventDefaults(e) {
    e.preventDefault()
    e.stopPropagation()
}

// pegar o arraste e solte pelo id
let dropArea = document.getElementById('hover-image-space')

dropArea.addEventListener('dragenter', preventDefaults, false)
dropArea.addEventListener('dragover', preventDefaults, false)
dropArea.addEventListener('dragleave', preventDefaults, false)
dropArea.addEventListener('drop', preventDefaults, false)

// evento para quando a imagem for solta
dropArea.addEventListener('drop', handleDrop, false)

function handleDrop(e) {
    let dt = e.dataTransfer
    let files = dt.files
    
    // pra dps
    handleFiles(files)
}

function handleFiles(files) {
    let file = files[0]

    // FileReader para exibir a imagem 
    let reader = new FileReader()
    reader.readAsDataURL(file)
    
    reader.onloadend = function() {
        // Limpar imagens do dropbox
        let dropArea = document.querySelector('#hover-image-space')
        dropArea.innerHTML = ""

        let img = document.createElement('img')
        img.src = reader.result

        // Adicionar a imagem
        dropArea.appendChild(img)
    }

    document.querySelector('input[type="file"]').files = files
}

