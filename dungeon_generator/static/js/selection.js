function toggleMethod() {
    const selectedMethod = document.getElementById('room-size-method').value;
    const methods = ["fixed", "range", "factor"];
    methods.forEach(method => {
        const methodElement = document.getElementById(method);
        if (method === selectedMethod) {
          methodElement.classList.remove('disabled');
        } else {
          methodElement.classList.add('disabled');
    }
  });
}

document.addEventListener('DOMContentLoaded', toggleMethod);