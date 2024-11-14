window.addEventListener('load', () => {

    // const imageInput = document.getElementById('image-input')
    const imagePreview = document.getElementById('image-preview')

    // if (imageInput.files.length !== 0){
    //     loadImage()
    // }

    function loadImage() {
        const files = imageInput.files

        if (files.length === 0) 
            return
    
        const blob = URL.createObjectURL(files[0])

        imagePreview.src = blob
        imagePreview.classList.remove('invisible')
    }

    const hoverImageSpace = document.getElementById('hover-image-space')
    let imageForms = document.querySelectorAll('.image-form')
    let imageContainer = document.getElementById('image-cards-container')
    let totalFormsElement = document.getElementById('id_postitem_set-TOTAL_FORMS')
    let formRegex = RegExp(`postitem_set-(\\d){1}-`, 'g')

    let nextFormIndex = imageForms.length - 1

    setUpNextImageInput()

    function addForm() {
        let newForm = getLastImageForm().cloneNode(true)
        nextFormIndex++

        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `postitem_set-${nextFormIndex}-`)
        newForm.id = `post-image-card-${nextFormIndex}`
        
        imageContainer.append(newForm)
        
        setUpNextImageInput()
        totalFormsElement.setAttribute('value', `${nextFormIndex}`)
    }

    function handleImageChange(e, index) {
        const currentImageContainer = document.getElementById(getImageContainerId(index))

        addForm()

        if (currentImageContainer.classList.contains('invisible'))
            currentImageContainer.classList.remove('invisible')
    }

    function getLastImageForm() {
        const imageForms = document.querySelectorAll('.image-form')

        return imageForms[imageForms.length - 1] || null
    }
    
    function getNextImageInputId() {
        return `id_postitem_set-${nextFormIndex}-image`
    }

    function getImageContainerId(index) {
        return `post-image-card-${index}`
    }

    function setUpNextImageInput() {
        hoverImageSpace.setAttribute('for', getNextImageInputId())
        document.getElementById(getNextImageInputId()).addEventListener('change', e => handleImageChange(e, nextFormIndex))
    }
    // imageInput.addEventListener('change', () => {
    //     loadImage()        
    // })
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
// window.addEventListener('load', () => {
//     const imageInput = document.getElementById('image-input'); // Campo de input (invisível)
//     const dropArea = document.getElementById('hover-image-space'); // Área de arraste e solta
//     const placeholderText = document.getElementById('placeholder-text'); // Texto inicial de placeholder
//     const imagePreview = document.createElement('img'); // Criar um elemento img para a prévia
//     dropArea.appendChild(imagePreview); // Adiciona a prévia na área de drop

//     // Lógica para carregar e mostrar a imagem
//     function loadImage(files) {
//         if (files.length === 0) return;

//         const blob = URL.createObjectURL(files[0]); // Criar uma URL temporária para a imagem
//         imagePreview.src = blob; // Definir a URL como a fonte da imagem
//         imagePreview.classList.remove('invisible'); // Mostrar a prévia da imagem
//         imagePreview.style.maxWidth = '100%'; // Ajustar o tamanho da imagem
//         imagePreview.style.height = 'auto'; // Ajustar a altura proporcionalmente

//         // Esconde o texto de placeholder assim que a imagem for carregada
//         if (placeholderText) {
//             placeholderText.style.display = 'none';
//         }
//     }

//     // Quando o input de arquivo mudar (imagem selecionada manualmente)
//     imageInput.addEventListener('change', () => {
//         loadImage(imageInput.files); // Carregar a imagem selecionada
//     });

//     // Prevenir comportamento padrão em arrastar e soltar
//     function preventDefaults(e) {
//         e.preventDefault();
//         e.stopPropagation();
//     }

//     // Eventos de arraste na área de drop
//     dropArea.addEventListener('dragenter', preventDefaults, false);
//     dropArea.addEventListener('dragover', preventDefaults, false);
//     dropArea.addEventListener('dragleave', preventDefaults, false);
//     dropArea.addEventListener('drop', preventDefaults, false);

//     // Lógica ao soltar a imagem na área de drop
//     dropArea.addEventListener('drop', handleDrop, false);

//     function handleDrop(e) {
//         let dt = e.dataTransfer;
//         let files = dt.files;

//         // Atribuir a imagem arrastada ao input invisível
//         let dataTransfer = new DataTransfer();
//         dataTransfer.items.add(files[0]);
//         imageInput.files = dataTransfer.files;

//         // Carregar e mostrar a imagem arrastada
//         loadImage(files);
//     }
// });