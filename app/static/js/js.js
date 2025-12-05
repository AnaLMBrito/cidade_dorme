function startTimer(duration, formId, displayId, redirectUrl) {
    let time = duration;
    let display = document.getElementById(displayId);
    let form = formId ? document.getElementById(formId) : null;

    let countdown = setInterval(() => {
        display.textContent = time;
        time--;
        if (time < 0) {
            clearInterval(countdown);
            if (form) {
                form.submit();  // só envia se existir form
            } else if (redirectUrl) {
                window.location.href = redirectUrl;  // redireciona se não houver form
            }
        }
    }, 1000);
}
