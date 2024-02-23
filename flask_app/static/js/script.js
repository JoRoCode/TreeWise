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



// Function for the Popup Quiz

const startButton = document.querySelector('.start_button');
const popupQuiz = document.querySelector('.popup_quiz');

// startButton.onclick = () => {
//     popupQuiz.classList.add('active');
// }


const startQuiz = () => {
    const popupQuiz = document.getElementById('.popup_quiz')
    popupQuiz.classList.add("active")
}