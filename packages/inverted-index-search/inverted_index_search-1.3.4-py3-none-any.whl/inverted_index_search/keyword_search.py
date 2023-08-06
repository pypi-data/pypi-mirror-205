import nltk
from nltk.util import ngrams
import warnings
import re
import nltk


def util_len(f):
    return len(f.strip().split(" "))


def clean_doc(doc_lst, removal):
    new_lst = []
    for i in doc_lst:
        if i not in removal:
            new_lst.append(i)
    return new_lst


def true_ngram_index(find, string):
    return [(m.start(), m.end()) for m in re.finditer(find, string)]


def check_warnings(n_gram_level, phrase_ngrams, phrases):
    if n_gram_level != 'word' and n_gram_level != 'char':
        raise Exception("Sorry, Ngram level can be either 'word' or 'char'")

    if len(phrase_ngrams) == 0:
        phrase_ngrams = set(
            [i for i in range(1, len(max(phrases, key=util_len).split(" "))+1)])

    else:
        for i in phrase_ngrams:
            if type(i) != int:
                raise Exception(
                    "Sorry, document ngrams range must be integer types")

    if n_gram_level == 'char' and (1 in phrase_ngrams):
        warnings.warn(
            "Ngrma is set to 'char' and either document or phrases ngrams are set to 1; This will case extreme matching")

        response = input("Do you want to continue? (y/n)")

        if response.lower() != 'y':
            print("Exiting program...")
            exit()
        else:
            print("Continuing program...")
    return (phrase_ngrams)


def make_doc_ngrams(doc: str, ngram_level: str, doc_ngram: list = [], remove_gram=[" "], verbose=False):
    if ngram_level != 'word' and ngram_level != 'char':
        raise Exception("Sorry, Ngram level can be either 'word' or 'char'")
    for i in doc_ngram:
        if type(i) != int:
            raise Exception("Sorry, document ngrams must be integer types")
    if ngram_level == 'char' and (1 in ngram_level):
        warnings.warn(
            "Ngram level is set to 'char' and either document ngrams are set to 1; This will case extreme matching")
        response = input("Do you want to continue? (y/n)")
        if response.lower() != 'y':
            print("Exiting program...")
            exit()
        else:
            print("Continuing program...")
    doc_ngrams_words = []

    for i in doc_ngram:
        if ngram_level == 'char':
            current_grams = list(ngrams(doc, i))
            for i in current_grams:
                doc_ngrams_words.append("".join(i))
        else:
            current_grams = list(ngrams(nltk.word_tokenize(doc), i))
            for i in current_grams:
                doc_ngrams_words.append(" ".join(i))

    doc_ngrams_words = clean_doc(doc_ngrams_words, remove_gram)
    n_gram_lookup = {}
    for grams in doc_ngrams_words:
        current_grams_span = true_ngram_index(grams, doc)
        if grams not in n_gram_lookup:
            n_gram_lookup[grams] = current_grams_span
    if verbose:
        print("DOCUMENT N GRAMS =>", doc_ngram)
        print("Removing these ngrams : " + ", ".join(remove_gram))
        print("DOCUMENT NGRAM LOOKUP TABLE =>", n_gram_lookup)
    return n_gram_lookup




make_doc_ngrams.__doc__ = """ This function creates ngrams out of the document you have
    specified and creates ngrams out of it for later matching. You can specify what ngram for using doc_ngrams paramter and
    . Simply pass doc_ngrams=[1,7,2] to create ngrams of size 1,7 and 2. There are two level ngram either words or chaarcter which
    you can change by changing the n_gram_level to either 'char' or 'word'. The remove_gram paramter is to remove specific ngrams that may 
    occur during generation. Supposedly you may want to add common words to this list that you do not
    want to be matched. To turn on logging setting verbose to True"""


def search_doc(n_gram_lookup, phrases: list,  phrase_ngrams: list = [], n_gram_level: str = 'word', verbose=False) -> dict:

    phrase_ngrams = check_warnings(n_gram_level, phrase_ngrams, phrases)
    if verbose:
        print("Phrase N GRAMS =>", phrase_ngrams)

    key_matches = {}
    for value in phrases:
        for nthgram in phrase_ngrams:
            if n_gram_level == 'char':
                current_grams = ngrams(value, nthgram)
                for curent_gram in current_grams:
                    if verbose:
                        print("Checking for phrase ngram : " +
                              str(curent_gram[0]))
                    cur_gram = "".join(curent_gram)
                    if cur_gram in n_gram_lookup:
                        if value not in key_matches:
                            key_matches[value] = {cur_gram: {"count": len(
                                n_gram_lookup[cur_gram]), "occured": n_gram_lookup[cur_gram]}}
                        else:

                            if cur_gram not in key_matches[value]:
                                key_matches[value][cur_gram] = {"count": len(
                                    n_gram_lookup[cur_gram]), "occured": n_gram_lookup[cur_gram]}
                            else:
                                key_matches[value][cur_gram]["occured"] += n_gram_lookup[cur_gram]
                                key_matches[value][cur_gram]['count'] += len(
                                    n_gram_lookup[cur_gram])
            else:
                current_grams = ngrams(nltk.word_tokenize(value), nthgram)
                for curent_gram in current_grams:
                    if verbose:
                        print("Checking for phrase ngram : " +
                              str(" ".join(curent_gram)))
                    cur_gram = " ".join(curent_gram)
                    if cur_gram in n_gram_lookup:
                        if value not in key_matches:
                            key_matches[value] = {cur_gram: {"count": len(
                                n_gram_lookup[cur_gram]), "occured": n_gram_lookup[cur_gram]}}
                        else:
                            if cur_gram not in key_matches[value]:
                                key_matches[value][cur_gram] = {"count": len(
                                    n_gram_lookup[cur_gram]), "occured": n_gram_lookup[cur_gram]}
                            else:
                                key_matches[value][cur_gram]["occured"] += n_gram_lookup[cur_gram]
                                key_matches[value][cur_gram]['count'] += len(
                                    n_gram_lookup[cur_gram])

    return key_matches


search_doc.__doc__ = """ This function creates ngrams out of the phrases you have
    entered and finds the matching substrings in the document. You can specify what ngram for using phrase_ngrams paramter and
   . Simply pass phrase_ngrams=[1,7,2] to create ngrams of size 1,7 and 2. There are two level ngram either words or chaarcter which
    you can change by changing the n_gram_level to either 'char' or 'word'. To turn on logging setting verbose to True"""



#document_ngrams = make_doc_ngrams("this is big document with multiple words and sentences", "word", [1,2], verbose=True)
#print(search_doc(document_ngrams, ['document' , 'multiple words'], [1], 'word', verbose=True))
