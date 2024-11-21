export async function ajaxRequest(url, data = null) {
    let token = document.getElementsByName("csrfmiddlewaretoken")[0].value
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token  
        }
    };
  
    if (data) options.body = JSON.stringify(data);
  
    const response = await fetch(url, options);
    if (!response.ok) {
        throw new Error(response.textMessage);
    }
    return await response.json();
}

export let invalidateInputs = (inputs) => {
    inputs.forEach(input => {
        input.classList.add("border-red-500", "bg-red-50");
        input.classList.remove("border-gray-300");
    })
}

export let validateInputs = (inputs) => {
    inputs.forEach(input => {
        input.classList.remove("border-red-500", "bg-red-50");
        input.classList.add("border-gray-300");
    })
}

export let setMessage = (msg, type, label) => {
    if (type === "error") { label.classList.remove("msgSuccess"); label.classList.add("msgError"); }
    if (type === "success") { label.classList.remove("msgError"); label.classList.add("msgSuccess"); }
    label.innerHTML = msg;
}

export let clearMessage = (label) => label.textContent = ''

export let isLoading = (el, state) => 
    state ? el.classList.remove('hidden') : el.classList.add('hidden');


export let disableInputs = inputs => inputs.forEach(input => input.setAttribute('disabled', true))
export let enableInputs = inputs => inputs.forEach(input => input.removeAttribute('disabled'))


export let clearInputs = inputs => inputs.forEach(input => input.value = '')