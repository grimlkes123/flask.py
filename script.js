document.getElementById('dateForm').addEventListener('submit', function(event) {
    event.preventDefault();
    document.getElementById('loading').classList.remove('hidden');
    const formData = new FormData(this);
    const queryString = new URLSearchParams(formData).toString();
    setTimeout(() => {
        window.location.href = '/dataset-result?' + queryString;
    }, 3000); // 3 seconds delay
});
