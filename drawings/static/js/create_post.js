window.addEventListener('load', () => {

    const imageInput = document.getElementById('image-input')
    const imagePreview = document.getElementById('image-preview')

    const hoverImageSpace = document.getElementById('hover-image-space')
    let imageForms = document.querySelectorAll('.image-form')
    let imageContainer = document.getElementById('image-cards-container')
    let totalFormsElement = document.getElementById('id_postitem_set-TOTAL_FORMS')
    let formRegex = RegExp(`postitem_set-(\\d){1}-`, 'g')

    let nextFormIndex = imageForms.length - 1

    setUpNextImageInput()

    function addForm() {
        let newForm = getLastImageForm().cloneNode(true)
        const newFormImageInput = newForm.querySelector(`.image-preview`)
        nextFormIndex++

        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `postitem_set-${nextFormIndex}-`)
        newForm.id = `post-image-card-${nextFormIndex}`
        
        imageContainer.append(newForm)
        
        setUpNextImageInput()
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
            console.log(imageBlob)
            imgPreview.src = imageBlob
        }

        if (currentImageContainer.classList.contains('invisible'))
            currentImageContainer.classList.remove('invisible')
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

    function setUpNextImageInput() {
        const currentIndex = nextFormIndex
        hoverImageSpace.setAttribute('for', getNextImageInputId())
        document.getElementById(getNextImageInputId()).addEventListener('change', e => handleImageChange(e, currentIndex))
    }
})
