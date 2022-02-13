import spacy
import pandas as pd
from spacy.matcher import Matcher


def extract_tokens_plus_meta(doc: spacy.tokens.doc.Doc):
    """Extract tokens and metadata from individual spaCy doc."""
    data = []
    for sentence_counter, sentence in enumerate(doc.sents):
        for token in sentence:
            data.insert(0, [sentence_counter, token.text, token.lemma_, token.pos_, token.morph,
                            token.is_alpha, token.is_digit, token.is_punct, token.is_sent_start, token.is_sent_end])
    # return array in reverse order
    return data[::-1]


def tidy_tokens(doc):
    """Extract tokens and metadata from list of spaCy docs."""

    cols = [
        "doc_id", "sentence_id", "token", "lemma",
        "pos (Wortart)", "morph", "is_alpha", "is_digit", "is_punct", "sentence-start", "sentence-end"
    ]

    meta_df = []
    meta = extract_tokens_plus_meta(doc)
    meta = pd.DataFrame(meta)
    meta.columns = cols[1:]
    meta_df.append(meta)

    return pd.concat(meta_df)


nlp = spacy.load("de_core_news_sm")
matcher1 = Matcher(nlp.vocab)
pattern1 = [{'IS_ALPHA': True},
            {'IS_PUNCT': True},
            {'IS_ALPHA': True}]
matcher1.add("Anadiplose", [pattern1])

matcher2 = Matcher(nlp.vocab)
pattern2 = [{'IS_ALPHA': True},
            {'IS_PUNCT': True},
            {'IS_ALPHA': True},
            {'IS_PUNCT': True},
            {'IS_ALPHA': True}]
matcher2.add("Asyndeton", [pattern2])

# with open('books/Kafka-Verwandlung.txt', encoding='utf8') as f:
# with open('books/Lessing-EmiliaGalotti.txt', encoding='utf8') as f:
# with open('books/Lessing-NathanDerWeise.txt', encoding='utf8') as f:
with open('books/Spyri-HeidisLehrUndWanderjahre.txt', encoding='utf8') as f:
# with open('books/Hoffmann-derGoldeneTopf.txt', encoding='utf8') as f:
# with open('books/Schiller-DieRaeuber.txt', encoding='utf8') as f:
# with open('books/Goethe-DieLeidenDesJungenWerther.txt', encoding='utf8') as f:
# with open('books/odi.txt', encoding='utf8') as f:
    document = nlp(f.read())

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    # for debugging: print analysis...
    # print(tidy_tokens(document))

    countAnadiplose = 0
    matches1 = matcher1(document)
    print("-- Number of matches (Anadiplose): ", len(matches1))
    for match_id, start, end in matches1:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = document[start:end]  # The matched span
        if document[start].lemma_ == document[end - 1].lemma_:
            countAnadiplose += 1
            print(string_id, span.text)

    countAsyndeton = 0
    matches2 = matcher2(document)
    print("-- Number of matches (Asyndeton): ", len(matches2))
    for match_id, start, end in matches2:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = document[start:end]  # The matched span
        if (document[start + 1].text == ",") & (document[start + 3].text == ","):
            countAsyndeton += 1
            print(string_id, span.text)

    print("")
    print("Summary: ")
    print("- matches Anadiplose: ", countAnadiplose)
    print("- matches Asyndeton: ", countAsyndeton)

# https://universaldependencies.org/u/pos/
# https://www.linguistik.hu-berlin.de/de/institut/professuren/korpuslinguistik/mitarbeiter-innen/hagen/STTS_Tagset_Tiger
# https://files.ifi.uzh.ch/cl/siclemat/lehre/hs13/ecl1/script/script.pdf
