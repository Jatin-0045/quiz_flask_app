let questions = [];
let currentIndex = 0;
let score = 0;
let timer;
let timeLeft = 20;

/* Decode HTML entities */
function decodeHTML(text) {
    const txt = document.createElement("textarea");
    txt.innerHTML = text;
    return txt.value;
}

const questionDiv = document.getElementById("question");
const optionsDiv = document.getElementById("options");
const footerDiv = document.getElementById("footer");
const restartBtn = document.getElementById("restartBtn");
const quitBtn = document.getElementById("quitBtn");

/* Initial UI state */
optionsDiv.style.display = "none";
footerDiv.style.display = "none";
restartBtn.style.display = "none";

/* ================= LOAD QUIZ ================= */

fetch("/get-questions")
    .then(res => res.json())
    .then(data => {
        if (!data.results || data.results.length === 0) {
            questionDiv.innerText = "No questions available right now.";
            restartBtn.style.display = "block";
            return;
        }

        questions = data.results.map(q => {
            const opts = [...q.incorrect_answers, q.correct_answer];
            opts.sort(() => Math.random() - 0.5);

            return {
                question: decodeHTML(q.question),
                options: opts.map(o => decodeHTML(o)),
                correct: decodeHTML(q.correct_answer)
            };
        });

        optionsDiv.style.display = "grid";
        footerDiv.style.display = "flex";
        loadQuestion();
    })
    .catch(() => {
        questionDiv.innerText = "Error loading quiz.";
        restartBtn.style.display = "block";
    });

/* ================= QUIZ LOGIC ================= */

function loadQuestion() {
    clearInterval(timer);

    const q = questions[currentIndex];
    questionDiv.innerText = q.question;

    document.getElementById("progress").innerText =
        `Question ${currentIndex + 1} of ${questions.length}`;
    document.getElementById("score").innerText = `Score: ${score}`;

    startTimer();

    document.querySelectorAll(".option").forEach((btn, i) => {
        btn.innerText = q.options[i];
        btn.className = "option";
        btn.disabled = false;
        btn.onclick = () => handleAnswer(btn, q.correct);
    });
}

function startTimer() {
    timeLeft = 20;

    let timerDiv = document.getElementById("timer");
    if (!timerDiv) {
        timerDiv = document.createElement("div");
        timerDiv.id = "timer";
        footerDiv.prepend(timerDiv);
    }

    timerDiv.innerText = `Time: ${timeLeft}s`;

    timer = setInterval(() => {
        timeLeft--;
        timerDiv.innerText = `Time: ${timeLeft}s`;

        if (timeLeft <= 0) {
            clearInterval(timer);
            nextQuestion();
        }
    }, 1000);
}

function handleAnswer(btn, correct) {
    clearInterval(timer);

    document.querySelectorAll(".option").forEach(b => {
        b.disabled = true;
        if (b.innerText === correct) b.classList.add("correct");
    });

    if (btn.innerText === correct) {
        score++;
        document.getElementById("score").innerText = `Score: ${score}`;
    } else {
        btn.classList.add("wrong");
    }

    setTimeout(nextQuestion, 900);
}

function nextQuestion() {
    currentIndex++;
    if (currentIndex < questions.length) {
        loadQuestion();
    } else {
        submitResult();
    }
}

/* ================= CONTROLS ================= */

restartBtn.onclick = () => {
    window.location.href = "/index";
};

quitBtn.onclick = () => {
    submitResult(true);
};

function submitResult(isQuit = false) {
    clearInterval(timer);

    const form = document.createElement("form");
    form.method = "POST";
    form.action = "/result";

    form.innerHTML = `
        <input type="hidden" name="score" value="${score}">
        <input type="hidden" name="total" value="${isQuit ? currentIndex : questions.length}">
    `;

    document.body.appendChild(form);
    form.submit();
}

function openDeleteDialog() {
    document.getElementById("deleteDialog").classList.remove("hidden");
}

function closeDeleteDialog() {
    document.getElementById("deleteDialog").classList.add("hidden");
}

function confirmDelete() {
    document.getElementById("deleteForm").submit();
}

setTimeout(() => {
    const flashes = document.querySelectorAll('.flash-message');
    flashes.forEach(msg => {
        msg.style.animation = 'fadeOut 0.4s ease forwards';
        setTimeout(() => msg.remove(), 400);
    });
}, 3000);

function togglePassword(el) {
    const input = el.previousElementSibling;

    if (input.type === "password") {
        input.type = "text";
        el.textContent = "👁️";
    } else {
        input.type = "password";
        el.textContent = "🙈";
    }
}


