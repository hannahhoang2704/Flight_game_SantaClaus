'use strict';
const search = document.getElementById('start');
const keyword = document.getElementById('keyword');
const result = document.getElementById('result');
function fetch_data(jsonData){                                //add options of airport in the chosen city
  for (let i = 0; i <jsonData.length; i++){
    const option = document.createElement('option');
    option.setAttribute('value', `${jsonData[i]['ICAO']}`);
    option.appendChild(document.createTextNode(`${jsonData[i]['Airport name']}`));
    result.appendChild(option);

  }
}
function fetch_airport(evt){
  evt.preventDefault();
  asynchronousFunction();
}

async function asynchronousFunction() {                 // asynchronous function is defined by the async keyword
        result.innerHTML = "";
        //console.log('asynchronous download begins');
        try {                                               // error handling: try/catch/finally
            //console.log(keyword.value);
            const response = await fetch('http://127.0.0.1:3000/' + keyword.value);    // starting data download, fetch returns a promise which contains an object of type 'response'
            const jsonData = await response.json();          // retrieving the data retrieved from the response object using the json() function
            fetch_data(jsonData);
        } catch (error) {
            console.log(error.message);
        } finally {                                         // finally = this is executed anyway, whether the execution was successful or not
            console.log('asynchronous load complete');
        }
    }
search.addEventListener('click', fetch_airport);