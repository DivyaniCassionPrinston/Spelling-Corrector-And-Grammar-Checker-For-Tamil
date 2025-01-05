import re
from collections import Counter
from typing import List

from levenshtein_utils import lev  
from levenshtein_utils import prefix_match, suffix_match


def prefilter_candidates(user_input, correct_words, length_threshold=2):
    return [
        word for word in correct_words
        if abs(len(word) - len(user_input)) <= length_threshold
    ]


def suggestions(user_input, correct_words, top_n=5):
    candidates = []
    filtered_correct_words = prefilter_candidates(user_input, correct_words)

    # Weight for penalty
    w_lev = 0.7  
    # Weight for prefix match - reward
    w_prefix = 0.15  
     # Weight for suffix match - reward
    w_suffix = 0.15 

    for word in filtered_correct_words:
        lev_score = lev(user_input, word)
        prefix_score = prefix_match(user_input, word)
        suffix_score = suffix_match(user_input, word)


        score = w_lev * lev_score - w_prefix * prefix_score - w_suffix * suffix_score
        candidates.append((word, score))

    candidates = sorted(candidates, key=lambda x: x[1])
    return [candidate[0] for candidate in candidates[:top_n]] if candidates else [user_input]



class SpellChecker:
    def __init__(self, correct_words):
        self.correct_words = correct_words  
        
    def suggestions(self, word):

        suggested_words = sorted(self.correct_words, key=lambda w: lev(word, w))
        return suggested_words[:5]  

    def correct(self, sentence):
    
        corrected_words = []
        for word_to_check in sentence.split(): 
            suggested_words = self.suggestions(word_to_check)

            best_match = suggested_words[0]
            corrected_words.append(best_match)

        return " ".join(corrected_words)  
