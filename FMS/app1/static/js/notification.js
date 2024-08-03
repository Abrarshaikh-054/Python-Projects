document.addEventListener('DOMContentLoaded', (event) => {
    const alert = document.querySelector('.alert');
    if (alert) {
        setTimeout(() => {
            alert.classList.remove('show');
            alert.classList.add('hide');
        }, 3000); // Adjust the time (3000ms = 3 seconds) as needed
    }
});