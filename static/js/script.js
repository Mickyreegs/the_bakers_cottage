document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const guestNameInput = document.querySelector("#id_guest_name");
    const guestEmailInput = document.querySelector("#id_guest_email");
    const userAuthStatus = document.querySelector("#user-authenticated");
    const specialGuestsInput = document.querySelector("#id_guests_with_special_requests");
    const totalGuestsInput = document.querySelector("#id_number_of_guests");

    // Booking form validation
    form.addEventListener("submit", function(event) {
        const guestName = guestNameInput.value.trim();
        const guestEmail = guestEmailInput.value.trim();
        const userAuthenticated = userAuthStatus.dataset.authenticated === "true";

        if (!userAuthenticated && (!guestName || !guestEmail)) {
            event.preventDefault();
            showErrorMessage("Guest bookings require both a name and an email.");
        }
    });

    // Validate number of special request guests
    specialGuestsInput.addEventListener("input", function() {
        let totalGuests = parseInt(totalGuestsInput.value) || 1;
        let specialGuests = parseInt(this.value) || 0;

        if (specialGuests > totalGuests) {
            showErrorMessage("The number of guests with special requests cannot exceed the total number of guests.");
            this.value = totalGuests;
        }
    });

    // Function to display error messages
    function showErrorMessage(message) {
        const errorContainer = document.querySelector("#form-errors");
        if (errorContainer) {
            errorContainer.innerHTML = ""; // Clears previous errors
            const errorAlert = document.createElement("div");
            errorAlert.className = "alert alert-danger alert-dismissible fade show";
            errorAlert.setAttribute("role", "alert");
            errorAlert.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            `;
            errorContainer.appendChild(errorAlert);
        }
    }

});
