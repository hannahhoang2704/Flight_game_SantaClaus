'use strict';

//start game page_ index.html

const playerNameButton = document.getElementById('name-button');
const playerName = document.querySelector('#user-name');        //input player's name
const search = document.getElementById('start');                //button to fetch all the airports in chosen city
const city = document.getElementById('city');                   //input of city
//const airport_options = document.getElementById('airport-fetch');//select element where all options of airports are listed
const div_ICAO = document.getElementById('ICAO-fetch')          //div contain all the ICAO element
const ICAO_p = document.createElement('p');                     //Message to player after choose the city

console.log(playerName.value);
//post method
async function get_player_name(evt){
  evt.preventDefault();
  const data = {
    body: JSON.stringify({
      name: document.getElementById('user-name').value
    }),
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
  }
  try{
    const response = await fetch('http://127.0.0.1:3000/', data);
    if(!response.ok) throw new Error('Invalid input');
    const json = await response.json();
    console.log('result',json);
  } catch (e){
    console.log('error',e);
  }
}
playerNameButton.addEventListener('click', get_player_name);


playerNameButton.addEventListener('click', ()=>{
  document.getElementById('welcome').innerText = `Hi ${playerName.value}, let's start your journey!`;
})



//All the airports are listed after player choose the city
function airportOptions(jsonData){

  ICAO_p.innerText = 'List of airports:';
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
  const button_airport = document.createElement('button');
  button_airport.appendChild(document.createTextNode('Take off!'));
  button_airport.setAttribute('id', 'button-airport')
  div_ICAO.appendChild(button_airport);


////////////////post method to get ICAO of airport
}
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
            ICAO_p.innerText = `City can not found! Choose another city.`;
            div_ICAO.appendChild(ICAO_p);

        } finally {                                         // finally = this is executed anyway, whether the execution was successful or not
            console.log('asynchronous load complete');
        }
    }


//call-back function to fetch all airport in chosen city
search.addEventListener('click', fetch_airport);

