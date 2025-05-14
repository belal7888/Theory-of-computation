# Naame: "Belal Abdullah Ragab";
# Sec : 2;
# ID: 4462;

def is_palindrome_odd_pda(string: str) -> bool:
    if len(string) % 2 == 0:
        return False

    stack = []
    n = len(string)
    mid = n // 2  

    for i in range(mid):
        stack.append(string[i])

    i = mid + 1

    while i < n:
        top = stack.pop()
        if string[i] != top:
            return False
        i += 1

    return not stack

print(is_palindrome_odd_pda("aba"))      
print(is_palindrome_odd_pda("abcba"))   
print(is_palindrome_odd_pda("abba"))    
print(is_palindrome_odd_pda("abca"))     

