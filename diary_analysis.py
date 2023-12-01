import os
import string
import json
import nltk

class Diary(object):
    def __init__(self, json_file):
        # all the attributes we want the class to have
        with open(json_file, 'r') as fin:
            self.json = json.load(fin)
        self.entries = [DiaryEntry(entry) for entry in self.json]
        # above is a one line version of the next few lines
        # entries = []
        # for entry in self.json:
        #     entries.append(DiaryEntry(entry))
        all_raw_tokens = []
        for entry in self.entries:
            all_raw_tokens.extend(entry.tokens)
        self.all_raw_tokens = all_raw_tokens
        self.raw_fq = nltk.FreqDist(self.all_raw_tokens)
        
        all_clean_tokens = []
        for entry in self.entries:
            all_clean_tokens.extend(entry.clean_tokens)
        self.all_clean_tokens = all_clean_tokens

        self.clean_fq = nltk.FreqDist(self.all_clean_tokens)

        self.nltk_version_of_diary = nltk.Text(self.all_raw_tokens)


# the Text class works the same as the Corpus, but will contain text-level only attributes
class DiaryEntry(object):
    # now create the blueprint for our text object
    def __init__(self, this_dict):
        self.year = this_dict['year']
        self.month = this_dict['month']
        self.date = this_dict['date']
        self.entry_date = this_dict['entry_date']
        self.entry_text = ' '.join(this_dict['entry_text'])
        self.endnotes = this_dict['endnotes']
        self.footnotes = this_dict['footnotes']
        self.annotations = this_dict['annotations']
        self.url = this_dict['url'] 
        self.tokens = nltk.word_tokenize(self.entry_text)
        stopwords_list = nltk.corpus.stopwords.words('english')
        stopwords_list_with_punct = list(string.punctuation) + stopwords_list
        self.clean_tokens = [token for token in self.tokens if token not in stopwords_list_with_punct]
        
# this is what runs if you run the file as a one-off 
def main():
    diary_file = 'sp_diary.json'

# this allows you to import the classes as a module. it uses the special built-in variable __name__ set to the value "__main__" if the module is being run as the main program
if __name__ == "__main__":
    main()


# python3 
# get the thing in the terminal
# >>> import diary_analysis
# >>> diary = diary_analysis.Diary('sp_diary.json')

# output all entries
# >>> diary.entries

# output the first entry
# >>> diary.entries[0]

# output the nltk version of the diary
# >>> diary.nltk_version_of_diary.collocations()

# when you change something
# >>> import importlib
# >>> importlib.reload(diary_analysis)