##This program is brute force
#全ての準列を列挙して辞書と比べることでアナグラムを見つける
#generate all possible words and compare input word to dictionary


#"generate_possible_word" is same as "itertools.permutations(iterable, r=None)"

# from itertools import permutations
# def generate_possible_word(random_word, r=None):
#     if r is None:
#         r = len(random_word)
#     return [''.join(p) for p in permutations(random_word, r)]

def generate_possible_word(random_word, r=None):#generate_possible_word('a,b,c', r=2) -> ab,ac,ba,bc,ca,cb
    pool = tuple(random_word)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n-r, -1))
    yield ''.join(pool[i] for i in indices[:r])

    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield ''.join(pool[i] for i in indices[:r])
                break
        else:
            return

#O(n!) n = len(randam_word)
#O(m) m = len(dictionary)

#O(n! * m)
def solution(random_word, dictionary):
    possible_words = list(generate_possible_word(random_word, len(random_word)))
    found_anagrams = []
    for word in possible_words:
        if word in dictionary:
            found_anagrams.append(word)
    return found_anagrams if found_anagrams else "No anagram found"

input_word = input("Enter a word: ")
with open("words.txt", "r") as file:
    words = file.read().splitlines()
anagrams = solution(input_word, words)
if isinstance(anagrams, list):
    print("Anagrams found:", ", ".join(anagrams))
else:
    print(anagrams)
