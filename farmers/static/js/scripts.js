document.addEventListener("DOMContentLoaded", function () {

    // ----- Delete Modal -----
    const deleteModal = document.getElementById('deleteModal');
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;

            // Support both data attributes
            const deleteUrl = button.getAttribute('data-delete-url') || button.getAttribute('data-url');
            const itemName = button.getAttribute('data-item-name');

            const modalTitle = deleteModal.querySelector('#itemName');
            const form = deleteModal.querySelector('#deleteForm');

            modalTitle.textContent = itemName;
            form.action = deleteUrl;
        });
    }

    // ----- SweetAlert Messages -----
    if (window.djangoMessages) {
        window.djangoMessages.forEach(msg => {
            Swal.fire({
                title: msg.tags.charAt(0).toUpperCase() + msg.tags.slice(1),
                text: msg.text,
                icon: msg.tags.includes('success') ? 'success' :
                      msg.tags.includes('error') ? 'error' :
                      msg.tags.includes('warning') ? 'warning' : 'info',
                confirmButtonText: "OK",
                timer: 2000,
                timerProgressBar: true
            });
        });
    }

});

