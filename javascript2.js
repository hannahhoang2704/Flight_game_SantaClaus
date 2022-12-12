'use strict';
let i = 0;
let txt = 'Each year children from all over the world fly to Rovaniemi to meet Santa. \n' +
    '                Believers to hug him and non-believers to expose him by pulling his beard. \n' +
    '                In any case your mission is to go to Rovaniemi and along the way pick up some other likeminded people. \n' +
    '                Each time you stop to pick someone up, they will challenge you to play a game with them. If you win you get to collect some gifts if you lose your new passengers get your gifts. \n' +
    '                Some would call it robbery; we call it fair play. \n' +
    '                The winner of this game is whoever collects the most gifts!';
let speed = 40;

function typeWriter() {
  if (i < txt.length) {
    document.getElementById("text-effect").innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
  }
}


function interact(){
  const next_button = document.createElement('button');
  next_button.innerHTML = 'Adventure';
  next_button.setAttribute('class', 'game-btn');
  next_button.setAttribute('id', 'adventure-btn');
  document.getElementById('popup').appendChild(next_button);
  next_button.onclick = function() {
  document.getElementById('popup').innerHTML = '';
  const question = document.createElement('p');
  question.innerHTML = `Do you believe in Santa Claus?`;
  document.getElementById('yes').appendChild(question);
  const yes_button = document.createElement('button');
  yes_button.innerHTML = 'Yes';
  yes_button.setAttribute('class', 'game-btn');
  document.getElementById('yes').appendChild(yes_button);
  yes_button.onclick = function() {
    alert(`Well what are you waiting for?!" 
            "Hop on the plane and come to Santa`);
    location = 'game_index.html';
  };
  const no_button = document.createElement('button');
  no_button.innerHTML = 'No';
  no_button.setAttribute('class', 'game-btn');
  document.getElementById('yes').appendChild(no_button);
  no_button.onclick = function() {
    alert(`I will prove wrong!
      Hop on the plane and get ready to be converted`);
    location = 'game_index.html';
  };
};
};
typeWriter();
interact();