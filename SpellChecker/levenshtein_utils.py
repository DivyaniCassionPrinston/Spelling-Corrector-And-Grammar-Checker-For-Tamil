# Levenshtein distance function
def lev(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    # Deletion
                    dp[i - 1][j] + 1,  
                     # Insertion
                    dp[i][j - 1] + 1, 
                    # Substitution
                    dp[i - 1][j - 1] + 1  
                )
    return dp[m][n]



def prefix_match(string1, string2):
    common_length = 0
    for i in range(min(len(string1), len(string2))):
        if string1[i] == string2[i]:
            common_length += 1
        else:
            break
    return common_length



def suffix_match(string1, string2):
    common_length = 0
    for i in range(1, min(len(string1), len(string2)) + 1):
        if string1[-i] == string2[-i]:
            common_length += 1
        else:
            break
    return common_length