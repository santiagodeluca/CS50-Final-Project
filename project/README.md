# CS50-Final-Project
# LearnWords
### Video demo: https://youtu.be/IPx7x0Z4SNQ?si=wKsMLtJTr6g9yNMH
# Description
## The idea
### This project was initially motivated by a need I had while learning english (I am from Argentina, a spanish-speaking country), specifically when learning words from large texts/books. Whenever I read books and loved the words used in them I just couldn't learn all the new vocabulary because finding the complex words among the more common ones was complicated. So in order to solve that problem, I wanted to design a webpage that allowed the user to input any text and get as a response a categorization of words depending on their complexity level, and their definition.
## The implementation
### The first problem to arise was how to categorize words in easy/hard. In order to do so, I decided that the frequency of usage was a great way to determine whether a words is more or less complex. This critiria may not be true with all words, but it is with most. So that was how I searched for a list that would order english words depending on frequency, and I [found it](https://github.com/hermitdave/FrequencyWords/blob/master/content/2018/en/en_50k.txt). The github user [Hermit Dave](https://github.com/hermitdave) created [the project](https://github.com/hermitdave/FrequencyWords) from where the database was extracted.
### I had to modify this huge list of the first 50,000 most frequently used english words using SQL, mainly to delete words which I considered way too basic for this project (words like, 'are', 'you', 'in'). I did so in order to improve the user expirience (it would be annoying if the program tried to teach the word 'the' each time you use it). Also, I added a column called 'id' that would autoincrement in order to use that number in app.py to determine which words are more complex than others. 
### Other changes include managing the actual way in which the original list was created. This list had next to each word a number that indicated the times the word was found/used. Using SQL I deleted those numbers, so that when app.py searches for a particular word on the table it can find without getting confused by the numbers next to it.
### Once the database was set, I designed the three main pages of the site (index.html, learn.html and play.html) all organized by app.py. I also created an 'About' page to give the user some information about the project and the references to the database used. 

## index.html
### Here the user will receive a brief introduction to the page and its purpose, and have big textarea box in which to write (or probably copy-paste!) their text. In order make the textarea responsive to the 'enter' key I had to write some javaScript. Here the top-left navbar is seen for the first time, it only has the 'home' item but this will change depending on what page the user is currently on.

## learn.html
### In this second page, the user will be able to choose a difficulty level. I took into account all the possible outcomes of the text being inputed: Wheter there are words in every level, wheter there are in some or whether there are no words in any list. In order to do so I used javaScript again. Jinja was heavily relied upon (to give an accurate example of a word in a list, the number of words per level and whether there are any words on the list via an if statement). For each level, I created a different card (using Bootstrap). Cards where really useful and where also used in play.html.

## play.html
### In this last page the user will be able to actually LearnWords! If the user knows the word, they can click 'I know it' and skip to the next one, where the next word will be displayed and the word count will be updated (more javaScript). If the user does not know the word they have the option to click on two links, one to the Cambridge Dictionary page of the unknown word and one of the Merriam-Webster Dictionary of that word too. In order to implement this page Jinja was heavily relied upon too (not only to extend layout.html, but also to set the correct total of words depending on the length of the list!).

## app.py
### Here the categorization actually takes place (depending on how further down the list the word is, it is considered more complex). I chose some particular numbers to divide the 50,000 words into four categories. Those three numbers are 9,000, 25,000, and 40,000. I determined this was a good way to divide the words by exploring the list, and trying to stand in the english-learner shoes. After testing the program with multiple texts (some of the used texts where articles about history like articles about the World War II and the Roman Empire and scientific articles for example about photosynthesis). I came to the conclusion that this was a correct way to divide the words (since the number of words in each level made sense, for example, when testing it with an article about the Roman empire, the numbers in the lists where 266, 76, 33 and 9 from easiest to hardest). 
### Also, here all the lists are passed in, once created, first to learn.html to display their length and give an example from each list, and then into each of the four levels. Notice how only one template (play.html) is used in all four of the levels. play.html was designed to achieve this, so that the level that is displayed depends directly upon what app.py passes in as a list and as a level name. In this way, a lot of time and space was saved. 
### All lists are kept in the session object, and restarted each time the user comes back to the homepage (so that new words inputed do not get mixed with old words that have already been learned).

## layout.html
### Here the base of all of the htmls is coded. Bootstrap is included, the background image is set in the body (only static element apart from styles.css) and the navbar is created.

## styles.css
### The main focus while designing the look of this site was starting with the background image (home-backgroun.jpg) and then selecting colors (of fonts and cards) based on what would contrast with that picture. Readability was at the core of the design and was always taken into consideration.
