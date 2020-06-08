# LexicalAnalysis
The project's goal is to provide a Django application that enables measuring some lexical metrics of a text (like the content of a book)
or a set of texts. As a user you can either upload a text (in the plain text or pdf format) which will be stored in a 
library folder or remove any item(s) from the library. Application endpoint for a given item in addition to showing figures
for 'Total number of words', 'Number of different words' and 'Number of sentences' also displays 
a random sentence and successively (in decreasing order by clicking the next button) sentences from the content starting from the longest one. In the navigation bar of the 'book' view there is a 'Show plot' link that redirects user to a 
view containing an image with a bar chart presenting the numbers of sentences for certain sentence-length-ranges. 

Furthermore, there is an option for a user to compare a selected set of items from the library and see a view containing image
with a stacked bar chart compering vocabulary sizes of the items from the set (including the size of the common
vocabulary and sizes of lexicons specific for each particular item in the group).

