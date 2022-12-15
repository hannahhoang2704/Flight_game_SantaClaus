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
let distanceToRov = document.getElementById('distance-to-rovaniemi');
let distanceFromLastt = document.getElementById('dist-from-last');


//airport weather
const temperature = document.getElementById('airport-temp');
const weatherCondition = document.getElementById('airport-conditions');
const windSpeed = document.getElementById('airport-wind');
const weatherIcon = document.getElementById('weather-icon');

let icao_start;                       //ICAO of the depature airport
const icao_rovaniemi = 'EFRO';        //ICAO of Rovaniemi
const pos_Rov = [66.565, 25.83];
let distanceTotal;
let newICAO;
let degrees;
let currentAirport = ' ';
let currentAirportICAO;
let currentAirport_long;
let currentAirport_lat;
let gifts;
let round = 5;

//main-game
const mainProgramDiv = document.getElementById('main-program');
const questionUpdate = document.getElementById('question');
const answerSelection = document.getElementById('answer-selection');
let correctAnswer;

//Rock Paper Scicssors
const rps_div = document.getElementById('rps');

// Next destination button
const next_destination = document.getElementById('next-destination');

//update gifts
//giftsUpdate.innerText = gifts;

//Add maps
let map;

function drawMapWithMarker(pos, icao) {
  // Use the leaflet.js library to show the location on the map (https://leafletjs.com/)
  // first the map itself if it has not been created before
  if (map == null) {
    map = L.map('map', {
      minZoom: 2,
      maxZoom: 3,
    });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);
  }
  map.setView(pos, 100);

  // then the marker
  L.marker(pos).addTo(map).bindPopup(icao).openPopup();
}

function drawMapWithMarkerRovaniemi(pos_Rov, icao_rovaniemi) {
  // Use the leaflet.js library to show the location on the map (https://leafletjs.com/)
  // first the map itself if it has not been created before
  if (map == null) {
    map = L.map('map');
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);
  }
  map.setView(pos_Rov, 100);

  // then the marker
  L.marker(pos_Rov).addTo(map).bindPopup('Santa\'s House').openPopup();
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
  weatherIcon.src = `https://openweathermap.org/img/wn/${icon}@2x.png`;
  console.log(weatherIcon.src);
}

//fetch the airport info(ICAO, name, long, lat) where you want to flight to
async function getAirportPosition(icao) {
  try {

    const userName = document.querySelector('#user-name').value;
    //document.getElementById('welcome').innerText = `Hi ${userName}, let's start your journey!`;
    const response = await fetch(
        'http://127.0.0.1:5000/gamerinfo?name=' + userName + '&location=' +
        icao);    // starting data download, fetch returns a promise which contains an object of type 'response'
    const jsonData = await response.json();          // retrieving the data retrieved from the response object using the json() function
    const pos = [jsonData.airport.Lat, jsonData.airport.Long];                                  // create position array for leaflet library
    console.log(jsonData);                                                              // log the result to the console
    //console.log(jsonData.airport.Name, jsonData.airport.Lat,jsonData.airport.Long);

    // Show the airport name to the screen
    currentAirport = jsonData.airport.Name;
    currentAirportICAO = jsonData.location;
    console.log('current airport ICAO: ' + currentAirportICAO);
    console.log('current airport: ' + currentAirport);
    currentAirport_lat = jsonData.airport.Lat;
    currentAirport_long = jsonData.airport.Long;

    //Add current airport name in Airport name h2
    const airportUpdateName = document.getElementById('airport-name');
    airportUpdateName.innerHTML = `<span>${currentAirport}</span>`;

    //update player name,gifts and co2 consumption
    const screen_name = jsonData.screen_name;
    gifts = jsonData.gifts;
    console.log(gifts);
    let currentco2 = jsonData.co2_consumed;
    updateGameStatus(screen_name, gifts, currentco2);

    // and draw the map
    drawMapWithMarker(pos, icao);
    drawMapWithMarkerRovaniemi(pos_Rov, icao_rovaniemi);

    //fetch weather of the airport
    const responseWeather = await fetch(
        'http://127.0.0.1:5000/weather?lat=' + currentAirport_lat + '&long=' +
        currentAirport_long);    // starting data download, fetch returns a promise which contains an object of type 'response'
    const jsonDataWeather = await responseWeather.json();
    console.log(jsonDataWeather);               // JsonDataweather objects
    console.log(jsonDataWeather.icon);
    updateWeather(jsonDataWeather.temperature, jsonDataWeather.description,
        jsonDataWeather.wind, jsonDataWeather.icon);      //update weather

    return jsonDataWeather;
  } catch (error) {
    console.log(error.message);
  } finally {                                         // finally = this is executed anyway, whether the execution was successful or not
    console.log('asynchronous load complete');
  }
}

////////////////////////////////
async function newAirportPosition(icao) {

  try {

    const response = await fetch(
        'http://127.0.0.1:5000/airport/' + icao);    // starting data download, fetch returns a promise which contains an object of type 'response'
    const jsonData = await response.json();          // retrieving the data retrieved from the response object using the json() function
    const pos = [jsonData.Lat, jsonData.Long];                                  // create position array for leaflet library
    console.log(jsonData);

    //let pos = [degrees];                                  // create position array for leaflet library
    console.log(pos, 'kakakakakakkka');                                                              // log the result to the console
    //console.log(jsonData.airport.Name, jsonData.airport.Lat,jsonData.airport.Long);

    // Show the airport name to the screen
    currentAirport = jsonData.Location;
    console.log('current airport: ' + currentAirport);
    currentAirport_lat = jsonData.Lat;
    currentAirport_long = jsonData.Long;


    //Add current airport name in Airport name h2
    const airportUpdateName = document.getElementById('airport-name');
    airportUpdateName.innerHTML = `<span>${currentAirport}</span>`;

    //update player name,gifts and co2 consumption
    const screen_name = jsonData.screen_name;
    gifts = jsonData.gifts;
    console.log(gifts);
    let currentco2 = jsonData.co2_consumed;
    updateGameStatus(screen_name, gifts, currentco2);

    // and draw the map
    drawMapWithMarker(pos, icao);
    drawMapWithMarkerRovaniemi(pos_Rov, icao_rovaniemi);

    //fetch weather of the airport
    const responseWeather = await fetch(
        'http://127.0.0.1:5000/weather?lat=' + currentAirport_lat + '&long=' +
        currentAirport_long);    // starting data download, fetch returns a promise which contains an object of type 'response'

    const jsonDataWeather = await responseWeather.json();
    console.log(jsonDataWeather);               // JsonDataweather objects
    console.log(jsonDataWeather.icon);
    updateWeather(jsonDataWeather.temperature, jsonDataWeather.description,
        jsonDataWeather.wind, jsonDataWeather.icon);      //update weather

    return jsonDataWeather;
  } catch (error) {
    console.log(error.message);
  } finally {                                         // finally = this is executed anyway, whether the execution was successful or not
    console.log('asynchronous load complete');
  }
}

async function co2Consumed(distance) {
  const response = await fetch(
      'http://127.0.0.1:5000/co2consumed/' + distance);    // starting data download, fetch returns a promise which contains an object of type 'response'
  const jsonData = await response.json();
  console.log(jsonData);
  currentco2Update.innerText = jsonData;
  return jsonData;
};

//get distance between 2 airport
async function getAirportDistance(icao_start, icao_end) {
  try {
    const response = await fetch(
        'http://127.0.0.1:5000/airportdistance?start=' + icao_start + '&end=' +
        icao_end);    // starting data download, fetch returns a promise which contains an object of type 'response'
    const jsonData = await response.json();          // retrieving the data retrieved from the response object using the json() function
    console.log(jsonData);
    drawMapWithLine(jsonData.start, jsonData.end);
    distanceTotal = jsonData.dist;     // log the result to the console
    distanceToRov.innerHTML = `${jsonData.dist}`;
    return jsonData;
  } catch (error) {
    console.log(error.message);
  }
}

/*
//fetch countdown Christmas API
async function addCountDown(){
  try {
    const response = await fetch('http://127.0.0.1:5000/countdown');    // starting data download, fetch returns a promise which contains an object of type 'response'
    const countDownData = await response.json();          // retrieving the data retrieved from the response object using the json() function
    console.log(countDownData);
    const statement = countDownData.statement;
    document.getElementById('count-down').innerText = statement;
  } catch (error) {
    console.log(error.message);
  }
}*/

//type effect
/*function type_effect(text, id) {
  let i = 0;
  let txt = `Do you think: ${text}`;
  var speed = 70;
  typeWriter();

  function typeWriter() {
    if (i < txt.length) {
      document.getElementById(`${id}`).innerHTML += txt.charAt(i);
      i++;
      setTimeout(typeWriter, speed);
    }
  }
}*/

//change the quiz in main program div
function quiz(question_screen) {
  questionUpdate.innerHTML = `Answer the question below: <br> ${question_screen}`;

}

//Fetch the quiz game
async function fetch_question_quiz() {
  try {
    const response = await fetch('http://127.0.0.1:5000/quiz');    // starting data download, fetch returns a promise which contains an object of type 'response'
    const quizData = await response.json();          // retrieving the data retrieved from the response object using the json() function
    console.log(quizData);
    //console.log(quizData.question);                // log the result to the console
    const question_screen = quizData.question;
    correctAnswer = quizData.answer;
    answerSelection.innerHTML = '';
    //type_effect(question_screen, 'question');
    quiz(question_screen);
    return question_screen;
  } catch (error) {
    console.log(error.message);
  }
};

//update the gifts by deduct or add the gifts
function mathForGifts(changeValue) {
  gifts = (parseInt(gifts) + parseInt(changeValue));
  giftsUpdate.innerText = gifts;
  return gifts;
}

//fetch gifts amount back to database and server
async function updateGiftsInDB(gifts) {
  try {
    const response = await fetch('http://127.0.0.1:5000/updategifts/' + gifts);    // starting data download, fetch returns a promise which contains an object of type 'response'
    const giftData = await response.json();          // retrieving the data retrieved from the response object using the json() function
    return giftData;
  } catch (error) {
    console.log(error.message);
  }
};

//fetch the reward/robbery that affect gift change from Database
async function changeGift(change) {
  try {
    const response = await fetch('http://127.0.0.1:5000/giftschange/' + change);    // starting data download, fetch returns a promise which contains an object of type 'response'
    const giftChangeData = await response.json();          // retrieving the data retrieved from the response object using the json() function
    console.log(giftChangeData);
    await mathForGifts(giftChangeData);
    console.log(gifts);
    await updateGiftsInDB(gifts);
  } catch (error) {
    console.log(error.message);
  }
};

//check answer of the quiz
async function checkAnswer() {
  const answerSelect = document.getElementById('answer-select');          //get the ICAO number of the chosen airport
  const playerAnswer = answerSelect.options[answerSelect.selectedIndex].value;
  console.log(playerAnswer);
  console.log(gifts);
  if (playerAnswer == correctAnswer) {
    //console.log('Correct answer');
    answerSelection.innerHTML = `Congrats! Your answer is correct. We send you some treasure box. Check your gifts now!`;
    changeGift('add');
  } else {
    //console.log('Wrong answer');
    answerSelection.innerHTML = `Oops! Your answer is wrong. Sadly your gifts also got robbed! `;
    changeGift('deduct');
  }

  const next_button = document.createElement('button');
  next_button.innerHTML = 'Next challenge';
  next_button.setAttribute('class', 'game-btn');
  document.getElementById('next-btn').appendChild(next_button);
  next_button.addEventListener('click', rock_paper_scissors);
  next_button.onclick = function() {
    document.getElementById('next-btn').innerHTML = '';
    document.getElementById('answer-selection').innerHTML = '';
  };

}

//push true,false options and button for quiz game
function pushQuiz() {
  const selectForQuiz = document.createElement('select');
  selectForQuiz.setAttribute('id', 'answer-select');
  const optionTrue = document.createElement('option');
  const optionFalse = document.createElement('option');
  optionTrue.innerHTML = `True`;
  optionTrue.value = 'true';
  optionFalse.innerHTML = `False`;
  optionFalse.value = 'false';
  selectForQuiz.appendChild(optionTrue);
  selectForQuiz.appendChild(optionFalse);
  const quizButton = document.createElement('button');
  quizButton.setAttribute('class', 'game-btn');
  answerSelection.appendChild(selectForQuiz);
  quizButton.appendChild(document.createTextNode('Submit'));
  answerSelection.appendChild(quizButton);
  quizButton.addEventListener('click', checkAnswer);
  quizButton.onclick = function() {
    document.getElementById('question').innerHTML = '';
  };
}

//Rock paper scissor
function rock_paper_scissors() {

  rps_div.innerHTML = '<p>Let\'s play rock paper scissors:</p><br>';
  const selectRps = document.createElement('select');
  selectRps.setAttribute('id', 'select-rps');
  rps_div.appendChild(selectRps);
  const rock = document.createElement('option');
  rock.innerText = 'Rock';
  rock.value = '0';
  selectRps.appendChild(rock);
  const paper = document.createElement('option');
  paper.innerHTML = 'Paper';
  paper.value = '1';
  selectRps.appendChild(paper);
  const scissor = document.createElement('option');
  scissor.innerHTML = 'Scissor';
  scissor.value = '2';
  selectRps.appendChild(scissor);
  const rpsButton = document.createElement('button');
  rpsButton.setAttribute('class', 'game-btn');
  rpsButton.innerText = 'Submit';
  rps_div.appendChild(rpsButton);
  rpsButton.addEventListener('click', rpsExecute);
}

//fetch the computer options in RPS game
async function checkComputerOption(playerValue) {                 // asynchronous function is defined by the async keyword
  try {                                               // error handling: try/catch/finally
    const response = await fetch(
        'http://127.0.0.1:5000/rpsgame/' + playerValue);    // starting data download, fetch returns a promise which contains an object of type 'response'
    const jsonData = await response.json();          // retrieving the data retrieved from the response object using the json() function
    console.log(jsonData);
    console.log(jsonData.computerChoice, jsonData.status, jsonData.result);
    const fetchResultDiv = document.getElementById('fetch-result-div');
    const p = document.createElement('p');
    p.appendChild(document.createTextNode('Computer chooses: '));
    fetchResultDiv.appendChild(p);
    const compValue = parseInt(jsonData.compImg);
    const imgPlayerOption = document.createElement('img');
    imgPlayerOption.src = `image/game-image/rock-paper-scissors/${compValue}.png`;
    fetchResultDiv.appendChild(imgPlayerOption);
    const h2 = document.createElement('h2');
    h2.setAttribute('id', 'rps-statement');
    h2.appendChild(document.createTextNode(
        `${jsonData.result}. Check your gifts update!`));
    const button_destination = document.createElement('button');
    h2.appendChild(button_destination);
    //button_destination.innerHTML = 'Next destination';

    mainProgramDiv.appendChild(h2);
    if (jsonData.status == -1) {
      changeGift('deduct');
    } else if (jsonData.status == 1) {
      changeGift('add');
    }
    return jsonData;
  } catch (error) {
    console.log(error.message);
  }
}

function showRpsResult() {
  const gameResultDiv = document.createElement('div');
  rps_div.appendChild(gameResultDiv);
  const button_destination = document.createElement('button');
  rps_div.appendChild(button_destination);
  button_destination.innerHTML = 'Next destination';
  button_destination.addEventListener('click', loopNextStop)
  button_destination.onclick = function(){
    document.getElementById('rps').innerHTML = "";
    document.getElementById('rps-statement').innerHTML = "";
  }
}

//when button is clicked, collect the player's option in RPS game and compare with Computer game
async function rpsExecute(evt) {

  evt.preventDefault();
  const fetchResultDiv = document.createElement('div');
  fetchResultDiv.setAttribute('id', 'fetch-result-div');
  rps_div.appendChild(fetchResultDiv);
  fetchResultDiv.innerHTML = '';
  const p = document.createElement('p');
  p.appendChild(document.createTextNode('You\'ve choose: '));
  fetchResultDiv.appendChild(p);
  const selectRps = document.getElementById('select-rps');
  const playerValue = selectRps.options[selectRps.selectedIndex].value;
  console.log(playerValue);
  const imgPlayerOption = document.createElement('img');
  imgPlayerOption.src = `image/game-image/rock-paper-scissors/${playerValue}.png`;
  fetchResultDiv.appendChild(imgPlayerOption);
  console.log(playerValue);
  await checkComputerOption(playerValue);
  await showRpsResult();
};

//Check how far from departure airport to Rovaniemi
async function airport_start(evt) {
  evt.preventDefault();
  const selectOption = document.getElementById('airport-fetch');          //get the ICAO number of the chosen airport
  icao_start = selectOption.options[selectOption.selectedIndex].value;              //get value of selected option in <select> element!!!
  await getAirportPosition(icao_start); //fetch the departure airport info
  await getAirportDistance(icao_start, icao_rovaniemi);
  await co2Consumed(distanceTotal);

  //await addCountDown();
  await fetch_question_quiz();
  pushQuiz();
}

/* draw the map with two positions and a line between them */
function drawMapWithLine(start_pos, end_pos) {
  // draw the line, http://leafletjs.com/reference.html#polyline
  let latlngs = Array();
  latlngs.push(start_pos);
  latlngs.push(end_pos);
  const polyline = L.polyline(latlngs, {color: 'red'}).addTo(map);

  // then scale the map to fit the line
  map.fitBounds(polyline.getBounds());
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
  button_airport.setAttribute('class', 'game-btn');
  button_airport.appendChild(document.createTextNode('Take off!'));
  button_airport.setAttribute('id', 'button-airport');
  div_ICAO.appendChild(button_airport);
  button_airport.addEventListener('click', airport_start); //click button to choose the departure airport
  button_airport.onclick = function() {
    document.getElementById('user-info').innerHTML = '';
  };
}

function loopNextStop() {
  findNextAirport(currentAirportICAO);

  //game over
  if (gifts <= 0 || round== 0){
  alert('Game over!');
  location = 'Exit.html';
}

};

// SELECT NEXT AIRPORT TO FLY TO

async function findNextAirport(icao) {
  try {
    const response = await fetch(
        'http://127.0.0.1:5000/next_airport/' + icao);    // starting data download, fetch returns a promise which contains an object of type 'response'
    const jsonData = await response.json();          // retrieving the data retrieved from the response object using the json() function
    console.log(jsonData, 'vavavavav');
    //drawMapWithLine(jsonData.start, jsonData.end);
    degrees = jsonData.Degrees;
    distanceTotal = jsonData.DistanceToRoi;
    round = jsonData.Round;
    console.log(round)
    newICAO = jsonData.ICAO;
    currentAirportICAO = jsonData.ICAO;
    currentAirport = jsonData.Name;

    distanceFromLastt = jsonData.DistanceFromLast;
    console.log(degrees);
    console.log(newICAO);
    console.log(currentAirport);
    console.log(currentAirportICAO);
    console.log(currentAirport_lat);
    console.log(currentAirport_long);

    currentAirport_lat = degrees[0];
    currentAirport_long = degrees[1];
    console.log(currentAirport_lat);
    console.log(currentAirport_long);


    const airportUpdateName = document.getElementById('airport-name');
    airportUpdateName.innerHTML = `<span>${currentAirport}</span>`;
    drawMapWithMarker(degrees, currentAirportICAO);
    drawMapWithMarkerRovaniemi(pos_Rov, icao_rovaniemi);

    //fetch weather of the airport
    const responseWeather = await fetch(
        'http://127.0.0.1:5000/weather?lat=' + currentAirport_lat + '&long=' +
        currentAirport_long);    // starting data download, fetch returns a promise which contains an object of type 'response'

    const jsonDataWeather = await responseWeather.json();
    console.log(jsonDataWeather);               // JsonDataweather objects
    console.log(jsonDataWeather.icon);
    updateWeather(jsonDataWeather.temperature, jsonDataWeather.description,
        jsonDataWeather.wind, jsonDataWeather.icon);      //update weather

    game();

    //newAirportPosition(newICAO);
  } catch (error) {
    console.log(error.message);
  }

};

//fetch all the airports in the chosen city
function fetch_airport(evt) {
  evt.preventDefault();
  airportFetches();
}

async function airportFetches() {                 // asynchronous function is defined by the async keyword
  div_ICAO.innerHTML = '';                        //empty the select option of game
  try {                                               // error handling: try/catch/finally
    //console.log(city.value);
    const response = await fetch('http://127.0.0.1:5000/' + city.value);    // starting data download, fetch returns a promise which contains an object of type 'response'
    const jsonData = await response.json();          // retrieving the data retrieved from the response object using the json() function
    //console.log(jsonData[0]['Airport name']);

    airportOptions(jsonData);
  } catch (error) {
    console.log(error.message);
    ICAO_p.innerText = `City can not found! Choose another city.`;        //inform the city is not in database
    div_ICAO.appendChild(ICAO_p);

  }
}

//call-back function to fetch all airport in chosen city
search.addEventListener('click', fetch_airport);

//Game over when there's no gift


async function game() {
  await fetch_question_quiz();
  await pushQuiz();
}
