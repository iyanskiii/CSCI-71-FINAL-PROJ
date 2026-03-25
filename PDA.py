import os

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
        
        # PDA start
        # State q0: Look for starting '!' 

        if state == "q0":
            if char == '!':
                state = "q1"
                stack.insert(0, '!')
            else:
                print(f"Invalid string. Failed at position {pos}.")
                print(f"Remaining unprocessed input string: {input_string[i:]}")
                return False

        # State q1: Process brackets and x's 
        # PDA Flow:
        # If x is read does nothing 
        # If any opening braket is read, push the bracket 
        # if any closing bracket is read, check the top of the stack if it matches then pop
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
                # Check for the matching "!" at the end of the input
                # if successful go to final state (q2)
                if stack[0] == '!':
                    stack.pop(0)
                    state = "q2"
                else:
                    print(f"Invalid string. Failed at position {pos}.")
                    return False
            else:
                # Any other character is invalid 
                print(f"Invalid string. Failed at position {pos}.")
                print(f"Remaining unprocessed input string: {input_string[i:]}")
                return False
        
        # After final '!', no more characters should exist 
        elif state == "q2":
             print(f"Invalid string. Failed at position {pos}.")
             return False

        # Print ID after processing the character 
        remaining = input_string[pos:] if pos < len(input_string) else "E"
        stack_str = ''.join(stack) # Bottom symbol Z at the end 
        print(f"ID: ({state}, {remaining}, {stack_str})")

    if state == "q2" and len(stack) == 1 and stack[0] == 'Z':
        print(f"{state} is a final state.")
        print(f"{input_string} is valid and has balanced brackets.")
        return True
    else:
        print(f"Invalid string. {state} is not a final state.")
        return False
    

def main1():
    if os.path.exists("input.txt"):
        with open("input.txt", "r") as f:
            for line in f:
                is_balanced(line.strip())
                print() 