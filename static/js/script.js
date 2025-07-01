function validateForm() {
    const form = document.querySelector('form');
    const errorDiv = document.getElementById('error-message');
    errorDiv.style.display = 'none';
    errorDiv.textContent = '';

    const inputs = form.querySelectorAll('input, select, textarea');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value && input.required) {
            errorDiv.textContent = 'All required fields must be filled!';
            errorDiv.style.display = 'block';
            isValid = false;
        }
    });

    if (form.id === 'spoilageForm') {
        const avgTemp = parseFloat(form.querySelector('input[name="avg_temp"]').value);
        const daysStored = parseInt(form.querySelector('input[name="days_stored"]').value);
        if (isNaN(avgTemp) || isNaN(daysStored)) {
            errorDiv.textContent = 'Temperature and days stored must be valid numbers!';
            errorDiv.style.display = 'block';
            isValid = false;
        }
    }

    return isValid;
}

document.addEventListener('DOMContentLoaded', () => {
    const rows = document.querySelectorAll('#dataTable tr');
    rows.forEach(row => {
        row.addEventListener('mouseover', () => {
            row.style.transition = 'background-color 0.3s';
        });
    });
});