document.addEventListener('DOMContentLoaded', function () {
    var formsetContainer = document.getElementById('formset-container');
    var addFormBtn = document.getElementById('add-form');
    var totalForms = document.querySelector('#id_form-TOTAL_FORMS');

    

    // Listen for the add button click
    addFormBtn.addEventListener('click', function (e) {
        e.preventDefault();

        // Get the last form in the formset container
        var currentForms = formsetContainer.querySelectorAll('.form-row');
        if (currentForms.length === 0) {
            console.error('No forms found in formset container.');
            return;
        }

        // Clone the last form in the formset
        var newForm = currentForms[currentForms.length - 1].cloneNode(true);

        // Update the form index
        var formIndex = parseInt(totalForms.value);
        var regex = new RegExp(`form-(\\d){1,}-`, 'g');
        newForm.innerHTML = newForm.innerHTML.replace(regex, `form-${formIndex}-`);

        // Clear the input values in the cloned form
        newForm.querySelectorAll('input, select, textarea').forEach(input => {
            input.value = '';
            // Uncheck checkboxes if present
            if (input.type === 'checkbox') {
                input.checked = false;
            }
        });

        // Append the new form to the formset container
        formsetContainer.appendChild(newForm);

        // Increment the form count
        totalForms.value = formIndex + 1;
    });

    // Handle the delete button click
    formsetContainer.addEventListener('click', function (e) {
        if (e.target.classList.contains('delete-form')) {
            e.preventDefault();

            // Remove the selected form row
            var formRow = e.target.closest('.form-row');
            if (formRow) {
                formRow.remove();
                // Decrement the total forms count
                totalForms.value = parseInt(totalForms.value) - 1;

                // Re-index the remaining forms
                var forms = formsetContainer.querySelectorAll('.form-row');
                forms.forEach((form, index) => {
                    form.innerHTML = form.innerHTML.replace(regex, `form-${index}-`);
                });
            }
        }
    });
});
