# CSE 597 001 Vocab Parser and Generator
import sys, os
import xml.etree.ElementTree as ET


class Generator:
    class Method:
        # Vocab and sentences are strictly space separated values
        SPACE_SPLIT = 0
        # Vocab and sentences are stripped of punctuation
        SPACE_SPLIT_NO_PUNCT = 1
        # Vocab and sentences are stripped of punctuation and possessives
        SPACE_SPLIT_NO_PUNCT_POSSESSIVES = 2
        # Vocab and sentences are stripped of punctuation, splits on corpus data in attempt to fix minor errors
        SPACE_SPLIT_NO_PUNCT_FIX = 3
        # Vocab and sentences are stripped of punctuation and possessives, splits on corpus data in attempt to fix minor errors
        SPACE_SPLIT_NO_PUNCT_POSSESSIVES_FIX = 4

    en_vocab = set()
    vi_vocab = set()

    def __init__(self, en_output, vi_output):
        self.en = open(en_output, 'w', encoding='utf-8')
        self.vi = open(vi_output, 'w', encoding='utf-8') if vi_output and en_output != vi_output else self.en

    def save_all(self):
        vi_count = 0
        en_count = 0

        for word in self.en_vocab:
            if word == '' or word == '\n' or word is None:
                continue
            self.en.write(word + '\n')
            en_count += 1

        for word in self.vi_vocab:
            if word == '' or word == '\n' or word is None:
                continue
            self.vi.write(word + '\n')
            vi_count += 1

        self.en.close()
        self.vi.close()
        self.en_vocab.clear()
        self.vi_vocab.clear()

        return vi_count, en_count

    def feed_en(self, sentence, method):
        for word in self.get_ens_from_sentence_with_method(sentence, method):
            self.en_vocab.add(word)

    def get_ens_from_sentence_with_method(self, sentence, method):
        words = []
        for word in sentence.split(' | '):
            if method == self.Method.SPACE_SPLIT:
                words.append(word)
            elif method == self.Method.SPACE_SPLIT_NO_PUNCT:
                words.append(word)
            elif method == self.Method.SPACE_SPLIT_NO_PUNCT_POSSESSIVES:
                words.append(word)
            elif method == self.Method.SPACE_SPLIT_NO_PUNCT_FIX:
                words.append(word)
            elif method == self.Method.SPACE_SPLIT_NO_PUNCT_POSSESSIVES_FIX:
                words.append(word)
            else:
                raise AttributeError('Method \'{}\' was not found for en parsing!'.format(method))
        return words

    def feed_vi(self, sentence, method):
        for word in self.get_vis_from_sentence_with_method(sentence, method):
            self.vi_vocab.add(word)

    def get_vis_from_sentence_with_method(self, sentence, method):
        words = []
        for word in sentence.split(' '):
            if method == self.Method.SPACE_SPLIT:
                words.append(word)

            elif method == self.Method.SPACE_SPLIT_NO_PUNCT:
                words.append(word.lstrip('(\'".,-)').strip('.,)("\\;:/-\''))

            elif method == self.Method.SPACE_SPLIT_NO_PUNCT_POSSESSIVES:
                w = word.lstrip('(\'".,-)').strip('.,)("\\;:/-\'')
                if w.endswith('\'s') or w.endswith('\'d'):
                    w = w[:-2]
                words.append(w)

            elif method == self.Method.SPACE_SPLIT_NO_PUNCT_FIX:
                new_sentence = word.lstrip('(\'".,-)').strip('.,)("\\;:/-\'')

                # Is there text surrounding a dot? Fixes items such as: 'Representatives.Barack' and NOT '17068.8'
                if '.' in new_sentence and (new_sentence.index('.') + 1) < len(new_sentence) and new_sentence.index('.') > 0 and str.isalnum(new_sentence[new_sentence.index('.') - 1]) and str.isalpha(new_sentence[new_sentence.index('.') + 1]):
                    new_sentence = new_sentence[:new_sentence.index('.')] + ' ' + new_sentence[new_sentence.index('.') + 1:]
                    for w in self.get_vis_from_sentence_with_method(new_sentence, method):
                        words.append(w)
                    continue
                # Is there text surrounding a comma? Fixes items such as: 'Mexico,United' and NOT '520,906,000'
                elif ',' in new_sentence and (new_sentence.index(',') + 1) < len(new_sentence) and new_sentence.index(',') > 0 and str.isalnum(new_sentence[new_sentence.index(',') - 1]) and str.isalpha(new_sentence[new_sentence.index(',') + 1]):
                    new_sentence = new_sentence[:new_sentence.index(',')] + ' ' + new_sentence[new_sentence.index(',') + 1:]
                    for w in self.get_vis_from_sentence_with_method(new_sentence, method):
                        words.append(w)
                    continue
                # Is there text surrounding a parentheses? Fixes items such as: 'Helena(mass'
                elif '(' in new_sentence and (new_sentence.index('(') + 1) < len(new_sentence) and new_sentence.index('(') > 0:
                    new_sentence = new_sentence[:new_sentence.index('(')] + ' ' + new_sentence[new_sentence.index('(') + 1:]
                    for w in self.get_vis_from_sentence_with_method(new_sentence, method):
                        words.append(w)
                    continue
                # Is there text surrounding a parentheses? Fixes items such as: 'city),Trenton'
                elif ')' in new_sentence and (new_sentence.index(')') + 1) < len(new_sentence) and new_sentence.index(')') > 0:
                    new_sentence = new_sentence[:new_sentence.index(')')] + ' ' + new_sentence[new_sentence.index(')') + 1:]
                    for w in self.get_vis_from_sentence_with_method(new_sentence, method):
                        words.append(w)
                    continue
                words.append(new_sentence)

            elif method == self.Method.SPACE_SPLIT_NO_PUNCT_POSSESSIVES_FIX:
                new_sentence = word.lstrip('(\'".,-)').strip('.,)("\\;:/-\'')
                if new_sentence.endswith('\'s') or new_sentence.endswith('\'d'):
                    new_sentence = new_sentence[:-2]

                # Is there text surrounding a dot? Fixes items such as: 'Representatives.Barack' and NOT '17068.8'
                if '.' in new_sentence and (new_sentence.index('.') + 1) < len(new_sentence) and new_sentence.index('.') > 0 and str.isalnum(new_sentence[new_sentence.index('.') - 1]) and str.isalpha(new_sentence[new_sentence.index('.') + 1]):
                    new_sentence = new_sentence[:new_sentence.index('.')] + ' ' + new_sentence[new_sentence.index('.') + 1:]
                    for w in self.get_vis_from_sentence_with_method(new_sentence, method):
                        words.append(w)
                    continue
                # Is there text surrounding a comma? Fixes items such as: 'Mexico,United' and NOT '520,906,000'
                elif ',' in new_sentence and (new_sentence.index(',') + 1) < len(new_sentence) and new_sentence.index(',') > 0 and str.isalnum(new_sentence[new_sentence.index(',') - 1]) and str.isalpha(new_sentence[new_sentence.index(',') + 1]):
                    new_sentence = new_sentence[:new_sentence.index(',')] + ' ' + new_sentence[new_sentence.index(',') + 1:]
                    for w in self.get_vis_from_sentence_with_method(new_sentence, method):
                        words.append(w)
                    continue
                # Is there text surrounding a parentheses? Fixes items such as: 'Helena(mass'
                elif '(' in new_sentence and (new_sentence.index('(') + 1) < len(new_sentence) and new_sentence.index('(') > 0:
                    new_sentence = new_sentence[:new_sentence.index('(')] + ' ' + new_sentence[new_sentence.index('(') + 1:]
                    for w in self.get_vis_from_sentence_with_method(new_sentence, method):
                        words.append(w)
                    continue
                # Is there text surrounding a parentheses? Fixes items such as: 'city),Trenton'
                elif ')' in new_sentence and (new_sentence.index(')') + 1) < len(new_sentence) and new_sentence.index(')') > 0:
                    new_sentence = new_sentence[:new_sentence.index(')')] + ' ' + new_sentence[new_sentence.index(')') + 1:]
                    for w in self.get_vis_from_sentence_with_method(new_sentence, method):
                        words.append(w)
                    continue
                words.append(new_sentence)
            else:
                raise AttributeError('Method \'{}\' was not found!'.format(method))
        return words

# Example usage definition
if __name__ == '__main__':
    # Create a new Generator
    g = Generator('vocab.en', 'vocab.vi')
    # Get all the corpus files in the 'unprocessed_data' folder
    corpus_files = [os.path.join(r, file) for r, d, f in os.walk('..\\unprocessed_data') for file in f]
    # Get the generator method
    method = int(input('Generator Method (0-4): '))
    # For each corpus file
    for corpus_file in corpus_files:
        # Print the filename being processed
        print('Parsing: ' + corpus_file)
        # Open the corpus file
        entries = ET.parse(corpus_file).getroot()[0]
        # Go through each entry
        for entry in entries:
            # Go through each entries attributes
            for tags in entry:
                # Is this a lex attribute?
                if tags.tag == 'lex':
                    # Feed this sentence to the vocab generator
                    g.feed_vi(tags.text, method)
                # Is this a modified triple set attribute?
                elif tags.tag == 'modifiedtripleset':
                    # Get all mtrip attributes
                    for mtrip in tags:
                        # Feed this sentence to the vocab generator
                        g.feed_en(mtrip.text, method)
    # Save the vocab files
    vi, en = g.save_all()
    print('Created {} vi vocab words and {} en words'.format(vi, en))

    # Given test sentence
    test_en_sentence = "Alfa_Romeo_164 | assembly | Milan | Alfa_Romeo_164 | related | Saab_9000"
    test_vi_sentence = "The Alfa Romeo 164, which is assembled in Milan, is a related means of transportation to Saab 9000 , in that they are both cars."
    # This is how you can extract sentences, simply by a join on a space
    print(test_en_sentence)
    print("becomes")
    print(' | '.join(g.get_ens_from_sentence_with_method(test_en_sentence, g.Method.SPACE_SPLIT_NO_PUNCT_POSSESSIVES_FIX)))

    print(test_vi_sentence)
    print("becomes")
    print(' '.join(g.get_vis_from_sentence_with_method(test_vi_sentence, g.Method.SPACE_SPLIT_NO_PUNCT_POSSESSIVES_FIX)))
