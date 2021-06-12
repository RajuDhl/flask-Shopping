const span = document.getElementById('CheckPwMatch');
span.innerHTML ='&nbsp;'
function checkPasswordMatch() {
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    //const span = document.getElementById('CheckPwMatch');
    if (password !== confirmPassword) {
        span.innerHTML = 'Passwords must match';
        span.style.color = 'red';
        document.getElementById('submit_button').disabled = true;
    } else {
        span.innerHTML = 'Passwords match <i class="fa fa-check" aria-hidden="true"></i>';
        span.style.color = 'green';
        document.getElementById('submit_button').disabled = false;
    }
}