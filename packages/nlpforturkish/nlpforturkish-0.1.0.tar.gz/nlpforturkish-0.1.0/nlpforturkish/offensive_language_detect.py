# Define the `offensive_language_detect` class
class offensive_language_detect:
    def read_file(self,file):
        with open(file, 'r', encoding="utf-8") as f:
            return f.readlines()

    def write_file(self,file, mode, data, new_line=False):
        with open(file, mode, encoding="utf-8") as f:
            for l in data:
                if l != None:
                    f.write(l)
                    if(new_line):
                        f.write("\n")
    def remove_punctuations(self,readFile):
        import re
        s = ""
        with open(readFile, "r", encoding="utf-8") as file:
            s = re.sub(r'[^\w\s]','',file.read())
            return s.lower()
    def splitText(self,raw_data_path, split_char):
        mylist = []
        with open(raw_data_path, encoding="utf-8") as file:
            mylist = [j.strip() for i in file.readlines() for j in i.split(split_char)]
        return mylist
    
    def stemmer(self,raw_data_splitted):
        from TurkishStemmer import TurkishStemmer
        from nltk.tokenize import RegexpTokenizer
        from nltk.probability import FreqDist
        stemmer = TurkishStemmer()
        stemmed_data = [stemmer.stem(i.strip()) for i in raw_data_splitted]

        lowercase_tokens = []
        for line in raw_data_splitted:
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(line)
            lowercase_tokens.extend([token.lower() for token in tokens])

        frq_dist = FreqDist(lowercase_tokens)
        words_by_frequency = sorted(frq_dist, key=frq_dist.get, reverse=True)
        return list(set(words_by_frequency + stemmed_data))

        
    
    def create_suffix(self,data):
        my_list=[]
        from turkish_suffix_library.turkish import Turkish
        # raw = self.read_file(path)
        for i in data:
            my_list.append(str(Turkish(i.strip().lower())))
            my_list.append(str(Turkish(i.strip().lower()).ablative()))
            my_list.append(str(Turkish(i.strip().lower()).ablative(person=1)))
            my_list.append(str(Turkish(i.strip().lower()).ablative(person=2)))
            my_list.append(str(Turkish(i.strip().lower()).ablative(person=3)))
            my_list.append(str(Turkish(i.strip().lower()).plural().ablative()))
            my_list.append(str(Turkish(i.strip().lower()).plural().ablative(person=1)))
            my_list.append(str(Turkish(i.strip().lower()).plural().ablative(person=2)))
            my_list.append(str(Turkish(i.strip().lower()).plural().ablative(person=3)))
            my_list.append(str(Turkish(i.strip().lower()).plural().possessive().ablative()))
            my_list.append(str(Turkish(i.strip().lower()).plural().possessive(person=1).ablative()))
            my_list.append(str(Turkish(i.strip().lower()).plural().possessive(person=2).ablative()))
            my_list.append(str(Turkish(i.strip().lower()).plural().possessive(person=3).ablative()))
            my_list.append(str(Turkish(i.strip().lower()).possessive().ablative()))
            my_list.append(str(Turkish(i.strip().lower()).possessive(person=1).ablative()))
            my_list.append(str(Turkish(i.strip().lower()).possessive(person=2).ablative()))
            my_list.append(str(Turkish(i.strip().lower()).possessive(person=3).ablative()))
            my_list.append(str(Turkish(i.strip().lower()).accusative()))
            my_list.append(str(Turkish(i.strip().lower()).accusative(person=1)))
            my_list.append(str(Turkish(i.strip().lower()).accusative(person=2)))
            my_list.append(str(Turkish(i.strip().lower()).accusative(person=3)))
            my_list.append(str(Turkish(i.strip().lower()).plural().accusative()))
            my_list.append(str(Turkish(i.strip().lower()).plural().accusative(person=1)))
            my_list.append(str(Turkish(i.strip().lower()).plural().accusative(person=2)))
            my_list.append(str(Turkish(i.strip().lower()).plural().accusative(person=3)))
            my_list.append(str(Turkish(i.strip().lower()).plural().possessive().accusative()))
            my_list.append(str(Turkish(i.strip().lower()).plural().possessive(person=1).accusative()))
            my_list.append(str(Turkish(i.strip().lower()).plural().possessive(person=2).accusative()))
            my_list.append(str(Turkish(i.strip().lower()).plural().possessive(person=3).accusative()))
            my_list.append(str(Turkish(i.strip().lower()).possessive().accusative()))
            my_list.append(str(Turkish(i.strip().lower()).possessive(person=1).accusative()))
            my_list.append(str(Turkish(i.strip().lower()).possessive(person=2).accusative()))
            my_list.append(str(Turkish(i.strip().lower()).possessive(person=3).accusative()))
            my_list.append(str(Turkish(i.strip().lower()).dative()))
            my_list.append(str(Turkish(i.strip().lower()).dative(person=1)))
            my_list.append(str(Turkish(i.strip().lower()).dative(person=2)))
            my_list.append(str(Turkish(i.strip().lower()).dative(person=3)))
            my_list.append(str(Turkish(i.strip().lower()).plural().dative()))
            my_list.append(str(Turkish(i.strip().lower()).plural().dative(person=1)))
            my_list.append(str(Turkish(i.strip().lower()).plural().dative(person=2)))
            my_list.append(str(Turkish(i.strip().lower()).plural().dative(person=3)))
            my_list.append(str(Turkish(i.strip().lower()).plural().possessive().dative()))
            my_list.append(str(Turkish(i.strip().lower()).plural().possessive(person=1).dative()))
            my_list.append(str(Turkish(i.strip().lower()).plural().possessive(person=2).dative()))
            my_list.append(str(Turkish(i.strip().lower()).plural().possessive(person=3).dative()))
            my_list.append(str(Turkish(i.strip().lower()).possessive().dative()))
            my_list.append(str(Turkish(i.strip().lower()).possessive(person=1).dative()))
            my_list.append(str(Turkish(i.strip().lower()).possessive(person=2).dative()))
            my_list.append(str(Turkish(i.strip().lower()).possessive(person=3).dative()))
            my_list.append(str(Turkish(i.strip().lower()).possessive(person=1, plural=True)))
            my_list.append(str(Turkish(i.strip().lower()).possessive(person=2, plural=True)))
            my_list.append(str(Turkish(i.strip().lower()).possessive(person=3, plural=True)))
            my_list.append(str(Turkish(i.strip().lower()).ordinal()))
            my_list.append(str(Turkish(i.strip().lower()).distributive()))
            my_list.append(str(Turkish(i.strip().lower()).instrumental()))
        return my_list

    # Türkçe karakterlerin İngilizce karakterlere dönüştürüldüğü sözlük
    CHAR_MAP = {
        'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u'
    }

    def convert_to_english(self,word):
        """
        Türkçe karakterleri İngilizce karakterlere dönüştürür.
        """
        return ''.join([self.CHAR_MAP.get(char, char) for char in word])

    def remove_vowels(self,word):
        """
        Kelimenin içindeki sesli harfleri çıkartır.
        """
        vowels = 'aeiouıöü'
        return ''.join([char for char in word if char.lower() not in vowels])

    def sensor_vowels(self,word, sensor_char='*'):
        """
        Kelimenin içindeki sesli harfleri sensörler.
        """
        vowels = 'aeiouıöü'
        return ''.join([sensor_char if char.lower() in vowels else char for char in word])

    def generate_possible_words(self, input_word):
        """
        Tüm mümkün kelime kombinasyonlarını oluşturur.
        """
        possible_words = []
        
        if type(input_word) == list:
            for word in input_word:
                word = word.lower()
                converted_word = self.convert_to_english(word)
                no_vowels_word = self.remove_vowels(word)
                sensor_two_vowels_word = self.sensor_vowels(word, sensor_char='*')
                sensor_first_last_vowels_word = self.sensor_vowels(word[0] + word[1:-1] + word[-1], sensor_char='*')
                sensor_middle_vowel_word = self.sensor_vowels(word[:len(word)//2] + '*' + word[len(word)//2+1:], sensor_char='*')
                possible_words += [word, converted_word, no_vowels_word, sensor_two_vowels_word,
                                sensor_first_last_vowels_word, sensor_middle_vowel_word]
                
                for i, char in enumerate(word):
                    if char.lower() in 'aeiouıöü':
                        for sensor_char in ['*']:
                            possible_word = word[:i] + self.sensor_vowels(char, sensor_char) + word[i+1:]
                            possible_word_no_vowels = self.remove_vowels(possible_word)
                            possible_word_converted = self.convert_to_english(possible_word)
                            possible_words += [possible_word, possible_word_no_vowels, possible_word_converted]
            
        elif type(input_word) == str:
            word = input_word.lower()
            converted_word = self.convert_to_english(word)
            no_vowels_word = self.remove_vowels(word)
            sensor_two_vowels_word = self.sensor_vowels(word, sensor_char='*')
            sensor_first_last_vowels_word = self.sensor_vowels(word[0] + word[1:-1] + word[-1], sensor_char='*')
            sensor_middle_vowel_word = self.sensor_vowels(word[:len(word)//2] + '*' + word[len(word)//2+1:], sensor_char='*')
            
            possible_words += [word, converted_word, no_vowels_word, sensor_two_vowels_word,
                                sensor_first_last_vowels_word, sensor_middle_vowel_word]
            
            for i, char in enumerate(word):
                if char.lower() in 'aeiouıöü':
                    for sensor_char in ['*']:
                        possible_word = word[:i] + self.sensor_vowels(char, sensor_char) + word[i+1:]
                        possible_word_no_vowels = self.remove_vowels(possible_word)
                        possible_word_converted = self.convert_to_english(possible_word)
                        possible_words += [possible_word, possible_word_no_vowels, possible_word_converted]
            
        # Tüm olası kelime kombinasyonlarını alfabetik sıraya göre sıralıyoruz
        possible_words = sorted(set(possible_words))
        
        return possible_words


    def get_eksisozluk_entries(self,suffixes, output_file_path, server_path='http://localhost:3000/api/baslik/'):
        import requests
        import json
        my_data = []
        with open(output_file_path, 'w', encoding='utf-8') as f:
            if isinstance(suffixes, str):
                with open(suffixes, encoding='utf-8') as suffix_file:
                    suffix_list = [suffix.strip() for suffix in suffix_file]
            else:
                suffix_list = suffixes


            for suffix in suffix_list:
                response = requests.get(server_path+suffix.strip())
                x= json.loads(response.text)
                try:
                    counter = 1
                    while True:  
                        my_response = requests.get(server_path+str(x["slug"])+"?p="+str(counter))
                        y = json.loads(my_response.text)
                        for i in y["entries"]:
                            print(i["body"])
                            f.write(i["body"])
                            my_data.append(i["body"])
                            f.write("\n")
                        counter = counter + 1
                        if(x["total_page"] == x["current_page"]):  
                            break
                        print("---------------------------------------------------")
                        print("---------------------------------------------------")
                        print("---------------------------------------------------")
                        print("---------------------------------------------------")
                        print("---------------------------------------------------")
                        print("---------------------------------------------------")
                        print("---------------------------------------------------")
                        print(suffix,x["total_page"] , x["current_page"], counter)
                        print("---------------------------------------------------")
                        print("---------------------------------------------------")
                        print("---------------------------------------------------")
                        print("---------------------------------------------------")
                        print("---------------------------------------------------")
                        print("---------------------------------------------------")
                except Exception as e:
                    print(e)

        return my_data


    def index_based_encoding(self,raw_data, write_file, max_words=None):
        # Open and read the input file
        with open(raw_data, encoding='utf-8') as document_corpus:
            document_corpus = document_corpus.readlines()
            
            # Calculate the maximum number of words in a row and initialize an empty set
            if max_words is None:
                max_words = len(max(document_corpus, key=len).split(" "))
            
            data_corpus = set()
            # Iterate over each row in the document corpus
            for row in document_corpus:
                # Split the row into individual words and add each unique word to the set
                for word in row.split(" "):
                    if word not in data_corpus:
                        data_corpus.add(word)
            # Sort the set to maintain consistency in encoding
            data_corpus=sorted(data_corpus)
            
            index_based_encoding=[]
            # Iterate over each row in the document corpus again
            for row in document_corpus:
                row_encoding = []
                split = row.split(" ")
                # Encode each word in the row using the data corpus set
                for i in range(max_words):
                    if i <= len(split)-1:
                        row_encoding.append(data_corpus.index(split[i])+1)
                    else:
                        row_encoding.append(0)
                index_based_encoding.append(row_encoding)
                
            # Write the encoded rows to the output file
            with open(write_file, 'w') as f:
                for i in index_based_encoding:
                    f.write(str(i).replace("[","").replace("]",""))
                    f.write("\n")

    
    def split_offensiveNNeutral(self,data_path, suffixes_path,merged_text, merged_number):
        suffixes = set(line.strip() for line in open(suffixes_path, encoding='utf-8'))
        data_list = set(line.strip() for line in open(data_path, encoding='utf-8'))

        offensive_data = []
        neutral_data = []

        for data in data_list:
            filtered_list = list(filter(lambda suffix: f" {suffix} " in data, suffixes))
            if filtered_list:
                offensive_data.append(data)
            else:
                neutral_data.append(data)

        offensive_data_number = ["0" for i in range(len(offensive_data))]
        neutral_data_number = ["1" for i in range(len(neutral_data))]

        self.write_file(merged_text, 'w', offensive_data+neutral_data,True)
        print(merged_text, len(offensive_data+neutral_data))
        self.write_file(merged_number, 'w', offensive_data_number+neutral_data_number,True)
        print(merged_number, len(offensive_data_number+neutral_data_number))
        return offensive_data+neutral_data, offensive_data_number+neutral_data_number






    def clean_html(self, file_path):
        from bs4 import BeautifulSoup
        cleantext = []
        with open(file_path, mode='r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'lxml')

            for line in soup:
                a_strip = line.text.strip()
                cleantext.append(a_strip)
        with open(file_path, mode='w', encoding='utf-8') as f2:
            f2.write('\n'.join(cleantext))
        return cleantext

    def gaussianNB(self,data_path, labels_path, word2vec=False, vector_size=90, test_size=0.2, data_sep=','):
        import numpy as np
        from sklearn.model_selection import train_test_split
        from sklearn.naive_bayes import GaussianNB
        from sklearn.metrics import accuracy_score

        if word2vec:
            X_train, X_test, y_train, y_test = self.get_word2vec(data_path, labels_path, vector_size=vector_size)
        else:
            CSVData = open(data_path)
            Array2d_result = np.genfromtxt(CSVData, delimiter=data_sep)
            X=Array2d_result

            CSVDataLabels = open(labels_path)
            Array2d_result = np.genfromtxt(CSVDataLabels, delimiter=data_sep)
            y=Array2d_result

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)

        print("GaussianNB")
        gnb = GaussianNB()
        y_pred = gnb.fit(X_train, y_train).predict(X_test)
        print(X_train.shape, X_test.shape)
        print(y_pred)
        print("Number of mislabeled points out of a total %d points : %d"
            % (X_test.shape[0], (y_test != y_pred).sum()))
        print('Model accuracy score: {0:0.4f}'. format(accuracy_score(y_test, y_pred)))
        print("######################################################################")
        return y_pred, y_test
            
    # def logisticRegression(self,  test_size=0.2, data_sep=','):

    def logisticRegression(self,data_path, labels_path, word2vec=False, vector_size=90, test_size=0.2, data_sep=','):
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score
        from sklearn.linear_model import LogisticRegression
        import numpy as np

        if word2vec:
            X_train, X_test, y_train, y_test = self.get_word2vec(data_path, labels_path, vector_size=vector_size)
        else:
            X_train, X_test, y_train, y_test = self.get_encoded_data(data_path, labels_path, test_size=test_size, data_sep=data_sep)
        logreg = LogisticRegression()
        logreg.fit(X_train, y_train)
        y_pred = logreg.predict(X_test)
        print("Number of mislabeled points out of a total %d points : %d" % (X_test.shape[0], (y_test != y_pred).sum()))
        print('Model accuracy score: {0:0.4f}'. format(accuracy_score(y_test, y_pred)))
        print("######################################################################")
        return y_pred, y_test
    def calculate_confusion_matrix(self,y_test, y_pred):
        import matplotlib.pyplot as plt
        from sklearn import metrics
        confusion_matrix = metrics.confusion_matrix(y_pred,y_test)
        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels = [False, True])
        cm_display.plot()
        plt.show()
    def calculate_classification_report(self,y_test, y_pred):
        from sklearn.metrics import classification_report
        print(classification_report(y_test, y_pred))

    def get_word2vec(self,data_path, labels_path, vector_size=90, test_size=0.2):

        from gensim.models import Word2Vec
        from sklearn.model_selection import train_test_split
        import numpy as np

        # Load the raw sentences from file
        with open(data_path, "r", encoding='utf-8') as f:
            sentences = [line.strip() for line in f]

        # Load the raw labels from file
        with open(labels_path, "r", encoding='utf-8') as f:
            y = [int(line.strip()) for line in f]
                # Train a Word2Vec model on the sentences
        sentences_tokens = [sentence.split() for sentence in sentences]
        w2v_model = Word2Vec(sentences_tokens, vector_size=vector_size, min_count=1)

        # Compute the average vector representation of each sentence
        X = np.array([np.mean([w2v_model.wv[word] for word in sentence.split() if word in w2v_model.wv], axis=0) for sentence in sentences])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)
        return X_train, X_test, y_train, y_test
    
    def get_encoded_data(self, data_path, labels_path, test_size=0.2, data_sep=','):
        import numpy as np
        from sklearn.model_selection import train_test_split
        CSVData = open(data_path)
        Array2d_result = np.genfromtxt(CSVData, delimiter=data_sep)
        X=Array2d_result

        CSVDataLabels = open(labels_path)
        Array2d_result = np.genfromtxt(CSVDataLabels, delimiter=data_sep)
        y=Array2d_result

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)
        return X_train, X_test, y_train, y_test
    def make_it_with_lazy_predict(self,data_path, labels_path, result_write_path, word2vec=False, vector_size=90, test_size=0.2, data_sep=','):
        ### importing LazyClassifier for classification problem
        from lazypredict.Supervised import LazyClassifier
        ### importing LazyClassifier for classification problem because here we are solving Classification use case.
        from lazypredict.Supervised import LazyClassifier

        clf = LazyClassifier(verbose=0,ignore_warnings=True, custom_metric=None)
        if word2vec:
            X_train, X_test, y_train, y_test = self.get_word2vec(data_path, labels_path, vector_size=vector_size)
        else:
            X_train, X_test, y_train, y_test = self.get_encoded_data(data_path, labels_path, test_size=test_size, data_sep=data_sep)
        models,predictions = clf.fit(X_train, X_test, y_train, y_test)
        print(models)
        with open("NLPResult_new.txt", 'a+', encoding='utf-8') as f:
            f.write(str(models)+"\n")