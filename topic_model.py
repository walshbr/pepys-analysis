import nltk
import gensim
import gensim.corpora as corpora
from gensim.corpora import Dictionary
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel

from pprint import pprint

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis



import diary_analysis
diary = diary_analysis.Diary('sp_diary.json')
# using this - https://neptune.ai/blog/pyldavis-topic-modelling-exploration-tool-that-every-nlp-data-scientist-should-know
entries = [entry.clean_tokens for entry in diary.entries]
entries[0:5]
id2word = Dictionary(entries)
# corpus = [id2word.doc2bow(entry) for entry in diary.entries]
# print(id2word)

corpus = [id2word.doc2bow(text) for text in entries]

lda_model = LdaModel(corpus=corpus,
                   id2word=id2word,
                   num_topics=100,
                   random_state=0,
                   chunksize=100,
                   alpha='auto',
                   per_word_topics=True)

pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]
import pyLDAvis.gensim_models as gensimvis
lda_viz = gensimvis.prepare(lda_model, corpus, id2word, mds='mmds')
with open('output.html','w') as fout:
    pyLDAvis.save_html(lda_viz,fout)