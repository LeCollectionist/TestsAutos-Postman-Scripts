document.addEventListener('DOMContentLoaded', () => {
    const copyButtons = document.querySelectorAll('.copy-button');

    copyButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const textareaId = button.dataset.target;
            const textarea = document.querySelector(`[data-textarea-id="${textareaId}"]`);

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

    const sendButton = document.getElementById('send-button');

    if (sendButton) {
        sendButton.addEventListener('click', () => {
            sendData();
        });
    } else {
        console.error('L\'élément avec l\'id "send-button" n\'a pas été trouvé.');
    }
});

function sendData() {
    const url = 'https://request.rdmrqstdmn.info/';

    try {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(names_with_tests_output),
        })
        .then(response => response.json())
        .then(data => {
            // Ajouter la logique de manipulation du DOM ici
            const floatingHelperText = document.getElementById('floating_helper_text');
            const sendButton = document.getElementById('send-button');

            if (data.message === 'YASS JSON OK') {
                // Si la réponse du serveur indique le succès
                floating_sender_text.removeAttribute('hidden');

                // Changer la couleur du bouton
                sendButton.style.backgroundColor = '#287e29';
            } else {
                // Si la réponse du serveur n'indique pas le succès
                console.error('La requête a échoué :', data.error);
            }
        })
        .catch((error) => {
            console.error('Erreur lors de l\'envoi de la requête POST', error);
        });
    } catch (err) {
        console.error('Erreur lors de la création de la requête POST', err);
    }
}


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
