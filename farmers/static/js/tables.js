document.addEventListener("DOMContentLoaded", function () {

    // ----- Delete Modal -----
    const deleteModal = document.getElementById('deleteModal');
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
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

    // ----- DataTables (no table-level loader) -----
function initializeDatatable($table) {
    if ($.fn.DataTable.isDataTable($table)) return;

    let totalRows = $table.find('tbody tr').length;
    let defaultOptions = [5, 10, 25, 50];
    let dynamicOptions = defaultOptions.filter(opt => opt < totalRows);
    if (!dynamicOptions.includes(totalRows) && totalRows > 0) dynamicOptions.push(totalRows);

    let tableTitle = $table.data('title') || $table.find('caption').text() || 'Table';
    function exportFilename() {
        let now = new Date();
        let datetime = now.toISOString().replace(/[:T]/g, '-').split('.')[0];
        return tableTitle.replace(/\s+/g, '_') + '_' + datetime;
    }

    // Initialize DataTable directly (no loader)
    $table.DataTable({
        paging: true,
        searching: true,
        ordering: true,
        info: true,
        lengthMenu: dynamicOptions,
        dom: "<'d-flex justify-content-between mb-2'lfB>tip",
        buttons: [
            { extend: 'copy', text: '📋', className: 'btn btn-primary me-1 dt-btn-lg', exportOptions: { columns: ':not(:last-child)' }, title: exportFilename() },
            { extend: 'csv', text: '💾', className: 'btn btn-success me-1 dt-btn-lg', exportOptions: { columns: ':not(:last-child)' }, title: exportFilename() },
            { extend: 'excel', text: '📊', className: 'btn btn-success me-1 dt-btn-lg', exportOptions: { columns: ':not(:last-child)' }, title: exportFilename() },
            { extend: 'pdf', text: '📄', className: 'btn btn-danger me-1 dt-btn-lg', exportOptions: { columns: ':not(:last-child)' }, title: exportFilename() },
            { extend: 'print', text: '🖨️', className: 'btn btn-info me-1 dt-btn-lg', exportOptions: { columns: ':not(:last-child)' }, title: exportFilename() }
        ]
    });
}


    // Init all tables
    $(document).ready(function() {
        $('.datatable').each(function() {
            initializeDatatable($(this));
        });
    });

    // ----- DataTable AJAX Loader -----
    $('.datatable').on('preXhr.dt', function () {
        $('#global-page-loader').fadeIn(200);
    });
    $('.datatable').on('xhr.dt', function () {
        $('#global-page-loader').fadeOut(200);
    });

    // ----- Global Loader on Link Click -----
    $(document).on('click', 'a', function (e) {
        let href = $(this).attr('href');

        // Ignore empty, JS-only, or anchor (#) links
        if (!href || href.startsWith('#') || href.startsWith('javascript:')) {
            return;
        }

        // Prevent instant navigation
        e.preventDefault();

        // Create loader if not already
        if ($('#global-page-loader').length === 0) {
            $('body').append(`
                <div id="global-page-loader" 
                     class="d-flex justify-content-center align-items-center position-fixed top-0 start-0 w-100 h-100 bg-white bg-opacity-75"
                     style="z-index: 2000; display:none;">
                    <div class="text-center">
                        <div class="spinner-border text-primary mb-3" style="width: 3rem; height: 3rem;" role="status"></div>
                        <div class="fw-bold"></div>
                    </div>
                </div>
            `);
        }

        // Show loader, then navigate
        $('#global-page-loader').fadeIn(200, function () {
            setTimeout(function () {
                window.location.href = href;
            }, 300); // delay so loader is visible
        });
    });

});

// Global defaults
$.extend(true, $.fn.dataTable.defaults, {
    columnDefs: [{ targets: '_all', defaultContent: '' }],
    language: { emptyTable: "No data available" },
    responsive: true,
    pageLength: 10
});
