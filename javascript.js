'use strict';

//start game page_ index.html

const playerNameButton = document.getElementById('name-button');
const playerName = document.querySelector('#username-form');        //username's form
const search = document.getElementById('start');                //button to fetch all the airports in chosen city
const city = document.getElementById('city');                   //input of city
const div_ICAO = document.getElementById('ICAO-fetch')          //div contain all the ICAO element
const ICAO_p = document.createElement('p');                     //Message to player after choose the city
let departureAirport;                   //departure airport name
let icao_start;                       //ICAO of the depature airport
const icao_rovaniemi = 'EFRO';               //ICAO of Rovaniemi
let currentAirport;






//retrieve player's name in database
function get_player_name(evt){
  evt.preventDefault();
  const name = document.querySelector('#user-name').value;
  document.getElementById('welcome').innerText = `Hi ${playerName.value}, let's start your journey!`;
  async function player_name(){
    try{
      const gameData = await fetch('http://127.0.0.1:3000/')
    }catch(error){
      console.log(error);
    }
  }
}
playerName.addEventListener('submit', get_player_name);


//Greeting to player
/*playerNameButton.addEventListener('click', ()=>{
  document.getElementById('welcome').innerText = `Hi ${playerName.value}, let's start your journey!`;
})*/

//fetch the airport info where you want to flight to
async function getAirportPosition(icao){
  try {
          const response = await fetch('http://127.0.0.1:3000/airport/' + icao);    // starting data download, fetch returns a promise which contains an object of type 'response'
          const jsonData = await response.json();          // retrieving the data retrieved from the response object using the json() function
          const pos = [jsonData.Lat, jsonData.Long];                                  // create position array for leaflet library
          console.log(jsonData.ICAO, jsonData.Name, jsonData.Lat, jsonData.Long);     // log the result to the console

          // Show the airport name to the screen
          currentAirport = jsonData.Name;
          console.log('current airport:' + currentAirport)
          // and draw the map
          //drawMapWithMarker(pos, icao)

      } catch (error) {
          console.log(error.message);
      } finally {                                         // finally = this is executed anyway, whether the execution was successful or not
          console.log('asynchronous load complete');
      }
  }


//get distance between 2 airport
async function getAirportDistance(icao_start, icao_end) {
    let jsonData;

    try {
        const response = await fetch('http://127.0.0.1:3000/airportdistance?start=' + icao_start + '&end=' + icao_end);    // starting data download, fetch returns a promise which contains an object of type 'response'
        jsonData = await response.json();          // retrieving the data retrieved from the response object using the json() function
        //drawMapWithLine(jsonData.start, jsonData.end)
        console.log(jsonData.dist);     // log the result to the console
    } catch (error) {
        console.log(error.message);
    } finally {                                         // finally = this is executed anyway, whether the execution was successful or not
        return jsonData.dist
    }
};

//promise 2 asynchronous
async function run_process(){
  let res;
  try{
    res = await Promise.all([
       getAirportPosition(icao_start),
       getAirportPosition(icao_rovaniemi),
    ]);
       console.log('Success>>', res);
  } catch(err){
    console.log('Fail>>', res, err);
  }
}

//Check how far from departure airport to Rovaniemi
function airport_start(evt){
  evt.preventDefault();
  const selectOption = document.getElementById('airport-fetch');          //get the ICAO number of the chosen airport
  icao_start = selectOption.options[selectOption.selectedIndex].value;
  console.log(icao_start);

  getAirportPosition(icao_start);                                                  //fetch the departure airport info
  //getAirportPosition(icao_rovaniemi);                                               //fetch the info of Rovaniemi airport
  // airport_route();
}



function airport_route() {
  getAirportDistance(icao_start, icao_rovaniemi).then(function(distance) {
   console.log('Distance = ' + distance + 'km')
  })
}



//All the airports are listed after player choose the city
function airportOptions(jsonData){
  ICAO_p.innerText = 'List of airports:';                                 //Make a dropdrown list of depature airports
  div_ICAO.appendChild(ICAO_p);
  const select = document.createElement('select');
  select.setAttribute('id', 'airport-fetch')
  div_ICAO.appendChild(select)
  for (let i = 0; i <jsonData.length; i++){
    const airport_options = document.createElement('option');
    airport_options.setAttribute('value', `${jsonData[i]['ICAO']}`);
    airport_options.appendChild(document.createTextNode(`${jsonData[i]['Airport name']}`));
    select.appendChild(airport_options);
  }
  const button_airport = document.createElement('button');      //Button to choose the departure airport
  button_airport.appendChild(document.createTextNode('Take off!'));
  button_airport.setAttribute('id', 'button-airport')
  div_ICAO.appendChild(button_airport);

////////////////post method to get ICAO of airport

  button_airport.addEventListener('click', airport_start)           //click button to choose the departure airport
}




//fetch all the airports in the chosen city
function fetch_airport(evt){
  evt.preventDefault();
  airportFetches();
}

async function airportFetches() {                 // asynchronous function is defined by the async keyword
        div_ICAO.innerHTML = "";
        console.log('asynchronous download begins');
        try {                                               // error handling: try/catch/finally
            console.log(city.value);
            const response = await fetch('http://127.0.0.1:3000/' + city.value);    // starting data download, fetch returns a promise which contains an object of type 'response'
            const jsonData = await response.json();          // retrieving the data retrieved from the response object using the json() function
            console.log(jsonData[0]['Airport name']);

            airportOptions(jsonData);
        } catch (error) {
            console.log(error.message);
            ICAO_p.innerText = `City can not found! Choose another city.`;        //inform the city is not in database
            div_ICAO.appendChild(ICAO_p);

        } finally {                                         // finally = this is executed anyway, whether the execution was successful or not
            console.log('asynchronous load complete');
        }
    }

//call-back function to fetch all airport in chosen city
search.addEventListener('click', fetch_airport);

