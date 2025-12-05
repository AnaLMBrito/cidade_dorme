// Função para timer com submissão automática de formulário
function startTimer(seconds, formId, timerId, redirectUrl = null) {
    let timeLeft = seconds;
    const timerElement = document.getElementById(timerId);
    const form = formId ? document.getElementById(formId) : null;

    const countdown = setInterval(() => {
        timeLeft--;
        if (timerElement) {
            timerElement.textContent = timeLeft;
        }
        
        if (timeLeft <= 0) {
            clearInterval(countdown);
            if (form) {
                form.submit();
            } else if (redirectUrl) {
                window.location.href = redirectUrl;
            }
        }
    }, 1000);
}

// Função para timer com redirecionamento simples
function redirectTimer(seconds, timerId, redirectUrl) {
    let timeLeft = seconds;
    const timerElement = document.getElementById(timerId);

    const countdown = setInterval(() => {
        timeLeft--;
        if (timerElement) {
            timerElement.textContent = timeLeft;
        }
        
        if (timeLeft <= 0) {
            clearInterval(countdown);
            window.location.href = redirectUrl;
        }
    }, 1000);
}