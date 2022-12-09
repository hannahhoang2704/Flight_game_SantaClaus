'use strict';

//start game page_ index.html

const search = document.getElementById('start');                //button to fetch all the airports in chosen city
const city = document.getElementById('city');                   //input of city
const div_ICAO = document.getElementById('ICAO-fetch');          //div contain all the ICAO element
const ICAO_p = document.createElement('p');                     //Message to player after choose the city

//game status update
const nameUpdate = document.getElementById('player-name');
const giftsUpdate = document.getElementById('gifts');
const currentco2Update = document.getElementById('consumed');
const distanceToRov = document.getElementById('distance-to-rovaniemi');

//airport weather
const temperature = document.getElementById('airport-temp');
const weatherCondition = document.getElementById('airport-conditions');
const windSpeed = document.getElementById('airport-wind');
const weatherIcon = document.getElementById('weather-icon');

let icao_start;                       //ICAO of the depature airport
const icao_rovaniemi = 'EFRO';               //ICAO of Rovaniemi
let distanceTotal;
let currentAirport = ' ';
let currentAirport_long;
let currentAirport_lat;

//main-game
const questionUpdate = document.getElementById('question');
const mainGameDiv = document.getElementById('main-program');
let correctAnswer;

//Add maps

let map;

function drawMapWithMarker(pos, icao) {
  // Use the leaflet.js library to show the location on the map (https://leafletjs.com/)
  // first the map itself if it has not been created before
  if (map == null) {
    map = L.map('map');
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);
  }
  map.setView(pos, 13);

  // then the marker
  L.marker(pos).addTo(map).bindPopup(icao).openPopup();
}

// function to update the game status
function updateGameStatus(screen_name, gifts, currentco2) {
  nameUpdate.innerText = `Player name: ${screen_name}`;
  giftsUpdate.innerText = gifts;
  currentco2Update.innerText = currentco2;
}

//function to update the weather in HTML
function updateWeather(temp, condition, wind, icon) {
  temperature.innerHTML = `<span>${temp}°C</span>`;
  weatherCondition.innerHTML = `<span>${condition}</span>`;
  windSpeed.innerHTML = `<span>${wind} m/s</span>`;
  weatherIcon.src = 'https://openweathermap.org/img/wn/' + str(icon) +
      '@2x.png';
}

//change the quiz in main program div
function quiz(question_screen) {
  questionUpdate.innerText = `Question: ${question_screen}`;

}

//fetch the airport info(ICAO, name, long, lat) where you want to flight to
async function getAirportPosition(icao) {
  try {

    const userName = document.querySelector('#user-name').value;
    document.getElementById(
        'welcome').innerText = `Hi ${userName}, let's start your journey!`;
    const response = await fetch(
        'http://127.0.0.1:5100/gamerinfo?name=' + userName + '&location=' +
        icao);    // starting data download, fetch returns a promise which contains an object of type 'response'
    const jsonData = await response.json();          // retrieving the data retrieved from the response object using the json() function
    const pos = [jsonData.airport.Lat, jsonData.airport.Long];                                  // create position array for leaflet library
    console.log(jsonData);     // log the result to the console
    console.log(jsonData.airport.Name, jsonData.airport.Lat,
        jsonData.airport.Long);

    // Show the airport name to the screen
    currentAirport = jsonData.airport.Name;
    console.log('current airport: ' + currentAirport);
    currentAirport_lat = jsonData.airport.Lat;
    currentAirport_long = jsonData.airport.Long;

    //Add current airport name in Airport name h2
    const airportUpdateName = document.getElementById('airport-name');
    airportUpdateName.innerHTML = `<span>${currentAirport}</span>`;

    //update player name,gifts and co2 consumption
    const screen_name = jsonData.screen_name;
    let gifts = jsonData.gifts;
    let currentco2 = jsonData.co2_consumed;
    updateGameStatus(screen_name, gifts, currentco2);

    // and draw the map
    drawMapWithMarker(pos, icao);

    //fetch weather of the airport
    const responseWeather = await fetch(
        'http://127.0.0.1:5100/weather?lat=' + currentAirport_lat + '&long=' +
        currentAirport_long);    // starting data download, fetch returns a promise which contains an object of type 'response'
    const jsonDataWeather = await responseWeather.json();
    console.log(jsonDataWeather);               // JsonDataweather objects
    updateWeather(jsonDataWeather.temperature, jsonDataWeather.description,
        jsonDataWeather.wind, jsonDataWeather.icon);      //update weather

    return jsonDataWeather;
  } catch (error) {
    console.log(error.message);
  } finally {                                         // finally = this is executed anyway, whether the execution was successful or not
    console.log('asynchronous load complete');
  }
}
async function co2Consumed(distance){
      const response = await fetch(
        'http://127.0.0.1:5100/co2consumed/'+ distance);    // starting data download, fetch returns a promise which contains an object of type 'response'
      const jsonData = await response.json();
      console.log(jsonData)
      currentco2Update.innerText = jsonData;
      return jsonData
    }

//get distance between 2 airport
async function getAirportDistance(icao_start, icao_end) {
  try {
    const response = await fetch(
        'http://127.0.0.1:5100/airportdistance?start=' + icao_start + '&end=' + icao_end);    // starting data download, fetch returns a promise which contains an object of type 'response'
    const jsonData = await response.json();          // retrieving the data retrieved from the response object using the json() function
    console.log(jsonData);
    //drawMapWithLine(jsonData.start, jsonData.end)
    distanceTotal = jsonData.dist;     // log the result to the console
    distanceToRov.innerHTML = `${jsonData.dist}`;
    return jsonData;
  } catch (error) {
    console.log(error.message);
  }

}

//Fetch the quiz game
async function fetch_question_quiz() {
  try {
      const response = await fetch('http://127.0.0.1:5100/quiz');    // starting data download, fetch returns a promise which contains an object of type 'response'
      const quizData = await response.json();          // retrieving the data retrieved from the response object using the json() function
      console.log(quizData);
      console.log(quizData.question);     // log the result to the console
      const question_screen = quizData.question;
      correctAnswer = quizData.answer;
      quiz(question_screen);

    return question_screen ;
  } catch (error) {
    console.log(error.message);
  } finally {                                         // finally = this is executed anyway, whether the execution was successful or not
    //console.log("log get airport distance")
  }
};

//check answer of the quiz
async function checkAnswer(){
  const answerSelect = document.getElementById('answer-select');          //get the ICAO number of the chosen airport
  const playerAnswer = answerSelect.options[answerSelect.selectedIndex].value;
  console.log(playerAnswer)
  if (playerAnswer == correctAnswer){
      console.log('Correct answer');
      mainGameDiv.innerHTML = `Congrats! Your answer is correct. We send you some treasure box. Check your gifts now!`;
  }else{
    console.log('Wrong answer');
    mainGameDiv.innerHTML = `Oops! Your answer is wrong. Sadly your gifts also got robbed! `;
  }
}

//push true,false options and button for quiz game
function pushQuiz(){
  const selectForQuiz = document.createElement('select');
  selectForQuiz.setAttribute('id', 'answer-select')
  const optionTrue = document.createElement('option');
  const optionFalse = document.createElement('option');
  optionTrue.innerHTML = `True`;
  optionTrue.value = 'true';
  optionFalse.innerHTML = `False`;
  optionFalse.value = 'false';
  selectForQuiz.appendChild(optionTrue);
  selectForQuiz.appendChild(optionFalse);
  const quizButton = document.createElement('button');
  mainGameDiv.appendChild(selectForQuiz)
  quizButton.appendChild(document.createTextNode('Submit'));
  mainGameDiv.appendChild(quizButton);
  quizButton.addEventListener('click', checkAnswer)
};

//Check how far from departure airport to Rovaniemi
async function airport_start(evt) {
  evt.preventDefault();
  const selectOption = document.getElementById('airport-fetch');          //get the ICAO number of the chosen airport
  icao_start = selectOption.options[selectOption.selectedIndex].value;              //get value of selected option in <select> element!!!
  //console.log(icao_start);

  await getAirportPosition(icao_start); //fetch the departure airport info

  await getAirportDistance(icao_start, icao_rovaniemi);
  await co2Consumed(distanceTotal);
  await fetch_question_quiz();

  pushQuiz();

}

//All the airports are listed after player choose the city
function airportOptions(jsonData) {
  ICAO_p.innerText = 'List of airports:';                                 //Make a dropdrown list of depature airports
  div_ICAO.appendChild(ICAO_p);
  const select = document.createElement('select');
  select.setAttribute('id', 'airport-fetch');
  div_ICAO.appendChild(select);
  for (let i = 0; i < jsonData.length; i++) {
    const airport_options = document.createElement('option');                   //options for airport drop down list
    airport_options.setAttribute('value', `${jsonData[i]['ICAO']}`);
    airport_options.appendChild(
        document.createTextNode(`${jsonData[i]['Airport name']}`));
    select.appendChild(airport_options);
  }
  const button_airport = document.createElement('button');      //Button to choose the departure airport
  button_airport.appendChild(document.createTextNode('Take off!'));
  button_airport.setAttribute('id', 'button-airport');

  div_ICAO.appendChild(button_airport);

////////////////post method to get ICAO of airport to flask server!!!!

  button_airport.addEventListener('click', airport_start);           //click button to choose the departure airport
}

//fetch all the airports in the chosen city
function fetch_airport(evt) {
  evt.preventDefault();
  airportFetches();
}

async function airportFetches() {                 // asynchronous function is defined by the async keyword
  div_ICAO.innerHTML = '';                        //empty the select option of game
  try {                                               // error handling: try/catch/finally
    //console.log(city.value);
    const response = await fetch('http://127.0.0.1:5100/' + city.value);    // starting data download, fetch returns a promise which contains an object of type 'response'
    const jsonData = await response.json();          // retrieving the data retrieved from the response object using the json() function
    //console.log(jsonData[0]['Airport name']);

    airportOptions(jsonData);
  } catch (error) {
    console.log(error.message);
    ICAO_p.innerText = `City can not found! Choose another city.`;        //inform the city is not in database
    div_ICAO.appendChild(ICAO_p);

  } finally {                                         // finally = this is executed anyway, whether the execution was successful or not
  }
}

//call-back function to fetch all airport in chosen city
search.addEventListener('click', fetch_airport);

