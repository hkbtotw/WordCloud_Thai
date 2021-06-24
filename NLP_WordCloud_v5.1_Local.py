import pandas as pd
from pythainlp import word_tokenize as thai_tokens
from nltk import word_tokenize as eng_tokens
from pythainlp.corpus import thai_stopwords as thaisw
from pythainlp.util import rank
import nltk
from nltk.corpus import stopwords as engsw
import datetime
from collections import Counter
import operator
from pythainlp.corpus.common import thai_words
from pythainlp import Tokenizer
import deepcut
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def reemovNestings(l): 
    for i in l: 
        if type(i) == list: 
            reemovNestings(i) 
        else: 
            output.append(i) 

###############################################################################
file_path=r'C:\\Users\\70018928\Documents\\Project2021\\Experiment\\NLP\\wordcutter\\'
file_name='TBPoint_Transaction_TC.xlsx'
spreadsheet_sheet='Transaction_NLP_no1'
###############################################################################

##### read input
df1=pd.read_excel(file_path+file_name,  sheet_name=spreadsheet_sheet, engine='openpyxl')


#### Select only identifier and textinput columns   
df2_Transaction = df1[['Id','OtherReason']].copy()

### Select only Textinput column to create List of strings 
dfList=df2_Transaction['OtherReason'].values.tolist()
#print(' dfList : ',dfList, ' ;; Len =',len(dfList))

####### CUTTING
#######  Looping through rows of textinput columns to cut words and remove stopwords
Outcome=[]
for r in dfList:
    Dummy=[]
    tokens=[]
    tokens=list(eng_tokens(r))
    lowered = [t.lower() for t in tokens]
    #print(' Dummy : ',lowered)
    lowered=" ".join(lowered)
        
    #print(' Dummy : ', Dummy)
    #Dummy=list(thai_tokens(lowered, keep_whitespace=False, engine='newmm'))

    ## Option1:  Custom cut
    # words = set(thai_words())  # thai_words() returns frozenset
    # words.add("พาเลท")
    # words.add("ผสานพลัง")
    # words.add("ทีมงาน")
    # custom_tokenizer = Tokenizer(words)
    # Dummy=list(custom_tokenizer.word_tokenize(lowered))

    ###  Option2: Custom Deepcut Tokenize
    Dummy=deepcut.tokenize(lowered,custom_dict=[u'ผสานพลัง',u'ถังไม้โอ๊ค',u'โรงงาน',u'วังน้อย',u'โอกาส',u'สิบทิศ',u'สนับสนุน'])


    #print(' Dummy 2 : ',Dummy)
    Outcome.append(Dummy)


###### REMOVING STOPWORDS
### Default Thai stopwords
ThaiWord=list(thaisw())
#print(' tw : ',ThaiWord)

#### Default English stopwords
EngWord=list(set(engsw.words('english')))
#print(' ew : ',EngWord, ' : ', type(EngWord))

#### Manually input customized stopwords
Morewords=['การ','การทำงาน','ทำงาน','เสมอ','krub','Test', 'nan', ' ','test','.',',','ดัน','ทำ','มือ','ลัก','พ','งาน','ดี','กา','/','\u200b',')','(']
All_Stop_Word=ThaiWord+EngWord+Morewords

#### Remove all stopwords
NoStop=[]
for k in Outcome:
    Dummy=[]
    Dummy=[word for word in k if word not in All_Stop_Word]
    NoStop.append(Dummy)


output=[]
reemovNestings(NoStop) 


print(' Output no stopwords : ',output, ' : ', len(output))
dfOutput=pd.DataFrame(output, columns=['output'])
dfOutput.to_csv(file_path+'output_for_wordcloud.csv')



############# Wordcloud image generation 
## ref: https://python3.wannaphong.com/2017/06/word-cloud-python.html
## ref: https://www.f0nt.com/release/th-sarabun-new/  (Thai font)
text=" ".join(output)
# Create and generate a word cloud image:
wordcloud = WordCloud(font_path='C:\\Users\\70018928\\Documents\\Project2021\\Experiment\\NLP\\wordcutter\\thai_font\\THSarabunNew.ttf',
                width = 800, height = 800,
                background_color ='white',
                regexp=r"[\u0E00-\u0E7Fa-zA-Z']+",
                min_font_size = 10).generate(text)
# Display the generated image:
  
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)
plt.show()



#############################################################
### Ranking most frequently appearing words
RankedWord=rank(output)
#print(' Rank : ',RankedWord,' == ',type(RankedWord))
c=dict(RankedWord)
#key=list(c.keys())
#value=list(c.values())
#print(' key : ',c, ' == ',type(c))
SortedWord = sorted(c, key=lambda x: c[x], reverse=True)
Dummy1=" - ".join(SortedWord[1:15])

print( " Top 15 words most frequently appearing words in the textinput -- ", Dummy1)



