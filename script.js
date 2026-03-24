const questions = [
    {
        question: "Çfarë ideologjie përfaqësonte regjimi nazist?",
        options: ["Demokraci", "Komunizëm", "Fashizëm", "Liberalizëm"],
        correct: 2,
        explanation: "Regjimi nazist ishte një formë ekstreme e fashizmit që promovonte racizmin dhe autoritarizmin."
    },
    {
        question: "Kush ishte udhëheqësi kryesor i Gjermanisë Naziste?",
        options: ["Joseph Goebbels", "Hermann Göring", "Adolf Hitler", "Heinrich Himmler"],
        correct: 2,
        explanation: "Adolf Hitler drejtoi Gjermaninë naziste nga 1933 deri në 1945."
    },
    {
        question: "Çfarë simboli përdornin nazistët?",
        options: ["Ylli i kuq", "Svastika", "Hamai", "Lulja e jetës"],
        correct: 1,
        explanation: "Svastika (kryqi i përmbysur) ishte simboli kryesor i nazistëve."
    },
    {
        question: "Kur filloi Lufta e Dytë Botërore?",
        options: ["1 shtator 1939", "7 dhjetor 1941", "22 qershor 1941", "6 qershor 1944"],
        correct: 0,
        explanation: "Lufta filloi kur Gjermania pushtoi Poloninë më 1 shtator 1939."
    },
    {
        question: "Kur hynë forcat naziste gjermane në Shqipëri?",
        options: ["1936", "1939", "1941", "1943"],
        correct: 3,
        explanation: "Forcat gjermane hynë në Shqipëri në vitin 1943, pas dorëheqjes së Italisë nga Lufta."
    },
    {
        question: "Cili ishte qëllimi kryesor i nazistëve gjatë pushtimit të vendeve të tjera?",
        options: ["Të përhapnin demokracinë", "Të krijonin aleanca paqësore", "Të zgjeronin territorin dhe fuqinë e Gjermanisë", "Të ndihmonin ekonomitë lokale"],
        correct: 2,
        explanation: "Nazistët synonin të zgjeronin territorin dhe fuqinë e Gjermanisë përmes pushtimeve dhe kontrollit autoritar."
    },
    {
        question: "Si reagoi populli shqiptar ndaj pushtimit nazist?",
        options: ["Nuk reagoi fare", "Bashkëpunoi plotësisht", "Organizoi rezistencë dhe luftë partizane", "U largua nga vendi"],
        correct: 2,
        explanation: "Populli shqiptar organizoi rezistencë dhe luftë partizane ndaj pushtimit nazist."
    },
    {
        question: "Shqipëria u pushtua nga Italia në vitin?",
        options: ["1936", "1939", "1941", "1943"],
        correct: 1,
        explanation: "Italia pushtoi Shqipërinë më 7 prill 1939."
    },
    {
        question: "Kush drejtoi Shqipërinë gjatë pushtimit italian?",
        options: ["Enver Hoxha", "Mustafa Kruja", "Victor Emanueli III", "Benito Mussolini"],
        correct: 1,
        explanation: "Mustafa Kruja u emua kryeministër i Shqipërisë nga italianët në 1941-1943."
    },
    {
        question: "Si përfundoi regjimi nazist?",
        options: ["Dorëzim i pa kushteve", "Traktat paqeje", "Revolucion i brendshëm", "Vdekja e Hitler-it"],
        correct: 0,
        explanation: "Gjermania naziste u dorëzua pa kushte më 8 maj 1945."
    }
];

let currentQuestion = 0;
let score = 0;
let answered = false;

function loadQuestion() {
    const q = questions[currentQuestion];
    const container = document.getElementById('quizContainer');
    
    container.innerHTML = `
        <div class="question-container">
            <div class="question"> ${q.question}</div>
            <div class="options">
                ${q.options.map((option, index) => 
                    `<div class="option" onclick="selectAnswer(${index})">${String.fromCharCode(65 + index)}. ${option}</div>`
                ).join('')}
            </div>
            ${answered ? `<div class="answer-explanation">💡 ${q.explanation}</div>` : ''}
        </div>
    `;

    updateProgress();
    document.getElementById('nextBtn').style.display = answered ? 'block' : 'none';
    document.getElementById('score').style.display = 'none';
}

function selectAnswer(index) {
    if (answered) return;
    
    answered = true;
    const correctIndex = questions[currentQuestion].correct;
    
    document.querySelectorAll('.option').forEach((option, i) => {
        if (i === correctIndex) {
            option.classList.add('correct');
        } else if (i === index && index !== correctIndex) {
            option.classList.add('incorrect');
        }
    });

    if (index === correctIndex) {
        score++;
    }

    setTimeout(() => {
        document.getElementById('nextBtn').style.display = 'block';
    }, 1500);
}

function nextQuestion() {
    currentQuestion++;
    answered = false;
    
    if (currentQuestion < questions.length) {
        loadQuestion();
    } else {
        showResults();
    }
}

function showResults() {
    document.getElementById('quizContainer').innerHTML = `
        <div style="text-align: center; padding: 40px 20px;">
            <h2 style="font-size: 2.5em; margin-bottom: 20px;">🎉 Quiz përfunduar!</h2>
            <div class="score" style="font-size: 2em;">
                Rezultati juaj: <span id="scoreValue">${score}</span>/${questions.length}
            </div>
            <div style="margin: 20px 0; font-size: 1.2em;">
                ${getResultMessage(score)}
            </div>
        </div>
    `;
    
    document.getElementById('score').style.display = 'none';
    document.getElementById('nextBtn').style.display = 'none';
    document.getElementById('restartBtn').style.display = 'block';
}

function getResultMessage(score) {
    const percentage = (score / questions.length) * 100;
    if (percentage >= 90) return "🥇 Ekspert i Historisë!";
    if (percentage >= 70) return "🥈 Shumë mirë!";
    if (percentage >= 50) return "🥉 Mirë, por lexo më shumë!";
    return "📚 Vazhdo të studiosh!";
}

function updateProgress() {
    const progress = ((currentQuestion) / questions.length) * 100;
    document.getElementById('progressBar').style.width = progress + '%';
}

function restartQuiz() {
    currentQuestion = 0;
    score = 0;
    answered = false;
    document.getElementById('restartBtn').style.display = 'none';
    document.getElementById('score').style.display = 'none';
    loadQuestion();
}

// Nis lojën
loadQuestion();