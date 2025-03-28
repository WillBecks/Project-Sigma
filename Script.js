document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("registerForm");
    const loginForm = document.getElementById("loginForm");

    if (registerForm) {
        registerForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const data = {
                username: document.getElementById("username").value,
                password: document.getElementById("password").value,
                email: document.getElementById("email").value,
                address: document.getElementById("address").value,
                streetname: document.getElementById("streetname").value,
                housenumber: document.getElementById("housenumber").value,
                zipcode: document.getElementById("zipcode").value,
                city: document.getElementById("city").value,
                km_monday: document.getElementById("km_monday").value,
                km_tuesday: document.getElementById("km_tuesday").value,
                km_wednesday: document.getElementById("km_wednesday").value,
                km_thursday: document.getElementById("km_thursday").value,
                km_friday: document.getElementById("km_friday").value
            };

            fetch("/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Registratie geslaagd!");
                    window.location.href = "/startscherm.html";
                } else {
                    document.getElementById("errorMessage").innerText = data.errors.join(", ");
                }
            })
            .catch(error => console.error("Fout bij registratie:", error));
        });
    }

    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const data = {
                username: document.getElementById("loginUsername").value,
                password: document.getElementById("loginPassword").value
            };

            fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Login succesvol!");
                    window.location.href = "/startscherm.html";
                } else {
                    document.getElementById("errorMessage").innerText = data.error;
                }
            })
            .catch(error => console.error("Fout bij inloggen:", error));
        });
    }
});
