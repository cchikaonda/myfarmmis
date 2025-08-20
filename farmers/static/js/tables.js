$(document).ready(function() {
    $('.datatable').each(function() {
        let $table = $(this);
        let totalRows = $table.find('tbody tr').length;

        // Dynamic lengthMenu
        let defaultOptions = [5, 10, 25, 50];
        let dynamicOptions = defaultOptions.filter(opt => opt < totalRows);
        if (!dynamicOptions.includes(totalRows) && totalRows > 0) {
            dynamicOptions.push(totalRows);
        }

        // Table title for export
        let tableTitle = $table.data('title') || $table.find('caption').text() || 'Table';

        function exportFilename() {
            let now = new Date();
            let datetime = now.getFullYear() + '-' +
                           String(now.getMonth() + 1).padStart(2,'0') + '-' +
                           String(now.getDate()).padStart(2,'0') + '_' +
                           String(now.getHours()).padStart(2,'0') +
                           String(now.getMinutes()).padStart(2,'0') +
                           String(now.getSeconds()).padStart(2,'0');
            return tableTitle.replace(/\s+/g, '_') + '_' + datetime;
        }

        $table.DataTable({
            paging: true,
            searching: true,
            ordering: true,
            info: true,
            lengthMenu: dynamicOptions,
            // 'l' = length menu, 'B' = buttons, 'f' = filter, 'tip' = table/info/pagination
            dom: "<'d-flex justify-content-between mb-2'lfB>tip",
            buttons: [
                {
                    extend: 'copy',
                    text: '📋',
                    className: 'btn btn-primary me-1 dt-btn-lg',
                    exportOptions: { columns: ':not(:last-child)' },
                    title: exportFilename()
                },
                {
                    extend: 'csv',
                    text: '💾',
                    className: 'btn btn-success me-1 dt-btn-lg',
                    exportOptions: { columns: ':not(:last-child)' },
                    title: exportFilename()
                },
                {
                    extend: 'excel',
                    text: '📊',
                    className: 'btn btn-success me-1 dt-btn-lg',
                    exportOptions: { columns: ':not(:last-child)' },
                    title: exportFilename()
                },
                {
                    extend: 'pdf',
                    text: '📄',
                    className: 'btn btn-danger me-1 dt-btn-lg',
                    exportOptions: { columns: ':not(:last-child)' },
                    title: exportFilename()
                },
                {
                    extend: 'print',
                    text: '🖨️',
                    className: 'btn btn-info me-1 dt-btn-lg',
                    exportOptions: { columns: ':not(:last-child)' },
                    title: exportFilename()
                }
            ]
        });
    });
});
