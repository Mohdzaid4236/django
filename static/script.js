// JavaScript to handle form navigation and progress
document.addEventListener("DOMContentLoaded", function () {
    const formSections = document.querySelectorAll(".form-section");
    const progressList = document.querySelectorAll("#progress-list li");
    const nextBtns = document.querySelectorAll(".next-btn");
    const prevBtns = document.querySelectorAll(".prev-btn");
    const employmentEntriesContainer = document.getElementById('employment-entries-container');
    
    let currentSection = 0;
    let employmentCounter = 1; // Start from 1 as the first entry is hardcoded

    function showSection(sectionIndex) {
        formSections.forEach((section, index) => {
            section.classList.remove("active");
            progressList[index].classList.remove("active");

            if (index === sectionIndex) {
                section.classList.add("active");
                progressList[index].classList.add("active");
            }
        });
    }

    function addNextSectionHandler() {
        nextBtns.forEach((btn) => {
            btn.addEventListener("click", function () {
                if (currentSection < formSections.length - 1) {
                    currentSection++;
                    showSection(currentSection);
                }
            });
        });
    }

    function addPrevSectionHandler() {
        prevBtns.forEach((btn) => {
            btn.addEventListener("click", function () {
                if (currentSection > 0) {
                    currentSection--;
                    showSection(currentSection);
                }
            });
        });
    }

    function addProgressClickHandler() {
        progressList.forEach((item, index) => {
            item.addEventListener("click", function () {
                currentSection = index;
                showSection(currentSection);
            });
        });
    }

    function createEmploymentEntry() {
        employmentCounter++;
        const employmentEntry = document.createElement('div');
        employmentEntry.classList.add('employment-entry');
        employmentEntry.setAttribute('data-employment', employmentCounter);

        employmentEntry.innerHTML = `
            <label for="company-name-${employmentCounter}">Company Name *</label>
            <input type="text" id="company-name-${employmentCounter}" required>

            <label for="job-title-${employmentCounter}">Job Title *</label>
            <input type="text" id="job-title-${employmentCounter}" required>

            <label for="start-date-${employmentCounter}">Start Date *</label>
            <input type="date" id="start-date-${employmentCounter}" required>

            <label for="currently-working-${employmentCounter}">
                <input type="checkbox" id="currently-working-${employmentCounter}" class="currently-working-checkbox"> Currently Working
            </label>

            <label for="end-date-${employmentCounter}">End Date</label>
            <input type="date" id="end-date-${employmentCounter}" class="end-date-input">

            <label for="job-description-${employmentCounter}">Job Description</label>
            <textarea id="job-description-${employmentCounter}"></textarea>

            <button type="button" class="delete-btn">Delete</button>
        `;

        employmentEntriesContainer.appendChild(employmentEntry);

        const checkbox = employmentEntry.querySelector(`#currently-working-${employmentCounter}`);
        const endDateInput = employmentEntry.querySelector(`#end-date-${employmentCounter}`);
        checkbox.addEventListener('change', function () {
            endDateInput.disabled = checkbox.checked;
            if (checkbox.checked) {
                endDateInput.value = '';
            }
        });
    }

    function handleAddEmploymentEntry() {
        document.getElementById('add-employment-btn').addEventListener('click', function () {
            createEmploymentEntry();
            alert('Employment entry added!'); // Feedback to user
        });
    }

    function handleDeleteEmploymentEntry(event) {
        if (event.target.classList.contains('delete-btn')) {
            const employmentEntry = event.target.closest('.employment-entry');
            if (employmentEntry) {
                employmentEntry.remove();
                alert('Employment entry deleted!'); // Feedback to user
            }
        }
    }

    // Set up event handlers
    addNextSectionHandler();
    addPrevSectionHandler();
    addProgressClickHandler();
    handleAddEmploymentEntry();
    employmentEntriesContainer.addEventListener('click', handleDeleteEmploymentEntry);

    // Initially display the first section
    showSection(currentSection);
});
