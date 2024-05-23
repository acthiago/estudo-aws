document.addEventListener('DOMContentLoaded', (event) => {
    const duration = 20 * 60; // 20 minutes
    let timer = duration, minutes, seconds;
    const display = document.querySelector('#time');
    
    function startTimer() {
        const interval = setInterval(() => {
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.textContent = minutes + ":" + seconds;

            if (--timer < 0) {
                clearInterval(interval);
                submitQuiz();
            }
        }, 1000);
    }

    startTimer();
});

function submitQuiz() {
    const questions = document.querySelectorAll('.question');
    const responses = [];
    questions.forEach((question, index) => {
        const options = question.querySelectorAll('input[type=radio]');
        let answer;
        options.forEach(option => {
            if (option.checked) {
                answer = option.value;
            }
        });
        responses.push({
            id: question.querySelector('input[type=radio]').name.split('-')[1],
            answer: answer
        });
    });

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ responses: responses })
    })
    .then(response => response.json())
    .then(result => {
        window.location.href = `/result`;
    })
    .catch(error => console.error('Error:', error));
}