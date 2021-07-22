import turicreate as tc

docs = tc.SFrame('Netflix.com.txt')

# Remove stop words and convert to bag of words
docs = tc.text_analytics.count_words(docs)
docs = docs.dict_trim_by_keys(tc.text_analytics.stop_words(), exclude=True)

# Learn topic model
model = tc.topic_model.create(docs)