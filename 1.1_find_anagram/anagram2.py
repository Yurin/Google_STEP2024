#This program uses brute force to search the dictionary using the binary search algorithm.
#全ての準列を列挙して辞書と比べることでアナグラムを見つける。辞書と比べる時に二分探索を用いた

def binary_search(target, sorted_list):
    low = 0
    high = len(sorted_list) - 1
    while low <= high:
        mid = (low + high) // 2
        guess = sorted_list[mid]  # sorted_list[mid]はタプルではなく文字列
        if guess == target:
            return mid
        elif guess < target:
            low = mid + 1
        else:
            high = mid - 1
    return None

def generate_possible_word(random_word, r=None):  # generate_possible_word('a,b,c', r=2) -> ab,ac,ba,bc,ca,cb
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
#O(logm) m = len(dictionary)

#O(n! * logm)

def solution(random_word, dictionary):
    possible_words = list(generate_possible_word(random_word, len(random_word)))
    found_anagrams = []
    for word in possible_words:
        if binary_search(word, dictionary) is not None:
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
