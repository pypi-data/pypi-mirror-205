
"""
Removes stopwords with nltk.
List of provided languages:
from nltk.corpus import stopwords
print(stopwords.fileids())
"""

from nltk.corpus import stopwords as st


def remove_stopwords(text: str,
                     stopwords = []):

    additional_stopwords = set(["i'm","i'd","i've","we'd","we've","he'd","she'd","it'd",
                                "they'd","it'll","it's"])

    for language in stopwords:
        stops= set(st.words(language))
        if 'english' in language :
            stops_extended = stops.union(additional_stopwords)
            filtered_words = [word for word in text.split() if word.lower() not in stops_extended]
        else:
            filtered_words = [word for word in text.split() if word.lower() not in stops]


    return " ".join(filtered_words)