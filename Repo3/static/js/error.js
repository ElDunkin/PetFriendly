document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    const error = urlParams.get('error');
    if (error) {
        const modal = new bootstrap.Modal(document.getElementById('errorModal'));
        modal.show();
    }
});
