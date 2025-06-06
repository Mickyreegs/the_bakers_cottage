/* jshint esversion: 8 */

//Removes item from modify order
function removeItem(itemId, orderId) {
	fetch(`/shop/modify_order/${orderId}/`, {
		method: "POST",
		headers: {
			"X-CSRFToken": document.querySelector("input[name=csrfmiddlewaretoken]")
				.value,
			"Content-Type": "application/x-www-form-urlencoded",
		},
		body: "remove_item=" + itemId,
	}).then((response) => {
		if (response.ok) {
			location.reload();
		} else {
			alert("Failed to remove item.");
		}
	});
}

//Google maps
if (document.getElementById("map")) {
	let googleMap;

	const initMap = async () => {
		const position = { lat: 51.88226, lng: -8.43848 };

		const { Map } = await google.maps.importLibrary("maps");
		const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

		googleMap = new Map(document.getElementById("map"), {
			zoom: 14,
			center: position,
			mapId: "{{ MAP_ID }}",
		});

		const marker = new AdvancedMarkerElement({
            map: googleMap,
            position: position,
            title: "Our Location",
        });

		console.log("Google Maps initialized successfully!");
	};

    window.initMap = initMap;
}
    

//email.js
document.addEventListener("DOMContentLoaded", () => {
	const contactForm = document.getElementById("contact-form");

	if (contactForm) {
		contactForm.addEventListener("submit", function (event) {
			event.preventDefault();

			const serviceID = "service_8zte0gb";
			const templateID = "contact";

			const templateParams = {
				name: document.getElementById("name").value,
				email: document.getElementById("email").value,
				message: document.getElementById("message").value,
			};

			emailjs
				.send(serviceID, templateID, templateParams)
				.then(() => {
					document.getElementById("success-message").style.display = "block";
					contactForm.reset();
				})
				.catch((error) => {
					console.error("EmailJS Error:", error);
					document.getElementById("fail-message").style.display = "block";
				});
		});
	}
});

document.addEventListener("DOMContentLoaded", function () {
	const bookingForm = document.querySelector("#booking-form");
	const logoutForm = document.querySelector("#logout-form");
	const guestNameInput = document.querySelector("#id_guest_name");
	const guestEmailInput = document.querySelector("#id_guest_email");
	const userAuthStatus = document.querySelector("#user-authenticated");
	const specialGuestsInput = document.querySelector(
		"#id_guests_with_special_requests"
	);
	const totalGuestsInput = document.querySelector("#id_number_of_guests");
	const dateInput = document.querySelector("#id_date");
	const timeInput = document.querySelector("#id_time");

	// Ensure only future dates can be selected
	const today = new Date().toISOString().split("T")[0];
	if (dateInput) {
		dateInput.setAttribute("min", today);
	}

	// Prevent selecting a past time when booking for today
	if (timeInput && dateInput) {
		dateInput.addEventListener("change", function () {
			if (dateInput.value === today) {
				const now = new Date();
				const currentTime =
					now.getHours().toString().padStart(2, "0") +
					":" +
					now.getMinutes().toString().padStart(2, "0");
				timeInput.setAttribute("min", currentTime);
			} else {
				timeInput.removeAttribute("min");
			}
		});
	}

	// Function to display messages dynamically
	function showMessage(id) {
		const message = document.getElementById(id);
		if (message) {
			message.style.display = "block";
			setTimeout(() => (message.style.display = "none"), 3000);
		}
	}

	// Handle adding items to cart dynamically
	const cartForms = document.querySelectorAll(".add-to-cart-form");
	cartForms.forEach((form) => {
		form.addEventListener("submit", function (event) {
			event.preventDefault(); // Prevent full page reload

			fetch(form.action, {
				method: "POST",
				body: new FormData(form),
			})
				.then((response) => response.json())
				.then((data) => {
					showMessage("cartMessage"); // Show add-to-cart success message
					document.getElementById(
						"cartTotal"
					).textContent = `Total: €${data.cart_total}`;
				})
				.catch((error) => console.error("Error:", error));
		});
	});

	// Handle removing items from cart in modal dynamically
	const removeButtons = document.querySelectorAll(".remove-from-cart");
	removeButtons.forEach((button) => {
		button.addEventListener("click", function (event) {
			event.preventDefault(); // Prevent page reload

			fetch(button.href, {
				method: "GET",
			})
				.then((response) => response.json())
				.then((data) => {
					showMessage("removeMessage"); // Show removal success message
					document.getElementById(
						"cartTotal"
					).textContent = `Total: €${data.cart_total}`;
					button.closest(".list-group-item").remove(); // Remove item visually from modal
				})
				.catch((error) => console.error("Error:", error));
		});
	});

	// Function to display error messages
	function showErrorMessage(messages) {
		const errorContainer = document.querySelector("#form-errors");
		if (errorContainer) {
			errorContainer.innerHTML = "";

			const errorAlert = document.createElement("div");
			errorAlert.className = "alert alert-danger alert-dismissible fade show";
			errorAlert.setAttribute("role", "alert");

			errorAlert.innerHTML = `
                ${messages.join("<br>")}  
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            `;

			errorContainer.appendChild(errorAlert);
		}
	}

	// Prevent empty booking form submissions
	function toggleSubmitButton() {
		const submitButton = document.querySelector(
			"#booking-form button[type='submit']"
		);
		if (submitButton && bookingForm) {
			submitButton.disabled = !bookingForm.checkValidity();
		}
	}

	if (bookingForm) {
		bookingForm.addEventListener("input", toggleSubmitButton);

		bookingForm.addEventListener("submit", function (event) {
			console.log("Booking Submit event triggered!");
			event.preventDefault();

			let errorMessages = [];
			const guestName = guestNameInput ? guestNameInput.value.trim() : "";
			const guestEmail = guestEmailInput ? guestEmailInput.value.trim() : "";
			const userAuthenticated = userAuthStatus ?
				userAuthStatus.dataset.authenticated === "true" :
				false;

			if (!userAuthenticated && (!guestName || !guestEmail)) {
				errorMessages.push("Guest bookings require both a name and an email.");
			}

			if (errorMessages.length > 0) {
				showErrorMessage(errorMessages);
			} else {
				console.log("Validation passed. Submitting booking form...");
				bookingForm.submit();
			}
		});
	}

	// Allow logout form to submit properly
	if (logoutForm) {
		logoutForm.addEventListener("submit", function (event) {
			console.log("Logout form submitted!");
		});
	}
});
