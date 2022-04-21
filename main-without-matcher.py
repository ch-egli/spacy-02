import spacy

nlp = spacy.load("de_core_news_sm")

# with open('books/Kafka-Verwandlung.txt', encoding='utf8') as f:
# with open('books/Lessing-EmiliaGalotti.txt', encoding='utf8') as f:
# with open('books/Lessing-NathanDerWeise.txt', encoding='utf8') as f:
# with open('books/Spyri-HeidisLehrUndWanderjahre.txt', encoding='utf8') as f:
# with open('books/Hoffmann-derGoldeneTopf.txt', encoding='utf8') as f:
# with open('books/Goethe-DieLeidenDesJungenWerther.txt', encoding='utf8') as f:
# with open('books/odi.txt', encoding='utf8') as f:
with open('books/Schiller-DieRaeuber.txt', encoding='utf8') as f:
    document = nlp(f.read())

    countAnadiplose = 0
    previous_sentence = None
    for sentence_counter, sentence in enumerate(document.sents):
        if previous_sentence is not None and len(previous_sentence) > 1:
            if sentence[0].lemma_ == previous_sentence[-2].lemma_:
                countAnadiplose += 1
                print(sentence[0].lemma_, ' * ', previous_sentence.text.replace('\n', ' '), '|',
                      sentence.text.replace('\n', ' '))
        previous_sentence = sentence

    print("")
    countAsyndetonComma = 0
    for sentence_counter, sentence in enumerate(document.sents):
        if len(sentence) > 4:
            for x in range(0, len(sentence) - 4):
                if sentence[x].is_alpha and \
                        sentence[x + 1].is_punct and sentence[x + 1].text == ',' and \
                        sentence[x + 2].is_alpha and \
                        sentence[x + 3].is_punct and sentence[x + 1].text == ',' and \
                        sentence[x + 4].is_alpha:
                    countAsyndetonComma += 1
                    print(sentence.text.replace('\n', ' '))

    print("")
    countAsyndetonOther = 0
    for sentence_counter, sentence in enumerate(document.sents):
        if len(sentence) > 4:
            for x in range(0, len(sentence) - 4):
                if sentence[x].is_alpha and \
                        sentence[x + 1].is_punct and sentence[x + 1].text != ',' and \
                        sentence[x + 2].is_alpha and \
                        sentence[x + 3].is_punct and sentence[x + 1].text != ',' and \
                        sentence[x + 4].is_alpha:
                    countAsyndetonOther += 1
                    print(sentence.text.replace('\n', ' '))

    print("")
    print("Summary: ")
    print("- matches Anadiplose: ", countAnadiplose)
    print("- matches Asyndeton (comma): ", countAsyndetonComma)
    print("- matches Asyndeton (other): ", countAsyndetonOther)

# https://universaldependencies.org/u/pos/
# https://www.linguistik.hu-berlin.de/de/institut/professuren/korpuslinguistik/mitarbeiter-innen/hagen/STTS_Tagset_Tiger
# https://files.ifi.uzh.ch/cl/siclemat/lehre/hs13/ecl1/script/script.pdf
