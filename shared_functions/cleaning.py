from langdetect import detect_langs
import nltk
from nltk.corpus import wordnet
import string


def clean_text(text):
    """
    Converts text to lowercase and removes punctuation/digits.

    Parameters:
    text (string): string which contains some unclean text

    Returns:
    Text that is in lowercase and removed punctuation/digits

   """
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation + '“”’—'))
    text = text.translate(str.maketrans('', '', string.digits))

    return text.strip()


def valid_english(row):
    """
    Checks if a review is in english (with at least 90% confidence).

    Parameters:
    row (Series): row which contains one review by a user for one movie

    Returns:
    True if langdetect is at least 90% confident that the review is in english.
    False otherwise.

   """
    try:
        # detect language(s) of review and their confidence
        lang_prob = detect_langs(row.review)
        lang, prob = str(lang_prob[0]).split(':')
        # return True if most probable langauge is english and has at least 90% confidence

        # TODO: cross validate here for probability?

        return lang == 'en' and prob > '0.9'
    # if the review does not contain letters, it will throw an exception and return False
    except:
        return False


def lemmatize(text, lemmatizer):
    """
    Lemmatizes the text.

    Parameters:
    text (string): string with unlemmatized text.
    lemmatizer (WordNetLemmatizer): WordNet lemmatizer.

    Returns:
    Lemmatized text.

   """
    # tokenize the text, then for each token, lemmatize the token
    words = [lemmatizer.lemmatize(w, wordnet_pos_tag(w)) for w in nltk.word_tokenize(text)]

    # join text back into a string
    return ' '.join(words)


def wordnet_pos_tag(word):
    """
    Tags word with a "part of speech" (POS) tag. This is necessary because the lemmatization process needs
    some context in order to get the lemma of a word. For example, a word that can be represented as both a noun
    and a verb may have different lemmas.

    Wordnet accepts only 4 different tags: adjective, noun, verb or adverb.
    nltk.pos_tag() gives many different tags. These tags will be mapped according to the first letter of its tag
    to a wordnet tag. Other tags that do not fit into these 4 categories will by default be tagged as a noun.

    Parameters:
    word (string): a word from a review.

    Returns:
    wordnet POS tag for that word

   """
    # nltk.pos_tag will return a tag in the format: [('Dog', 'NN')]
    # we need to get the first letter of the tag, namely 'N'
    tag = nltk.pos_tag([word])[0][1][0].upper()

    # define the four mappings of nltk pos tags to wordnet tags
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    # return the correct mapping or, if unavailable, return noun by default
    return tag_dict.get(tag, wordnet.NOUN)
