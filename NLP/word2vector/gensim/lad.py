from gensim import corpora, models

d = [['想', '买辆', '汽车'], ['我', '买辆', '汽车', '汽车', '喜欢']]
dictionary = corpora.Dictionary(d)
dictionary.save('./gensim.dict')
corpora.Dictionary.load('./gensim.dict')
print(dictionary)

corpus = [dictionary.doc2bow(text) for text in d]  # bag of words
print(corpus)

lda = models.LdaModel(corpus=corpus, num_topics=2, id2word=dictionary)
print(lda.print_topics(2))
print(lda[corpus[0]])
