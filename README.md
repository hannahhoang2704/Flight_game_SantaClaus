# <h1>Flight_simulator_game</h1>

Christmas themed game which allows player to fly through 5 layoff destinations from the departure airport that player choose, to collect gift before arrive Rovaniemi.

The project is using Python Flask as a server, to connect different APIs and SQL database.



<h2>1. Introduction</h2>

The purpose of this document is to give an overview of the Ho Ho Ho game project and
describe the implementation of the program. Target group of the game is players at the
age of 12 onwards.
The report consists of current state and vision of the game, functional requirements as
well as quality requirements.
<h2>2. Current State</h2>
The framework of the main game has been completed and available on the webpage.
There are still some bugs needed to be fixed and some further development ideas can
be implemented to improve the quality of the game.
Apart from entertainment, the major purpose of the game project is to raise players’
environmental awareness of CO2 emission in airplanes by displaying distance between
different locations and providing the estimated calculation of how much CO2 is needed
for the airplane to fly such distance. Moreover, the quiz questions are involved in
environmental topics which help to emphasize on the importance of environmental
sustainability and preservation.


<h2>3. Vision</h2>

The aim of the single-player Ho Ho Ho game project is to produce an entertaining and
educational experience where players get to use airplanes to fly to Rovaniemi and learn
about environmental sustainability. It is an interactive game, allowing the players to use
mouse and keyboard to engage throughout the game. Based on players‘ inputs and
choice the program will generate different outputs.
The program begins with a countdown until Christmas Eve and an introduction story.
The purpose of the story is to raise the interest and engagement of players in the game.
The story tells that every year there are people that fly to Rovaniemi to meet Santa
Claus. To get there, the players have five layover stops and, in each stop, they will have
some passengers to pick up. These passengers will challenge them to play some
games – quiz and rock paper scissors game. If players win then they will receive points
in the form of gifts, otherwise some of their gifts will be robbed.
In the beginning of the game the players can express if they believe in Santa or not.
Afterwards they choose their starting point/departure airport to fly from. They are then
informed of the distance from their starting point to Rovaniemi. The amount of the gifts
that the players have in the beginning of the game as well as the amount of CO2
consumption will also be displayed.
The game also displays weather conditions in every layover airport (wind, temperature,
description) as players visit it.
In every destination, the players need to answer one question related to the
environment and sustainability. If they answer correctly, they will receive gifts. They will
then continue the journey with a rock-paper-scissors game challenge. The gifts will be
updated based on the game result.


<h2>4. Functional requirements</h2>

Figure 1 represents the game's diagram. The game starts by telling a player a storyline
and instruction on how to play the game. Game’s mission and goal is also clarified
explicitly before the player starts the game. To raise users’ experience and interactive
engagement, the player is asked to answer a few questions before his flight.
The players start the game by entering his name and choosing a city where they would
like to depart from within a scope of European regions. The server will fetch from the
database all available airports in the city from which the players can select one as a
departure airport . As soon as players click on take-off button, those data including
players’ name, departure airport will be inserted to the database. Meanwhile on the
webpage, several elements are updated: the departure airport will be marked on the
map by using map API in the server. In the game status section, players’ name is
shown. The distance between departure airport and Rovaniemi airport is displayed.
Default gifts value is also presented in the game status section and CO2 consumption
fetched from CO2 API is also shown in the game status.

Besides, the weather of current location including temperature, wind speeds and
description is updated, by fetching weather API running in the server.
In every layoff destination, players will complete two games which are quizzes and a
rock-paper-scissors game to collect gifts. In order to win the game, players need to pass
through 5 destinations and keep their gifts above 0, otherwise the game is over.
While loop and if condition is created to ensure users play the game under those
conditions. Every time players move to a new transit airport, it is also marked on the
map. Additionally, the current airport name is updated as well as current location’s
weather. A random question is called from a list of questions and one round of
rock-paper-scissors is played. After the question is called, it is removed from the list to
avoid duplicated questions in the following destination. Depending on the answer (either
correctly or not), the player can collect gifts or lose them. Same rule of win and lose is
applied in the rock-paper-scissors game.
After the game ends, players’ names, their scores (number of gifts) and the amount of
estimated CO2 consumption is stored in the database.


<h2>5. Quality requirements</h2>

One of the quality requirements applied in the program to improve users’ experience is
Christmas Eve countdown watch. Considering that the whole game revolves around
Rovaniemi and players’ journey to visit Santa Claus to get the player initially excited,
the countdown will increase players’ engagement in the theme of the game.
In addition, a quality requirement implemented in the game to improve the game
experience includes Christmas - themed color palette and pictures, snowflakes effects,
and Santa Claus related questions to increase interaction between the game and
players. Those features engage users to the festive/Christmas spirit.
The second effect in terms of quality requirements is the game status display. A
separate color text is used to emphasize on important information which indicates
current game status, amount of gifts, amount of CO2 needed for the trip and the
distance from departure airport to Rovaniemi.
Moreover, to help players visualize their current location better a map API is displayed
on the webpage. Adding the weather information of the airport that the users are
currently on can make them feel more realistic about the trip. The red line that connects
the starting point and ending point and the pop up window with the position of the
airports help users more with visualization.
By utilizing the type effect text, not only will the player have some spare moments to
comprehend the instructions or messages, but the game will also pause for a few
seconds before proceeding, giving users a chance to build anticipation.
Furthermore, by clearing the screen of the parts of the game that are no longer needed,
the game provides clearer layout in an organized manner, allowing users to focus on
only necessary information. During the game, players get instant feedback every time
they submit their choice and total gifts are updated after that, allowing them to follow the
game flow. Also the alert pops up when players finish the game or lose all the gifts
which are gameover, making the players understand all the events happening during
the game.
Last but not least, photos of the different elements that belong to the such as rock paper
scissors to make the game more versatile.
