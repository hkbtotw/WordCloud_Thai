from pythainlp import word_tokenize as thai_tokens
from nltk import word_tokenize as eng_tokens
from pythainlp.corpus import stopwords as thaisw
import nltk
from nltk.corpus import stopwords as engsw
from nltk.stem import WordNetLemmatizer
from deepcut import stop_words
import deepcut
import pandas as pd
from pythainlp.corpus.common import thai_words
from pythainlp import Tokenizer
from pythainlp.rank import rank

def Cutter_Ranker_BU(FCT_FULL, select):

    ConnectCol=FCT_FULL[['GBU']].values.tolist()+FCT_FULL[['GBU_S']].values.tolist()

    output=[]
    def reemovNestings(l): 
        for i in l: 
            if type(i) == list: 
                reemovNestings(i) 
            else: 
                output.append(i) 
    reemovNestings(ConnectCol) 


    BUList=list(set(output))
    #print(' BUList : ', BUList)

    BU_frequentW={}
    #BUList=['Beer Product']



    BU_frequentW={}
    #BUList=['Beer Product']
    for n in BUList:


        if select=='External':
            print( ' ==> External ')    
            df2_Transaction=FCT_FULL.loc[(FCT_FULL['GBU'] == n) &  (FCT_FULL['GBU_S'] != n)].copy()
            df2_Transaction_2=FCT_FULL.loc[(FCT_FULL['GBU'] != n) &  (FCT_FULL['GBU_S'] == n)].copy()
            df_BU = df2_Transaction[['Id','OtherReason']].copy()
            df_BU_2 = df2_Transaction_2[['Id','OtherReason']].copy()
            dfList=df_BU['OtherReason'].values.tolist()+df_BU_2['OtherReason'].values.tolist()
            #print(' dfList : ',dfList, ' ;; Len =',len(dfList))                            
        else:
            print( ' ==> Internal ')
            df2_Transaction=FCT_FULL.loc[(FCT_FULL['GBU'] == n) &  (FCT_FULL['GBU_S'] == n)].copy()
            df_BU = df2_Transaction[['Id','OtherReason']].copy()
            dfList=df_BU['OtherReason'].values.tolist()

    
        Outcome=[]
        for r in dfList:
            Dummy=[]
            tokens=[]
            tokens=list(eng_tokens(r))
            lowered = [t.lower() for t in tokens]
            #print(' Dummy : ',lowered)
            lowered=" ".join(lowered)
            
            ### Simple pythainlp tokenization
            #Dummy=list(thai_tokens(lowered, engine='newmm'))
            
            ### Custom Deepcut Tokenize
            Dummy=deepcut.tokenize(lowered,custom_dict=[u'ไทยเบฟ',u'ผสานพลัง',u'ถังไม้โอ๊ค',u'โรงงาน',u'วังน้อย',u'โอกาส',u'สิบทิศ',u'สนับสนุน'])
            
            #print(' Dummy 2 : ',Dummy)
            Outcome.append(Dummy)

        
        ThaiWord=list(thaisw.words('thai'))
        #print(' tw : ',ThaiWord)
        EngWord=list(set(engsw.words('english')))
        #print(' ew : ',EngWord, ' : ', type(EngWord))    
        Morewords=[u'การ',u'การทำงาน',u'ทำงาน',u'เสมอ',u'krub',u'Test', u'nan', u' ',u'test',u'.',u'ท่าน',
                    u',',u'ดัน',u'ทำ',u'มือ',u'ลัก',u'พ',u'งาน',u'ดี',u'กา',u'/',u'\u200b',u')',u'(',u'จ้อ']                                    
        All_Stop_Word=ThaiWord+EngWord+Morewords

        NoStop=[]
        for k in Outcome:
            Dummy=[]
            Dummy=[word for word in k if word not in All_Stop_Word]
            NoStop.append(Dummy)


        output=[]
        def reemovNestings(l): 
            for i in l: 
                if type(i) == list: 
                    reemovNestings(i) 
                else: 
                    output.append(i) 
        reemovNestings(NoStop) 

        
        #print(' output : ',output, ' : ', len(output))
        RankedWord=rank(output)
        #print(' Rank : ',RankedWord,' == ',type(RankedWord))
        c=dict(RankedWord)
        #key=list(c.keys())
        #value=list(c.values())
        #print(' key : ',c, ' == ',type(c))
        SortedWord = sorted(c, key=lambda x: c[x], reverse=True)
        Dummy1=" - ".join(SortedWord[1:10])
        
        #print(' n : ',n, " -- ", Dummy1)
        BU_frequentW[n]=Dummy1

    return BU_frequentW

def Cutter_Ranker_LV(FCT_FULL, select):
    
    ConnectCol=FCT_FULL[['Level_R']].values.tolist()+FCT_FULL[['Level_S']].values.tolist()

    output=[]
    def reemovNestings(l): 
        for i in l: 
            if type(i) == list: 
                reemovNestings(i) 
            else: 
                output.append(i) 
    reemovNestings(ConnectCol) 

    #print(' CC : ',list(set(output)))

    #df1=FCT_TRNS

    #================================================= df1= FCT_TRNS==================================


    BUList=list(set(output))
    #print(' BUList : ', BUList)

    BU_frequentW={}
    #BUList=['10-10']
    for n in BUList:

        if select=='External':
            print( ' ==> External ')  
            df2_Transaction=FCT_FULL.loc[(FCT_FULL['Level_R'] == n) &  (FCT_FULL['Level_S'] != n)].copy()
            df2_Transaction_2=FCT_FULL.loc[(FCT_FULL['Level_R'] != n) &  (FCT_FULL['Level_S'] == n)].copy()
            df_BU = df2_Transaction[['Id','OtherReason']].copy()
            df_BU_2 = df2_Transaction_2[['Id','OtherReason']].copy()
            dfList=df_BU['OtherReason'].values.tolist()+df_BU_2['OtherReason'].values.tolist()
            #print(' dfList : ',dfList, ' ;; Len =',len(dfList))     
        else:
            print( ' ==> Internal ')  
            df2_Transaction=FCT_FULL.loc[(FCT_FULL['Level_R'] == n) &  (FCT_FULL['Level_S'] == n)].copy()
            df_BU = df2_Transaction[['Id','OtherReason']].copy()
            dfList=df_BU['OtherReason'].values.tolist()
    
        Outcome=[]
        for r in dfList:
            Dummy=[]
            tokens=[]
            tokens=list(eng_tokens(r))
            lowered = [t.lower() for t in tokens]
            #print(' Dummy : ',lowered)
            lowered=" ".join(lowered)
            
            #print(' Dummy : ', Dummy)
            
            ### custom tokenization
            #words = set(thai_words())  # thai_words() returns frozenset
            #words.add("ไทยเบฟ")
            #words.add("พาเลท")
            #words.add("ผสานพลัง")
            #words.add("ทีมงาน")
            #custom_tokenizer = Tokenizer(words)
            #Dummy=list(custom_tokenizer.word_tokenize(lowered))

            ### Simple pythainlp tokenization
            #Dummy=list(thai_tokens(lowered, engine='newmm'))
            
            ### Custom Deepcut Tokenize
            Dummy=deepcut.tokenize(lowered,custom_dict=[u'ไทยเบฟ',u'ผสานพลัง',u'ถังไม้โอ๊ค',u'โรงงาน',u'วังน้อย',u'โอกาส',u'สิบทิศ',u'สนับสนุน'])

            #print(' Dummy 2 : ',Dummy)
            Outcome.append(Dummy)

        
        ThaiWord=list(thaisw.words('thai'))
        #print(' tw : ',ThaiWord)
        EngWord=list(set(engsw.words('english')))
        #print(' ew : ',EngWord, ' : ', type(EngWord))
        Morewords=[u'การ',u'การทำงาน',u'ทำงาน',u'เสมอ',u'krub',u'Test', u'nan', u' ',u'test',u'.',u'ท่าน',
                    u',',u'ดัน',u'ทำ',u'มือ',u'ลัก',u'พ',u'งาน',u'ดี',u'กา',u'/',u'\u200b',u')',u'(',u'จ้อ']    
        All_Stop_Word=ThaiWord+EngWord+Morewords

        NoStop=[]
        for k in Outcome:
            Dummy=[]
            Dummy=[word for word in k if word not in All_Stop_Word]
            NoStop.append(Dummy)


        output=[]
        reemovNestings(NoStop) 

        
        #print(' output : ',output, ' : ', len(output))
        RankedWord=rank(output)
        #print(' Rank : ',RankedWord,' == ',type(RankedWord))
        c=dict(RankedWord)
        #key=list(c.keys())
        #value=list(c.values())
        #print(' key : ',c, ' == ',type(c))
        SortedWord = sorted(c, key=lambda x: c[x], reverse=True)
        Dummy1=" - ".join(SortedWord[1:10])
        
        #print(' n : ',n, " -- ", Dummy1)
        BU_frequentW[n]=Dummy1



    return BU_frequentW
