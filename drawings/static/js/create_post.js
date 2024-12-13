window.addEventListener('load', () => {

    const imageInput = document.getElementById('image-input')
    const imagePreview = document.getElementById('image-preview')

    const hoverImageSpace = document.getElementById('hover-image-space')
    let imageForms = document.querySelectorAll('.image-form')
    let imageContainer = document.getElementById('image-cards-container')
    let totalFormsElement = document.getElementById('id_postitem_set-TOTAL_FORMS')
    let formRegex = RegExp(`postitem_set-(\\d){1}-`, 'g')

    let nextFormIndex = imageForms.length - 1

    updateAllForms()
    setUpHoverSpace()

    function addForm() {
        let newForm = getLastImageForm().cloneNode(true)
        const imageInputLabel = newForm.querySelector(`#image-input-label`)
        nextFormIndex++

        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `postitem_set-${nextFormIndex}-`)
        newForm.id = `post-image-card-${nextFormIndex}`

        imageInputLabel.setAttribute('for', getNextImageInputId())
        
        imageContainer.append(newForm)
        
        setUpNextImageForm()
        totalFormsElement.setAttribute('value', `${nextFormIndex}`)
    }

    function handleImageChange(e, index) {
        const currentImageContainer = document.getElementById(getImageContainerId(index))

        if (nextFormIndex === index)
            addForm()
        
        const imgPreview = currentImageContainer.querySelector(`.image-preview`)
        const imgInput = currentImageContainer.querySelector(`#${getImageInputId(index)}`)

        if (imgPreview) {
            const imageBlob = URL.createObjectURL(imgInput.files[0]) 
            imgPreview.src = imageBlob
        }

        if (currentImageContainer.classList.contains('invisible'))
            currentImageContainer.classList.remove('invisible')
    }

    function handleRemoveForm(index) {
        console.log("HERE")

        const form = document.getElementById(getImageContainerId(index))
        form.remove()

        nextFormIndex--
        totalFormsElement.setAttribute('value', `${nextFormIndex}`)

        updateAllForms()
    }

    function updateAllForms() {
        const formCards = document.getElementById('image-cards-container').querySelectorAll("article")
        
        formCards.forEach((card, index) => {
            card.id = `post-image-card-${index}`
            card.innerHTML = card.innerHTML.replace(formRegex, `postitem_set-${index}-`)
            setUpImageForm(index)
        })

        nextFormIndex = formCards.length - 1
        setUpHoverSpace()
    }

    function getLastImageForm() {
        const imageForms = document.querySelectorAll('.image-form')

        return imageForms[imageForms.length - 1] || null
    }
    
    function getNextImageInputId() {
        return getImageInputId(nextFormIndex)
    }

    function getImageInputId(index) {
        return `id_postitem_set-${index}-image`
    }

    function getImageContainerId(index) {
        return `post-image-card-${index}`
    }

    function setUpImageForm(index) {
        const deleteButton = document.getElementById(getImageContainerId(index)).querySelector('.form-delete-button')
        const imageInput = document.getElementById(getImageInputId(index))

        imageInput.addEventListener('change', e => handleImageChange(e, index))
        deleteButton.addEventListener('click', () => handleRemoveForm(index))
    }

    function setUpNextImageForm() {
        const index = nextFormIndex
        setUpImageForm(index)
        setUpHoverSpace()
    }

    function setUpHoverSpace() {
        hoverImageSpace.setAttribute('for', getNextImageInputId())
    }
})
