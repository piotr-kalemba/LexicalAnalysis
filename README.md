# LexicalAnalysis
The project's goal is to provide a Django application that enables measuring some lexical metrics of a book
or a set of books. As a user you can either upload a book (in the plain text or pdf format) which will be stored in a 
library folder or remove any book from the library. Application endpoint for a given book in addition to showing figures
for 'Total number of words', 'Number of different words' and 'Number of sentences' also displays three longest sentences
and one random sentence from the content. In the navigation bar there is a 'Show plot' link that redirects user to a 
view containing an image with a bar chart presenting the numbers of sentences for certain sentence-length-ranges. 

Furthermore, there is an option for a user to compare a selected set of books from the library and see a view containing image
with a stacked bar chart compering vocabulary sizes of the books from the set (including the size of the common
vocabulary and sizes of lexicons specific for each particular book in the group).

