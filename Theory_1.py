# Naame: "Belal Abdullah Ragab";
# Sec : 2;
# ID: 4462;


from typing import Set, Dict, List, Tuple

class State:
    def __init__(self):
        self.transitions = {} 
        self.epsilon = []   

class NFA:
    def __init__(self, start: State, accept: State):
        self.start = start
        self.accept = accept

def symbol_nfa(symbol: str) -> NFA:
    start = State()
    accept = State()
    start.transitions[symbol] = [accept]
    return NFA(start, accept)

def concat_nfa(nfa1: NFA, nfa2: NFA) -> NFA:
    nfa1.accept.epsilon.append(nfa2.start)
    return NFA(nfa1.start, nfa2.accept)

def union_nfa(nfa1: NFA, nfa2: NFA) -> NFA:
    start = State()
    accept = State()
    start.epsilon += [nfa1.start, nfa2.start]
    nfa1.accept.epsilon.append(accept)
    nfa2.accept.epsilon.append(accept)
    return NFA(start, accept)

def star_nfa(nfa: NFA) -> NFA:
    start = State()
    accept = State()
    start.epsilon += [nfa.start, accept]
    nfa.accept.epsilon += [nfa.start, accept]
    return NFA(start, accept)

def regex_to_nfa(regex: str) -> NFA:
    stack = []
    for char in regex:
        if char == '*':
            nfa = stack.pop()
            stack.append(star_nfa(nfa))
        elif char == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(concat_nfa(nfa1, nfa2))
        elif char == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(union_nfa(nfa1, nfa2))
        else:
            stack.append(symbol_nfa(char))
    return stack[0]

def epsilon_closure(states: Set[State]) -> Set[State]:
    stack = list(states)
    closure = set(states)
    while stack:
        state = stack.pop()
        for next_state in state.epsilon:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure

def move(states: Set[State], symbol: str) -> Set[State]:
    result = set()
    for state in states:
        if symbol in state.transitions:
            result.update(state.transitions[symbol])
    return result

class DFA:
    def __init__(self, start_state: int, accept_states: Set[int], transitions: Dict[Tuple[int, str], int]):
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

    def accepts(self, s: str) -> bool:
        state = self.start_state
        for char in s:
            if (state, char) in self.transitions:
                state = self.transitions[(state, char)]
            else:
                return False
        return state in self.accept_states

def nfa_to_dfa(nfa: NFA) -> DFA:
    state_map = {}
    dfa_transitions = {}
    dfa_accept_states = set()

    start_set = frozenset(epsilon_closure({nfa.start}))
    state_map[start_set] = 0
    unmarked = [start_set]
    state_count = 1

    while unmarked:
        current = unmarked.pop()
        current_id = state_map[current]
        for symbol in ['a', 'b']:  
            target = epsilon_closure(move(current, symbol))
            if not target:
                continue
            target_frozen = frozenset(target)
            if target_frozen not in state_map:
                state_map[target_frozen] = state_count
                unmarked.append(target_frozen)
                state_count += 1
            dfa_transitions[(current_id, symbol)] = state_map[target_frozen]

    for state_set, state_id in state_map.items():
        if nfa.accept in state_set:
            dfa_accept_states.add(state_id)

    return DFA(0, dfa_accept_states, dfa_transitions)

def regex_to_dfa(regex: str) -> DFA:
    postfix = infix_to_postfix(regex)
    nfa = regex_to_nfa(postfix)
    return nfa_to_dfa(nfa)

def infix_to_postfix(regex: str) -> str:
    output = []
    stack = []
    precedence = {'*': 3, '.': 2, '|': 1}
    def add_concat(regex):
        result = []
        for i in range(len(regex)):
            result.append(regex[i])
            if i + 1 < len(regex):
                if regex[i] not in '(|' and regex[i+1] not in '|*)':
                    result.append('.')
        return ''.join(result)
    regex = add_concat(regex)
    for char in regex:
        if char.isalnum():
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and precedence[stack[-1]] >= precedence[char]:
                output.append(stack.pop())
            stack.append(char)
    while stack:
        output.append(stack.pop())
    return ''.join(output)

assert regex_to_dfa("(a|b)*abb").accepts("aabb") == True
print("DFA Success")
assert regex_to_dfa("(a|b)*abb").accepts("ababa") == False
print("DFA Fault")
