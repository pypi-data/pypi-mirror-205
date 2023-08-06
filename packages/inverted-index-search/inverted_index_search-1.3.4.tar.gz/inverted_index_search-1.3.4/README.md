# inverted-index-search
inverted-index-search is python library for searching up keywords or sub words in a corpus of data using inverted index lookup

## Installation

Use the package manager pip to install.

```bash
pip install inverted-index-search
```

## Usage

The library's usage is straightforward, and it can be easily imported into your Python script. The make_doc_ngrams function breaks down the document into n-grams, and the search_doc function finds matching substrings in the document. You can specify the n-gram size and the type of n-gram level (word or character) for the search.

Here is an example of how to use the library:

```python
from  inverted_index_search import search_doc


#This breaks down the document in ngrams to be used for searching
document_ngrams = make_doc_ngrams("this is big document with multiple words and sentences", "word", [1,2], verbose=True)
>> DOCUMENT N GRAMS => [1, 2]
>> Removing these ngrams :  
>> DOCUMENT NGRAM LOOKUP TABLE => {'this': [(0, 4)], 'is': [(2, 4), (5, 7)], 'big': [(8, 11)], 'document': [(12, 20)], 'with': [(21, 25)], 'multiple': [(26, 34)], 'words': [(35, 40)], 'and': [(41, 44)], 'sentences': [(45, 54)], 'this is': [(0, 7)], 'is big': [(5, 11)], 'big document': [(8, 20)], 'document with': [(12, 25)], 'with multiple': [(21, 34)], 'multiple words': [(26, 40)], 'words and': [(35, 44)], 'and sentences': [(41, 54)]}



#This breaks down the phrases and actually does the matching
search_doc(document_ngrams, ['document' , 'multiple words'], [1], 'word', verbose=True))
>> Phrase N GRAMS => [1]
Checking for phrase ngram : document
Checking for phrase ngram : multiple
Checking for phrase ngram : words
>> {'document': {'document': {'count': 1, 'occured': [(12, 20)]}}, 'multiple words': {'multiple': {'count': 1, 'occured': [(26, 34)]}, 'words': {'count': 1, 'occured': [(35, 40)]}}}


print(search_doc.__doc__)
>>  """ This function creates ngrams out of the phrases you have
    entered and finds the matching substrings in the document. You can specify what ngram for using phrase_ngrams paramter and
   . Simply pass phrase_ngrams=[1,7,2] to create ngrams of size 1,7 and 2. There are two level ngram either words or chaarcter which
    you can change by changing the n_gram_level to either 'char' or 'word'. To turn on logging setting verbose to True"""

```

## Features

    Efficient inverted index search for large text data sets
    Customizable n-gram size and level (word or character)
    Simple and easy-to-use API
    Built-in logging for debugging and testing purposes

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Github

[Affan](https://github.com/Affanmir)
