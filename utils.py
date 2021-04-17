import string
from wordcloud import STOPWORDS

def remove_punctuation(contents):
    letter = list()
    for content in contents.rstrip().lower():
        if content in string.punctuation or content in string.digits:
            continue
        letter.append(content)
    return ''.join(letter)


def filter_text(text):
    temp = list()
    words = text.split()
    for word in words:
        if word in set(STOPWORDS):
            continue
        temp.append(word)
    return temp


def calculate_frequencies(words):
    counts = dict()
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def plot_cloud(cloud):
    plt.figure(figsize=(12,10))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()