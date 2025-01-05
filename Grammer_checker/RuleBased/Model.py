import json
import nltk
from nltk.tokenize import word_tokenize

# Download the necessary tokenizer models
nltk.download('punkt')

class SpellCheckerModule:
    def __init__(self):
        # Load the rules from JSON files
        with open('subject_verb_rules.json', 'r', encoding='utf-8') as f:
            self.verb_rules = json.load(f)

        with open('tense_rules.json', 'r', encoding='utf-8') as f:
            self.subject_rules = json.load(f)

    def correct_spell(self, text):
        # Tokenize the text
        words = word_tokenize(text)
        corrected_words = []

        for word in words:
            # Check if the word is a known verb or subject and keep it
            if word in self.verb_rules or word in self.subject_rules:
                corrected_words.append(word)
            else:
                # If the word is not found, keep it as is
                corrected_words.append(word)

        return ' '.join(corrected_words)

    def correct_grammar(self, text):
        # Tokenize the text
        words = word_tokenize(text)
        corrected_grammar = []
        mistakes = []

        for i, word in enumerate(words):
            # Check if the current word is a subject
            if word in self.subject_rules:
                # Check the next word for verb agreement
                if i + 1 < len(words):
                    next_word = words[i + 1]
                    # If the next word is a verb, get the correct form based on the subject
                    if next_word in self.verb_rules:
                        correct_verb = self.verb_rules[next_word].get(word)
                        if correct_verb:
                            # Append the correct verb form
                            if isinstance(correct_verb, list):
                                # Choose the first correct verb form (or implement your selection logic)
                                corrected_grammar.append(correct_verb[0])
                            else:
                                corrected_grammar.append(correct_verb)
                        else:
                            # If no correct verb found, just append the original next word
                            corrected_grammar.append(next_word)
                            mistakes.append(next_word)  # Mark as mistake if no correction is found
                    else:
                        # If the next word is not a verb, just append it as is
                        corrected_grammar.append(next_word)
            else:
                # For non-subject words, just add them as they are
                corrected_grammar.append(word)

        corrected_text = ' '.join(corrected_grammar)

        # Final check for any incorrect forms
        for i, word in enumerate(corrected_grammar):
            # Check for additional subject-verb agreement errors
            if word in self.subject_rules and i + 1 < len(corrected_grammar):
                next_word = corrected_grammar[i + 1]
                if next_word in self.verb_rules:
                    correct_verb = self.verb_rules[next_word].get(word)
                    if correct_verb and correct_verb != next_word:
                        corrected_grammar[i + 1] = correct_verb[0] if isinstance(correct_verb, list) else correct_verb

        corrected_text = ' '.join(corrected_grammar)
        return corrected_text, mistakes  # Return both corrected text and mistakes