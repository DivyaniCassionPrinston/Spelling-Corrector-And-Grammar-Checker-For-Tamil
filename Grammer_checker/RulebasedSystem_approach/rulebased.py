
import nltk
nltk.download('punkt_tab')

import json
import nltk
from nltk.translate.bleu_score import sentence_bleu
from nltk.tokenize import sent_tokenize  # To split paragraph into sentences



def load_rules_from_file(file_path):
    """Loads rules from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def tokenize_sentence(sentence):
    """Splits the sentence into words."""
    return sentence.split()

def check_subject_verb_agreement(sentence, subject_verb_rules):
    """
    Rule: Check if the subject agrees with the verb.
    """
    tokens = tokenize_sentence(sentence)
    if len(tokens) > 1 and tokens[0] in subject_verb_rules:
        expected_verb = subject_verb_rules[tokens[0]]
        if tokens[1] != expected_verb:
            corrected_sentence = sentence.replace(tokens[1], expected_verb)
            return corrected_sentence
    return sentence

def check_tense_agreement(sentence, tense_rules):
    """
    Rule: Check if the verb agrees with the tense.
    """
    tokens = tokenize_sentence(sentence)
    if len(tokens) > 1 and tokens[0] in tense_rules:
        subject = tokens[0]
        verb = tokens[1]

        # Check if verb matches any of the tenses for the subject
        for tense, correct_verb in tense_rules[subject].items():
            if verb == correct_verb:
                return sentence  # Already correct
        
        # Default to past tense if no match
        expected_verb = tense_rules[subject].get("past", verb)  # Fallback to the current verb if no past tense defined
        corrected_sentence = sentence.replace(verb, expected_verb)
        return corrected_sentence
    return sentence

def grammar_corrector(sentence, subject_verb_rules, tense_rules):
    """Check for both subject-verb agreement and tense-based agreement errors."""
    corrected_sentence = check_subject_verb_agreement(sentence, subject_verb_rules)
    corrected_sentence = check_tense_agreement(corrected_sentence, tense_rules)
    return corrected_sentence

def calculate_char_bleu_score(predicted_sentence, reference_sentence):
    """
    Calculate BLEU score at the character level.
    Tokenizes sentences into characters instead of words.
    """
    reference = [list(reference_sentence)]  # Reference as list of characters
    predicted = list(predicted_sentence)    # Predicted as list of characters
    return sentence_bleu(reference, predicted)

def evaluate_paragraph(paragraph, reference_paragraph, subject_verb_rules, tense_rules):
    """
    Evaluate each sentence in the paragraph, calculate character-level BLEU, and compute average BLEU.
    """
    test_sentences = sent_tokenize(paragraph)  # Split paragraph into sentences
    reference_sentences = sent_tokenize(reference_paragraph)  # Reference paragraph into sentences
    
    total_bleu_score = 0.0
    scores = []
    
    for i, test_sentence in enumerate(test_sentences):
        predicted_paragraph = grammar_corrector(test_sentence, subject_verb_rules, tense_rules)
        reference_sentence = reference_sentences[i]
        
        bleu_score = calculate_char_bleu_score(predicted_paragraph, reference_sentence)
        scores.append(bleu_score)
        total_bleu_score += bleu_score
        
        print(f"Test para: {test_paragraph}")
        print("  ")
        print(f"Predicted: {predicted_paragraph}")
        print("  ")
        print(f"Reference: {reference_paragraph}")
        print("  ")
        print(f"Character-Level BLEU Score: {bleu_score:.4f}\n")
    
    average_bleu_score = total_bleu_score / len(test_paragraph)
    print(f"Average Character-Level BLEU Score: {average_bleu_score:.4f}")
    return scores, average_bleu_score

# Load the rules from JSON files
subject_verb_rules = load_rules_from_file("C:/Users/SARITHA/Desktop/Grammer_check/Spelling-Corrector-And-Grammar-Checker-For-Tamil/Grammer_checker/RulebasedSystem_approach/subject_verb_rules.json")
tense_rules = load_rules_from_file("C:/Users/SARITHA/Desktop/Grammer_check/Spelling-Corrector-And-Grammar-Checker-For-Tamil/Grammer_checker/RulebasedSystem_approach/tense_rules.json")

# Test Paragraph and Reference Paragraph
test_paragraph = """
அவன் பள்ளிக்கு போகின்றன, ஆனால் அவள் இன்னும் அவளது பையை 
தேடிக் கொண்டு இருக்கின்றார்.அவன் உடனே அந்த விஷயத்தை முடித்துவிடும் 
என்று நாங்கள் நம்பினோம், ஆனால் அவளது வேலை இன்னும் முடியவில்லை. 
அவன் நிமிடத்திற்கு பிறகு வருவார், ஆனால் அவள் இன்னும் அவளது படிப்பை 
முடிக்காமல் இருக்கின்றன
"""

reference_paragraph = """
அவன் பள்ளிக்கு போகின்றான், ஆனால் அவள் இன்னும் அவளது பையை தேடிக் கொண்டு 
இருக்கின்றாள். அவன் உடனே அந்த விஷயத்தை முடித்துவிடுவான் என்று நாங்கள் நம்பினோம், 
ஆனால் அவளது வேலை இன்னும் முடியவில்லை. அவன் நிமிடத்திற்கு பிறகு வருவான், ஆனால் 
அவள் இன்னும் அவளது படிப்பை முடிக்காமல் இருக்கின்றாள்.
"""

# Evaluate the paragraph
evaluate_paragraph(test_paragraph, reference_paragraph, subject_verb_rules, tense_rules)
