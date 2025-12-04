// Função para criar contagem regressiva de 1 minuto (60 segundos)
function startTimer(duration, formId, displayId) {
    let time = duration;
    let display = document.getElementById(displayId);
    let form = document.getElementById(formId);

    let countdown = setInterval(() => {
        display.textContent = time;
        time--;
        if (time < 0) {
            clearInterval(countdown);
            // envia o formulário automaticamente quando o tempo acabar
            form.submit();
        }
    }, 1000);
}
