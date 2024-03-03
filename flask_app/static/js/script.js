const commentOff = document.querySelector('.popup_container')
const quizHeader = document.querySelector('.header');
const quizSection = document.querySelector('.quiz_section');
const popupQuiz = document.querySelector('.popup_quiz');
const quizBox = document.querySelector('.quiz_box');
const nextBtn = document.querySelector('.next_button');
const resultsBox = document.querySelector('.results_box');
const tryAgainBtn = document.querySelector('.tryAgian_btn');
const goHomeBtn = document.querySelector('.goHome_btn');
let questionCount = 0;
let questionNumb = 1;
let userScore = 0;

// Function for the update comment popup

const showForm = id => {
    const form = document.getElementById(`popup_container${id}`);
    form.classList.add("active");
}

function commentOffNow(){
    commentOff.classList.remove("active");
}

// Function for the hardieness zone API

let zipCodeTB = document.getElementById('zipCodeTB')
let submitButton = document.getElementById('submitButton')
let resultsContainer = document.getElementById('resultsContainer')

async function fetchZone(zip) {
    let response = await fetch(`https://phzmapi.org/${zip}.json`)
    let zoneResults = await response.json()
    return zoneResults
}

submitButton.addEventListener('click', async () => {
    let zipCode = zipCodeTB.value
    const zipCodeRegex = /^\d{5}$/
    if (zipCodeRegex.test(zipCode)) {
        let result = await fetchZone(zipCode)
        let zone = 
            `<div class="zoneDisplay">
                <h2> Your Growing Zone </h2>
                <span>Zone: ${result.zone}</span>
                <span>Temp Range: ${result.temperature_range}</span>
                <span>Lat: ${result.coordinates.lat}</span>
                <span>Lat: ${result.coordinates.lon}</span>
            </div>`
        resultsContainer.innerHTML = zone
        zipCodeTB.value = ''
    }
    else{
    resultsContainer.innerHTML = 'Please enter a valid zip code'
    zipCodeTB.value = ''
    }
})

// Onclick to start the Popup Quiz

function startQuiz(){
    popupQuiz.classList.add("active");
    quizHeader.classList.add("active");
}
// Function to remove the popup quiz
function stopQuiz(){
    quizSection.classList.remove("active");
    popupQuiz.classList.remove("active");
    quizHeader.classList.remove("active");

}

function continueQuiz(){
    quizSection.classList.add("active");
    popupQuiz.classList.remove("active");
    quizHeader.classList.remove("active");
    quizBox.classList.add("active");
    showQuestions(0);
    questionCounter(1);
    headerScore();
}

function tryQuizAgain(){
    popupQuiz.classList.add("active");
    nextBtn.classList.remove('active');
    resultsBox.classList.remove("active");

questionCount = 0;
questionNumb = 1;
userScore = 0;
showQuestions(questionCount);
questionCounter(questionNumb);

headerScore();
}

function goHome(){
    quizSection.classList.remove("active");
    nextBtn.classList.remove('active');
    resultsBox.classList.remove("active");

questionCount = 0;
questionNumb = 1;
userScore = 0;
showQuestions(questionCount);
questionCounter(questionNumb);

headerScore();
}

function nextQuestion(){
    if (questionCount < questions.length -1){
        questionCount++;
        showQuestions(questionCount);

        questionNumb++
        questionCounter(questionNumb);

        nextBtn.classList.remove('active');
    }
    else {
        showResultBox();
    }
}


function showQuestions(index) {
    const questionText = document.querySelector('.question_text');
    const quizPics = document.querySelector('.quiz_pics');
    questionText.textContent = `${questions[index].numb}.`;
    let picsTag = 
    `<img class="quiz_picture" src="/static/images/${questions[index].question[0]}">
    <img class="quiz_picture" src="/static/images/${questions[index].question[1]}">
    <img class="quiz_picture" src="/static/images/${questions[index].question[2]}">
    <img class="quiz_picture" src="/static/images/${questions[index].question[3]}">`
    
    quizPics.innerHTML = picsTag;

    let optionTag = 
        `<div class="option"><span>${questions[index].options[0]}</span></div>
        <div class="option"><span>${questions[index].options[1]}</span></div>
        <div class="option"><span>${questions[index].options[2]}</span></div>
        <div class="option"><span>${questions[index].options[3]}</span></div>`;
    document.getElementById('option_list').innerHTML = optionTag;

    const option = document.querySelectorAll('.option');
    for (let i = 0; i < option.length; i++) {
        option[i].setAttribute('onclick', 'optionSelected(this)');
    }
}

function optionSelected(answer) {
    let userAnswer = answer.textContent;
    let correctAnswer = questions[questionCount].answer;
    let allOptions = option_list.children.length;

    if(userAnswer == correctAnswer) {
        answer.classList.add('correct');
        userScore += 1;
        headerScore();
    }
    else {
        answer.classList.add('incorrect');
        for (let i = 0; i < allOptions; i++) {
            if (option_list.children[i].textContent == correctAnswer) {
                option_list.children[i].setAttribute('class', 'option correct');
            }
        }
    }
    
    for (let i = 0; i < allOptions; i++) {
        option_list.children[i].classList.add('disabled');
    }
    nextBtn.classList.add('active');
}

function questionCounter(index) {
    const questionTotal = document.querySelector('.question_total');
    questionTotal.textContent = `${index} of ${questions.length} Questions`;
}

function headerScore() {
    const headerScoreText = document.querySelector('.header_score');
    headerScoreText.textContent = `Score: ${userScore} / ${questions.length}`
}

function showResultBox() {
    console.log(userScore, "USER SCORE!!!!")
    sendResults();

    quizBox.classList.remove('active');
    resultsBox.classList.add('active');

    const scoreText = document.querySelector('.score_text');
    scoreText.textContent = `Your Score: ${userScore} out of ${questions.length}`;

    const circularProgress = document.querySelector('.circular_progress');
    const progressValue = document.querySelector('.progress_value');
    let progressStartValue = -1;
    let progressEndValue = (userScore / questions.length) * 100;
    let speed = 20;

    let progress = setInterval(() => {
        progressStartValue++;

        progressValue.textContent = `${progressStartValue}%`;
        circularProgress.style.background = `conic-gradient(darkgreen ${progressStartValue * 3.6}deg, rgb(0, 36, 0) 0deg)`;

        if (progressStartValue == progressEndValue) {
        clearInterval(progress);
        }
    }, speed);
}

function sendResults() {
    let thisScore = userScore*10;
    console.log(thisScore, "USERSCORE**********")
    $.ajax({
        url: '/process',
        type: 'POST',
        data: {'score': thisScore},
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    })
}