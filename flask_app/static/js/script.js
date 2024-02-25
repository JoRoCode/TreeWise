// Function for the update comment popup

const showForm = id => {
    const form = document.getElementById(`popup_container${id}`)
    form.classList.add("active")
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
    document.querySelector('.popup_quiz').classList.add("active");
    document.querySelector('.header').classList.add("active");
}
// Function to remove the popup quiz
function stopQuiz(){
    document.querySelector('.popup_quiz').classList.remove("active");
    document.querySelector('.header').classList.remove("active");

}

function continueQuiz(){
    document.querySelector('.quiz_section').classList.add("active");
    document.querySelector('.popup_quiz').classList.remove("active");
    document.querySelector('.header').classList.remove("active");
    document.querySelector('.quiz_box').classList.add("active");
    showQuestions(0);
}

let questionCount = 0;

function nextQuestion(){
document.querySelector('.next_button');
questionCount++;
showQuestions(questionCount)
}

function showQuestions(index) {
    const questionText = document.querySelector('.question_text');
    questionText.textcontent =`${question[index].numb}. ${questions[index].question}`;
}