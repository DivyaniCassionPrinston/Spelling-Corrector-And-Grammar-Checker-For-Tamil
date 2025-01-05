from sklearn.metrics import precision_score, recall_score, f1_score

def evaluator(test_sentences, expected_corrections, corrected_sentence):
    TP = 0  
    FP = 0  
    FN = 0  
    TN = 0  
    total_words = 0

    for i, sentence in enumerate(test_sentences):
        expected_sentence = expected_corrections[i]

        corrected_words = corrected_sentence.split()
        expected_words = expected_sentence.split()
        test_words = sentence.split()

        for corrected_word, expected_word, test_word in zip(corrected_words, expected_words, test_words):
            total_words += 1
            if test_word == expected_word: 
                if test_word == corrected_word: 
                    TN += 1
                else: 
                    FP += 1
            elif test_word != expected_word: 
                if test_word == corrected_word: 
                    FN += 1
                else: 
                    TP += 1

    accuracy = (TP + TN) / (TP + FP + FN + TN)
    precision = TP / (TP + FP) if (TP + FP) != 0 else 0
    recall = TP / (TP + FN) if (TP + FN) != 0 else 0
    specificity = TN / (TN + FP) if (TN + FP) != 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"Specificity: {specificity}")
    print(f"F1-Score: {f1_score}")