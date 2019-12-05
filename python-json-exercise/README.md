# Goals of the Coding Exercise

* Ingest a json file that contains the following elements:
    * Playlists
    * Songs
    * Users
    
 As you can imagine, this is not a fully-fleshed out data model, but I hope 
 will provide you with enough code to give you a sense of my ability to tackle 
 this challenge.
 
 For instance, I lumped the songs together in a denormalized way where in I hard-coded
 the album and artist names rather than linking to more objects in a more 'normalized'
 way. Please excuse the shortcuts as I made the most of my time.
 

 # How to run it
 
 I wrote this exercise using Python 3.7. Most modern Mac and Linux distros should have this
 installed by default.
 
 Assuming this is the case, once you pull down this projct, all you will need to do from your shell is:
 
 ```$ python3 ./supermixer.py mixtape.json changes.json output.json```
 
 NB: I included a very basic test suite to validate inputs and you can run these from the project folder like so:
 
 ```$ pytest```
 
 # Discussion on Scaling
 
 My sample is rather simplistic and assumes (relatively) small data sets for the mixtape 
 and changes json files. Given that my code is loading these into memory and then performing
 actions against them, we could run into memory pressures as the size of the input files increase.
 
 With this in mind, my thought would be to consider the following alternatives:
 
 * Using a stream based approach, reduce the size of the input files. For example, we could read
 through the changes file, and extract the different kinds of update operations into their own
 smaller files and run the update operations in smaller sequential batches.
 
 * Consider using a database (either file or traditional) to load all of the data. Then, work in
 smaller chunks of operations in a similar sequential manner.
 
 
 # Closing thoughts
 
 Hi! 
 
 Thanks for taking your time to read through my coding exercise. It was fun putting this together. I truly enjoy big
 data and integration challenges of this nature. And of course, providing the means to ingest data from many kinds of 
 sources and deliver them out in turn. 
 
 It sounds like Highspot has some truly unique challenges of this nature and more. I'd be excited to talk about this submission and look forward to speaking with you soon.
 
 Cheers!
 
 ~ Paul