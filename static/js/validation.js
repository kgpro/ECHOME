document.addEventListener("DOMContentLoaded", () => {

    function showError(input, message) {
        clearError(input);
        const err = document.createElement("div");
        err.className = "input-error";
        err.innerText = message;
        input.classList.add("input-invalid");
        input.parentNode.appendChild(err);
    }

    function clearError(input) {
        input.classList.remove("input-invalid");
        const existing = input.parentNode.querySelector(".input-error");
        if (existing) existing.remove();
    }

    function validEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function validUsername(u) {
        return /^[a-zA-Z0-9_]{3,20}$/.test(u);
    }

    function validFullName(name) {
        return name.trim().length >= 3;
    }

    /* -------------------- SIGNUP -------------------- */
    const signupForm = document.getElementById("signupForm");

    if (signupForm) {
        signupForm.addEventListener("submit", (e) => {

            const fullName = document.getElementById("fullName");
            const username = document.getElementById("username");
            const email = document.getElementById("email");
            const pass = document.getElementById("password");
            const conf = document.getElementById("confirmPassword");

            let errors = 0;
            [fullName, username, email, pass, conf].forEach(clearError);

            if (!validFullName(fullName.value)) {
                showError(fullName, "Enter a valid full name");
                errors++;
            }

            if (!validUsername(username.value)) {
                showError(username, "Username must be 3–20 characters.");
                errors++;
            }

            if (!validEmail(email.value)) {
                showError(email, "Enter a valid email address");
                errors++;
            }

            if (pass.value.length < 6) {
                showError(pass, "Password must be at least 6 characters");
                errors++;
            }

            if (pass.value !== conf.value) {
                showError(conf, "Passwords do not match");
                errors++;
            }

            if (errors > 0) {
                e.preventDefault();
                return;
            }


        });
    }

    /* -------------------- LOGIN -------------------- */
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", (e) => {

            const email = document.getElementById("loginEmail");
            const password = document.getElementById("loginPassword");

            let errors = 0;
            [email, password].forEach(clearError);

            if (!validEmail(email.value)) {
                showError(email, "Invalid email");
                errors++;
            }

            if (!password.value.trim()) {
                showError(password, "Password required");
                errors++;
            }

            if (errors > 0) {
                e.preventDefault();
                return;
            }


        });
    }
});
