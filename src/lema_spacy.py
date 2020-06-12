import spacy
nlp = spacy.load('es_core_news_sm')
text = 'Soy un texto que pide a gritos que lo procesen. Por eso yo canto, tú cantas, ella canta, nosotros cantamos, cantáis, cantan…'
doc = nlp(text)
lemmas = [tok.lemma_.lower() for tok in doc]
print(lemmas)