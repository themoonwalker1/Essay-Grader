from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances


corpus=[
'Gaming',
'Kind of cool',
'Government shutdown',
'and steve',
'coronavirus'
]


vec = CountVectorizer()
features = vec.fit_transform(corpus).todense()
print(vec.vocabulary_)

print(len(corpus))

for i in range(0, len(corpus)):
  for f in features:
    print("Task: " + str(i) + str( euclidean_distances(features[i], f)))
