document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('year').textContent = new Date().getFullYear();

    const daysEl = document.getElementById('days');
    const hoursEl = document.getElementById('hours');
    const minutesEl = document.getElementById('minutes');
    const secondsEl = document.getElementById('seconds');
    const billEl = document.getElementById('bill');
    const win11El = document.getElementById('win11-gif'); // Elemento para el nuevo GIF

    const endDate = new Date('2025-10-14T23:59:59');
    let lastMinute = -1;

    // Función para mostrar a Bill Gates (para el botón)
    function danceBillDance() {
        billEl.classList.add('show');
        setTimeout(() => {
            billEl.classList.remove('show');
        }, 10000); // Show for 10 seconds
    }

    // Función para mostrar el GIF de Windows 11 (para el cambio de minuto)
    function showWin11Gif() {
        win11El.classList.add('show');
        setTimeout(() => {
            win11El.classList.remove('show');
        }, 10000); // Show for 10 seconds
    }

    function updateCountdown() {
        const now = new Date();
        const diff = endDate - now;

        if (diff <= 0) {
            document.querySelector('.container').innerHTML = '<h1>Windows 10 support has ended!</h1>';
            clearInterval(countdownInterval);
            billEl.remove();
            win11El.remove();
            return;
        }

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        // Initialize lastMinute on the first run
        if (lastMinute === -1) {
            lastMinute = minutes;
        }

        daysEl.innerText = days;
        hoursEl.innerText = hours.toString().padStart(2, '0');
        minutesEl.innerText = minutes.toString().padStart(2, '0');
        secondsEl.innerText = seconds.toString().padStart(2, '0');

        // Check if the minute has changed since the last update
        if (minutes !== lastMinute) {
            showWin11Gif(); // <-- AQUÍ ESTÁ EL CAMBIO
            lastMinute = minutes; // Update the last minute
        }
    }

    // Initial call to set the values right away
    updateCountdown();
    
    // Update countdown every second
    const countdownInterval = setInterval(updateCountdown, 1000);

    // Listener para el botón de llamar
    const callBillButton = document.getElementById('call-bill-button');
    callBillButton.addEventListener('click', danceBillDance);
});