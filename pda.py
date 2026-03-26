import os
import sys
import io

def is_balanced(input_string):
    # Initial PDA setup 
    state = "q0"
    stack = ['Z'] 
    
    print(f"Processing {input_string}")
     
    # Starting ID 
    # Format: (state, remaining_input, stack_as_string)
    print(f"ID: ({state}, {input_string}, {''.join(stack[::-1])})")


    opening_brackets = {'(': ')', '[': ']', '{': '}', '<': '>'}
    
    for i, char in enumerate(input_string):
        pos = i + 1
        
        if state == "q0":
            if char == '!':
                state = "q1"
                stack.insert(0, '!')
            else:
                print(f"Invalid string. Failed at position {pos}.")
                print(f"Remaining unprocessed input string: {input_string[i:]}")
                return False

        elif state == "q1":
            if char == 'x':
                pass 
            elif char in opening_brackets:
                stack.insert(0, char)
            elif char in opening_brackets.values():
                top = stack[0]
                if top in opening_brackets and opening_brackets[top] == char:
                    stack.pop(0)
                else:
                    print(f"Invalid string. Failed at position {pos}.")
                    print(f"Remaining unprocessed input string: {input_string[i:]}")
                    return False
            elif char == '!':
                if stack[0] == '!':
                    stack.pop(0)
                    state = "q2"
                else:
                    print(f"Invalid string. Failed at position {pos}.")
                    return False
            else:
                print(f"Invalid string. Failed at position {pos}.")
                print(f"Remaining unprocessed input string: {input_string[i:]}")
                return False
        
        elif state == "q2":
             print(f"Invalid string. Failed at position {pos}.")
             return False

        remaining = input_string[pos:] if pos < len(input_string) else "E"
        stack_str = ''.join(stack)
        print(f"ID: ({state}, {remaining}, {stack_str})")

    if state == "q2" and len(stack) == 1 and stack[0] == 'Z':
        print(f"{state} is a final state.")
        print(f"{input_string} is valid and has balanced brackets.")
        return True
    else:
        print(f"Invalid string. {state} is not a final state.")
        return False
def _find_matching(s, open_idx):
    close_map = {'(': ')', '[': ']', '{': '}', '<': '>'}
    target = close_map[s[open_idx]]
    depth = 0
    for i in range(open_idx, len(s)):
        if s[i] == s[open_idx]:
            depth += 1
        elif s[i] == target:
            depth -= 1
            if depth == 0:
                return i   
def _eval(s):
    count = 0
    i = 0
    while i < len(s):
        if s[i] == 'x':
            count += 1
            i += 1
        elif s[i] in '([{<':
            j = _find_matching(s, i)
            inside = s[i+1:j]
            inner_count = _eval(inside)

            if s[i] == '<':
                count += 2 * inner_count        # <S> → SS
            elif s[i] == '{':
                count += inner_count + 1        # {S} → Sxy
            elif s[i] == '[':
                count += 0                      # [S] → εy
            elif s[i] == '(':
                if inner_count == 0:
                    count += 0                  # (ε) → εy
                else:
                    count += inner_count - 1    # (xS) → S

            i = j + 1
        else:
            i += 1
    return count

def evaluate(s):
    inner = s[1:-1]   # strip outer ! marks
    return _eval(inner)

def main1():
    if os.path.exists("input.txt"):
        with open("input.txt", "r") as f:
            for line in f:
                is_balanced(line.strip())
                print()

def main2():
    if os.path.exists("input.txt"):
        with open("input.txt", "r") as f:
            lines = [line.strip() for line in f]

        for line in lines:
            # run is_balanced() silently, capture and discard its prints
            buf = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = buf
            valid = is_balanced(line)
            sys.stdout = old_stdout

            if valid:
                result = evaluate(line)
                print(f"{line} - Resulting number of x's: {result}")
            else:
                print(f"{line} - Invalid string.")

if __name__ == "__main__":
    main1()
    main2()
