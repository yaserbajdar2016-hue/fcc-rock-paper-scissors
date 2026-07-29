import random

def player(prev_play, opponent_history=[], sequences={}):
    stride = 3
    
    if prev_play != '':
        opponent_history.append(prev_play)
    
    if len(opponent_history) <= stride:
        return "R"
    
    opponent_type = identify_opponent(opponent_history)
    
    if opponent_type == "quincy":
        return beat_quincy(opponent_history)
    elif opponent_type == "abbey":
        return beat_abbey(opponent_history)
    elif opponent_type == "kris":
        return beat_kris(opponent_history)
    elif opponent_type == "mrugesh":
        return beat_mrugesh(opponent_history)
    else:
        return predict_pattern(prev_play, opponent_history, sequences, stride)

def identify_opponent(history):
    if len(history) < 5:
        return "unknown"
    
    # تست Quincy
    is_quincy = True
    for i in range(len(history)):
        expected = ["R", "P", "S"][i % 3]
        if history[i] != expected:
            is_quincy = False
            break
    if is_quincy:
        return "quincy"
    
    # تست Kris
    if len(history) >= 8:
        is_kris = True
        for i in range(4, len(history)):
            if history[i] != history[i-4]:
                is_kris = False
                break
        if is_kris:
            return "kris"
    
    # تست Mrugesh
    if len(history) >= 10:
        recent = history[-10:]
        most_common = max(set(recent), key=recent.count)
        if recent.count(most_common) / len(recent) > 0.7:
            return "mrugesh"
    
    # تست Abbey
    if len(history) >= 15:
        patterns = {}
        for i in range(len(history)-3):
            pattern = "".join(history[i:i+3])
            patterns[pattern] = patterns.get(pattern, 0) + 1
        if max(patterns.values()) > 3:
            return "abbey"
    
    return "unknown"

def beat_quincy(history):
    next_index = len(history) % 3
    quincy_next = ["R", "P", "S"][next_index]
    return counter_move(quincy_next)

def beat_abbey(history):
    if len(history) < 5:
        return random_choice()
    
    if len(history) >= 4:
        patterns = {}
        for i in range(len(history)-2):
            pattern = "".join(history[i:i+2])
            next_move = history[i+2] if i+2 < len(history) else None
            if next_move:
                key = pattern + next_move
                patterns[key] = patterns.get(key, 0) + 1
        
        if patterns:
            last_two = "".join(history[-2:])
            possible_moves = ["R", "P", "S"]
            best_move = None
            best_count = -1
            for move in possible_moves:
                key = last_two + move
                count = patterns.get(key, 0)
                if count > best_count:
                    best_count = count
                    best_move = move
            if best_move:
                return counter_move(best_move)
    
    recent = history[-10:]
    if len(set(recent)) == 1:
        return counter_move(recent[0])
    
    return random_choice()

def beat_kris(history):
    if len(history) < 4:
        return random_choice()
    kris_next = history[-4]
    return counter_move(kris_next)

def beat_mrugesh(history):
    if len(history) < 5:
        return random_choice()
    
    recent = history[-10:]
    counts = {"R": 0, "P": 0, "S": 0}
    for move in recent:
        counts[move] += 1
    
    least_common = min(counts, key=counts.get)
    
    if len(history) > 20 and len(set(history[-15:])) == 1:
        return counter_move(history[-1])
    
    if random.random() < 0.3:
        return random_choice()
    
    return counter_move(least_common)

def predict_pattern(prev_play, opponent_history, sequences, stride):
    if len(opponent_history) > stride + 1:
        opponent_history.pop(0)
    
    seq = "".join(opponent_history)
    sequences[seq] = sequences.get(seq, 0) + 1
    
    seq = "".join(opponent_history[-stride:])
    predict = max([seq + "R", seq + "P", seq + "S"],
                  key=lambda key: sequences.get(key, 0))[-1]
    
    return counter_move(predict)

def counter_move(move):
    if move == "R":
        return "P"
    elif move == "P":
        return "S"
    else:
        return "R"

def random_choice():
    return random.choice(["R", "P", "S"])
