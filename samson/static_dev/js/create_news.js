document.addEventListener("DOMContentLoaded", function () {
    const formContainer = document.getElementById("form-container")
    const addFormBtn = document.getElementById("add-form")
    const totalFormsInput = document.getElementById("id_form-TOTAL_FORMS")
    const emptyFormWrapperHtml = document.getElementById("empty-form-template").innerHTML

    addFormBtn.addEventListener("click", () => {
        const newIndex = parseInt(totalFormsInput.value, 10)

        const newFormFieldsHtml = formHtml.replace(/__prefix__/g, newIndex)

        const newFormCompleteHtml = emptyFormWrapperHtml.replace(/__FORM_HTML__/g, newFormFieldsHtml)

        const tempDiv = document.createElement('div')
        tempDiv.innerHTML = newFormCompleteHtml

        const newFormElement = tempDiv.firstElementChild

        if (newFormElement) {
            formContainer.appendChild(newFormElement)
            totalFormsInput.value = newIndex + 1
        } else {
            console.error("Не удалось создать новый элемент формы из шаблона.")
        }
    })
})
