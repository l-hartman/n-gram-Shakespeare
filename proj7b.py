import pickle
import random

'''
pre: n/a 
post: returns the depickled cumulative probability dictionary.
'''
def depickle():
    fin = open('proj7b.pkl', 'rb')
    c_probs = pickle.load(fin)
    fin.close()
    return c_probs

'''
pre: takes in a unigram probability dictionary.
post: returns a list of sentences generated from the dictionary.
'''
def make_unigram_sentences(unigram_prob_dict):
    sentence_lst = []
    minval = 100
    maxval = 0
    # figure out min/max probabilities for rng
    for x in unigram_prob_dict:
        if minval > x[1]:
            minval = x[1]
        if maxval < x[1]:
            maxval = x[1]
    for _ in range(5):
        sentence = ''
        for _ in range(12):
            for i in unigram_prob_dict:
                if i[1] > random.uniform(minval, maxval):
                    word = i[0]
                    break
            # add word to sentence
            sentence += word + ' '
        ## remove trailing spaces
        sentence = sentence[:-1] 
        sentence += '.'
        sentence = sentence.capitalize()
        sentence_lst.append(sentence)
    return sentence_lst

''' 
Pre: prob_dict - a probability dictionary for a specific ngram dict, n is the number grams to be generated, size the number specifying the type of gram.
Post: returns a list of sentences generated from function input.
'''
def generate_sentences(prob_dict, size, n):
    sentence_lst = []
    for _ in range(5):
        sentence = ''
        for i in range(n):
            ngram = ''
            for x in prob_dict:
                if x[1] > random.random():
                    ngram = x[0]
                    break
            if i == 0 or i == n - 1:
                while((i == 0 and ngram[0] != '<s>') or (i == n - 1 and ngram[size - 1] != '</s>')):
                    for x in prob_dict:
                        if x[1] > random.random():
                            ngram = x[0]
                            break
            else:
                while(set(('<s>',)).issubset(ngram) or set(('</s>',)).issubset(ngram)):
                    ngram = ''
                    for x in prob_dict:
                        if x[1] > random.random():
                            ngram = x[0]
                            break
            for word in ngram:
                if not word == "":
                    sentence += word + ' '
        sentence = sentence[:-1] 
        sentence = sentence[:4] + sentence[4].upper() + sentence[5:-5] + '.' + sentence[-5:]
        sentence_lst.append(sentence)
    return sentence_lst

'''
pre: sentences - a list of strings 
'''
def print_list(sentences):
    for x in sentences:
        print("    " + x)
    print('\n')

def main():
    # reading in pickle file
    cumulative_probs = depickle()
    
    # print unigram sentences
    u_sentences = make_unigram_sentences(cumulative_probs[0])
    print("unigram sentences:")
    print_list(u_sentences)

    # print bigram sentences
    b_sentences = generate_sentences(cumulative_probs[1], 2, 6)
    print("bigram sentences:")
    print_list(b_sentences)

    # print trigram sentences
    t_sentences = generate_sentences(cumulative_probs[2], 3, 4)
    print("trigram sentences:")
    print_list(t_sentences)
    
    q_sentences = generate_sentences(cumulative_probs[3], 4, 3)
    print("quadgram sentences:")
    print_list(q_sentences)


main()