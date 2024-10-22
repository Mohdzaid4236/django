// Get references to all sections, progress list items, and buttons
const formSections = document.querySelectorAll('.form-section');
const progressItems = document.querySelectorAll('#progress-list li');

// Function to show the specific form section
function showSection(sectionId) {
    // Hide all sections
    formSections.forEach(section => section.classList.remove('active'));

    // Show the requested section
    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.classList.add('active');
    }

    // Update progress bar
    progressItems.forEach(item => item.classList.remove('active'));
    const activeIndex = Array.from(progressItems).findIndex(item => item.getAttribute('data-section') === sectionId);
    if (activeIndex !== -1) {
        progressItems[activeIndex].classList.add('active');
    }
}

// Add click event listener to each progress item
progressItems.forEach(item => {
    item.addEventListener('click', () => {
        const sectionId = item.getAttribute('data-section');
        showSection(sectionId);
    });
});

// Next button functionality
document.querySelectorAll('.next-btn').forEach(button => {
    button.addEventListener('click', () => {
        const currentSection = button.closest('.form-section');
        const nextSection = currentSection.nextElementSibling;

        if (nextSection) {
            showSection(nextSection.id);
        }
    });
});

// Previous button functionality
document.querySelectorAll('.prev-btn').forEach(button => {
    button.addEventListener('click', () => {
        const currentSection = button.closest('.form-section');
        const prevSection = currentSection.previousElementSibling;

        if (prevSection) {
            showSection(prevSection.id);
        }
    });
});

// Initialize the form by showing the first section
showSection(formSections[0].id);
