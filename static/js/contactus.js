function handleSubmit(event) {
    event.preventDefault(); // Prevents the default form submission behavior

    // Show success message at the top of the page
    document.getElementById('successMessage').style.display = 'block';

    // Reset form fields
    document.getElementById('contactForm').reset();

    // Optionally hide success message after a few seconds
    setTimeout(function () {
        document.getElementById('successMessage').style.display = 'none';
    }, 5000);
}
