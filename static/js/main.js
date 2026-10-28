// -------------------------------------------------------------
// Online Bookstore - Main JavaScript File
// Modern interactive enhancements & Bootstrap modal wiring
// -------------------------------------------------------------

document.addEventListener('DOMContentLoaded', () => {

    // 1. Client-side Bootstrap Form Validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // 2. Dynamic Delete Confirmation Modal Wiring
    const deleteModal = document.getElementById('deleteConfirmModal');
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', event => {
            const button = event.relatedTarget;
            const bookId = button.getAttribute('data-book-id');
            const bookTitle = button.getAttribute('data-book-title');
            const bookAuthor = button.getAttribute('data-book-author');

            // Update modal text elements
            const modalBookTitle = document.getElementById('modalBookTitle');
            const modalBookId = document.getElementById('modalBookId');
            const modalBookAuthor = document.getElementById('modalBookAuthor');
            const deleteForm = document.getElementById('deleteForm');

            if (modalBookTitle) modalBookTitle.textContent = bookTitle || 'Selected Book';
            if (modalBookId) modalBookId.textContent = `#${bookId}`;
            if (modalBookAuthor) modalBookAuthor.textContent = bookAuthor ? `by ${bookAuthor}` : '';

            // Set the form action URL to /delete/<bookId>
            if (deleteForm && bookId) {
                deleteForm.action = `/delete/${bookId}`;
            }
        });
    }

    // 3. Client-side Live Search / Filter for Books Table
    const searchInput = document.getElementById('liveSearchInput');
    const tableBody = document.getElementById('booksTableBody');
    const noResultsRow = document.getElementById('noResultsRow');

    if (searchInput && tableBody) {
        searchInput.addEventListener('input', () => {
            const filter = searchInput.value.toLowerCase().trim();
            const rows = tableBody.querySelectorAll('tr.book-row');
            let visibleCount = 0;

            rows.forEach(row => {
                const titleText = row.getAttribute('data-title') || '';
                const authorText = row.getAttribute('data-author') || '';
                const idText = row.getAttribute('data-id') || '';

                if (titleText.includes(filter) || authorText.includes(filter) || idText.includes(filter)) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });

            if (noResultsRow) {
                noResultsRow.style.display = visibleCount === 0 ? '' : 'none';
            }
        });
    }

    // 4. Optional: Auto-dismiss flash alert messages after 6 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alertEl => {
        setTimeout(() => {
            // Check if Bootstrap's Alert component is available
            if (window.bootstrap && bootstrap.Alert) {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
                if (bsAlert) {
                    bsAlert.close();
                }
            }
        }, 6000);
    });

});

