import string
import re
import pickle

'''
desc: This function takes in a the name of a file and returns the contents in a list with correct formatting. 
pre: filename
post: lines - list of all the words from file
'''
def tokenize_file(filename):
    with open(filename) as f:
        lines = f.read().lower().splitlines()
        lines = [line for line in lines if line] 
        lines = [re.sub(r'’', '\'', line) for line in lines] # swap ’ for ' 
        lines = [re.split("(?:(?:[^a-zA-Z]+')|(?:'[^a-zA-Z]+))|(?:[^a-zA-Z']+)", line) for line in lines]
        #lines = [word for line in lines for word in line if word != '' ]   
    return lines

'''
pre: lines - a list of lines
post: unigram_dict - a dictionary of unigrams created from lines
'''
def unigramizer(lines):
    unigram_dict = {}
    for line in lines:
        for word in line:
            if word in unigram_dict:
                unigram_dict[word] = unigram_dict[word] + 1
            else:
                unigram_dict[word] = 1
    return unigram_dict

'''
pre: lines - a list of lines
post: bigram_dict - a dictionary of bigrams created from lines
'''
def bigramizer(lines):
    bigram_dict = {}    
    for line in lines:
        line = ['<s>'] + line + ['</s>']
        for i in range(len(line) - 1):
            bigram = tuple(line[i + j] for j in range(2))
            if bigram in bigram_dict:
                bigram_dict[bigram] = bigram_dict[bigram] + 1
            else:
                bigram_dict[bigram] = 1
    return bigram_dict

'''
pre: lines - a list of lines
post: trigram_dict - a dictionary of trigrams created from lines
'''
def trigramizer(lines):
    trigram_dict = {}
    for line in lines:
        line = ['<s>'] + line + ['</s>']
        for i in range(len(line) - 2):
            trigram = tuple(line[i + j] for j in range(3))
            if trigram in trigram_dict:
                trigram_dict[trigram] = trigram_dict[trigram] + 1
            else:
                trigram_dict[trigram] = 1
    return trigram_dict

'''
pre: lines - a list of lines
post: quadgram_dict - a dictionary of quadgrams created from lines
'''
def quadgramizer(lines):
    quadgram_dict = {}
    for line in lines:
        line = ['<s>'] + line + ['</s>']
        for i in range(len(line) - 3):
            quadgram = tuple(line[i + j] for j in range(4))
            if quadgram in quadgram_dict:
                quadgram_dict[quadgram] = quadgram_dict[quadgram] + 1
            else: 
                quadgram_dict[quadgram] = 1 
    return quadgram_dict
'''
pre: ngram_dict - a dictionary of ngrams, size - dict size
post: returns a dictionary w/ relative frequency
''' 
def compute_relative_freq(ngram_dict, size):
    return [(key, float(item)/size) for key, item in ngram_dict.items()]

'''
pre: takes in u,b,t,q - ngram dictionaries
post: returns c_probs - an array of cumulative probabilities for each ngram dictionary
'''
def compute_cumulative_prob(u, b, t, q):
    c_probs = []
    u_rel_freq = compute_relative_freq(u, len(u))
    b_rel_freq = compute_relative_freq(b, len(b))
    t_rel_freq = compute_relative_freq(t, len(t))
    q_rel_freq = compute_relative_freq(q, len(q))
    
    c_probs.append(c_probs_helper(u_rel_freq))
    c_probs.append(c_probs_helper(b_rel_freq))
    c_probs.append(c_probs_helper(t_rel_freq))
    c_probs.append(c_probs_helper(q_rel_freq))
    return c_probs

'''
pre: n_rel_freq - ngram relative frequency dictionary
post: cumulative_prob - ngram cumulative probability
'''
def c_probs_helper(n_rel_freq):
    prob_sum = 0
    cumulative_prob = []
    for i in n_rel_freq:
        cumulative_prob.append((i[0], i[1] + prob_sum))
        prob_sum = prob_sum + i[1]
    return cumulative_prob

def pickle_(c_probs):
    fout = open ('proj7b.pkl','wb')
    pickle.dump(c_probs,fout)
    fout.close()

def main():
    lines = tokenize_file('shakespeare.txt')

    # compute unigram, bigram, trigram, and quadgram dicts
    unigram_dict = unigramizer(lines)
    bigram_dict = bigramizer(lines)
    trigram_dict = trigramizer(lines)
    quadgram_dict = quadgramizer(lines)

    # make an array of cumulative probabilities of each dict
    c_probs = compute_cumulative_prob(unigram_dict, bigram_dict, trigram_dict, quadgram_dict)
    
    # send it through the pickler
    pickle_(c_probs)


main()