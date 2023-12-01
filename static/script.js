document.addEventListener('DOMContentLoaded', () => {
    const copyButtons = document.querySelectorAll('.copy-button');

    copyButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const textarea = button.previousElementSibling;

            try {

                navigator.clipboard.writeText(textarea.value)
                    .then(() => {
                        alert('Texte copié avec succès');
                    })
                    .catch((err) => {
                        console.error('Erreur lors de la copie du texte', err);
                    });
            } catch (err) {
                console.error('Erreur lors de la copie du texte', err);
            }
        });
    });
});

function updateFileName() {
    const fileInput = document.getElementById('fileInput');
    const fileNameElement = document.getElementById('fileName');

    if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        fileNameElement.innerHTML = fileName;
    } else {

        fileNameElement.innerHTML = "Drop files anywhere to upload <br/>or<br/>Select Files";
    }
}
