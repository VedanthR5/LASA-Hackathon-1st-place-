#https://pythonhosted.org/PyPDF2/
#from requests import get
#import PyPDF2
#import textract
from tika import parser
import math


###TEACHER INPUT###
informed = input("Informed grading? y/n:\n")

structWeight = 5
mincount = 0
mindeduction = 5
def intConversion(var, str):
  temp = input(str)
  return var if temp == "" else int(temp)
if informed == "y":
  topic = input("Topic of paper:\n") #todo incorporate web search of this into grading (is the paper on topic?)
  structWeight = intConversion(structWeight, "Weight of structure on grade 1-10 (default " + str(structWeight) + "):\n")
  mincount = intConversion(mincount, "Minimum word count (default " + str(mincount) + "):\n")
  mindeduction = intConversion(mindeduction, "Point deduction if minimum not reached (default " + str(mindeduction) + "):\n")


###IMPORT AND FORMAT PDF / GATHER INFO###
filename = "pdf.pdf"
raw = parser.from_file(filename)
raw = str(raw)

#separate pdf data from text cleanly
raw = raw.split("\'content\': \"")[1]
raw = raw.split("\", \'status\':")[0]

wordcounter = 0
hardwords = 0
words = []
wordsnopunc = []
neatwords = ""
neatwordsnopunc = ""

#separate words from \n and count
for x in raw.split(" "): # x is a 'word' in the pdf file

  if "\\n" in x:
    while True:
      if x.find("\\n") != -1: # word contains line break
        words.append(x[0 : x.find("\\n")]) # add content before \n
        x = x[x.find("\\n") + 2:] # keep content after \n
        if "\\n" not in x: # repeated \n doesn't count as words
          wordcounter += 1
        continue
      else:
        break

  words.append(x)
  wordcounter += 1

  hardwords += math.floor(len(x) / 7)

for word in words:
  neatwords += word + " "

#count characters
charcounter = len(neatwords)
charcounternopunc = 0
punccounter = 0
for x in neatwords:
  if(ord(x) >= 65 and ord(x) <= 90 or ord(x) >= 97 and ord(x) <= 122):
    charcounternopunc += 1
  elif ord(x) != 32:
    punccounter += 1

#separate and count sentences
sentences = neatwords.split(".")

for x in sentences:
  if "!" in x:
    sentences.append(x[x.find("!")])
    x = x[0 : x.find("!")]
  if "?" in x:
    sentences.append(x[x.find("?")])
    x = x[0 : x.find("?")]
sentencecounter = len(sentences)


###CALCULATE###

#sentence structure/complexity (reading level)
level = 0.4 * ((wordcounter / sentencecounter) + (hardwords / wordcounter * 100))
level += (punccounter - sentencecounter) / 5 #internal punctuation is advanced

#grade or score
structGrade = (level / 30 * 100)
topicGrade = 50

grade = structGrade * (structWeight / 10)
grade += topicGrade * (1 - structWeight / 10)
if wordcounter < mincount:
  grade -= mindeduction

grade = min(grade, 100)


###OUTPUT###
print("\n\n\n")
print(neatwords)

print('\n- - - - - - - HelpaTeacher Analysis - - - - - - -')

print('\nWord Count: ' + str(wordcounter))
print('Character Count: ' + str(charcounter))
print('Sentence Count: ' + str(sentencecounter))
print('\nAverage word length: ' + str("{:.2f}".format(charcounternopunc / len(words))) + ' characters')
print('Average sentence length: ' + str("{:.2f}".format(wordcounter / sentencecounter)) + ' words')
print('\nReading level: ' + str("{:.2f}".format(level)))
print('Score: ' + str("{:.2f}".format(grade)))

print('\n- - - - - - - - - - - - - - - - - - - - - - - - -')

print("\n\n\n")


'''
Tyler: (512) 521-2289
Asa: (512) 550-2201
Vedanth: (512) 839-4119
https://docs.google.com/presentation/d/1aM5usKoYzyz-Rx2PArZ-ikMEKdqm73pgs5gCC384qow/edit?usp=sharing
'''