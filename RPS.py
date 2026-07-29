def player(prev_play, opponent_history=[], sequences={}):
    # تنظیمات اولیه
    stride = 3
    threshold = 0.6  # آستانه تشخیص ربات
    
    # ذخیره تاریخچه حرکات حریف
    if prev_play != '':
        opponent_history.append(prev_play)
    
    # اگر داده کافی نیست، حرکت تصادفی برگردان
    if len(opponent_history) <= stride:
        return "R"
    
    # تشخیص ربات حریف بر اساس الگوی حرکات
    opponent_type = identify_opponent(opponent_history)
    
    # انتخاب استراتژی بر اساس نوع ربات
    if opponent_type == "quincy":
        return beat_quincy(opponent_history)
    elif opponent_type == "abbey":
        return beat_abbey(opponent_history)
    elif opponent_type == "kris":
        return beat_kris(opponent_history)
    elif opponent_type == "mrugesh":
        return beat_mrugesh(opponent_history)
    else:
        # استراتژی پیش‌بینی الگو برای ربات‌های ناشناخته
        return predict_pattern(prev_play, opponent_history, sequences, stride)

def identify_opponent(history):
    """تشخیص ربات حریف"""
    if len(history) < 5:
        return "unknown"
    
    # تست Quincy (الگوی R,P,S تکراری)
    is_quincy = True
    for i in range(len(history)):
        expected = ["R", "P", "S"][i % 3]
        if history[i] != expected:
            is_quincy = False
            break
    if is_quincy:
        return "quincy"
    
    # تست Kris (تکرار با تاخیر 4)
    if len(history) >= 8:
        is_kris = True
        for i in range(4, len(history)):
            if history[i] != history[i-4]:
                is_kris = False
                break
        if is_kris:
            return "kris"
    
    # تست Mrugesh (بیشترین تکرار)
    if len(history) >= 10:
        recent = history[-10:]
        most_common = max(set(recent), key=recent.count)
        # اگر یک حرکت بیش از 70% تکرار شده باشد
        if recent.count(most_common) / len(recent) > 0.7:
            return "mrugesh"
    
    # تست Abbey (استفاده از الگوهای پیچیده‌تر)
    if len(history) >= 15:
        # بررسی اینکه آیا الگوی خاصی وجود دارد
        patterns = {}
        for i in range(len(history)-3):
            pattern = "".join(history[i:i+3])
            patterns[pattern] = patterns.get(pattern, 0) + 1
        
        # اگر یک الگوی خاص زیاد تکرار شده باشد
        if max(patterns.values()) > 3:
            return "abbey"
    
    return "unknown"

def beat_quincy(history):
    """شکست Quincy با الگوی R,P,S"""
    next_index = len(history) % 3
    quincy_next = ["R", "P", "S"][next_index]
    return counter_move(quincy_next)

def beat_abbey(history):
    """شکست Abbey با تحلیل آماری"""
    if len(history) < 5:
        return random_choice()
    
    # Abbey معمولاً به حرکات قبلی واکنش نشان می‌دهد
    # ما از تکنیک مخلوط کردن استراتژی‌ها استفاده می‌کنیم
    
    # روش 1: بررسی الگوهای 2 حرکتی
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
            # پیدا کردن حرکت بعدی که بیشترین احتمال را دارد
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
    
    # روش 2: تحلیل 10 حرکت آخر
    recent = history[-10:]
    if len(set(recent)) == 1:
        # اگر همه یکسان هستند
        return counter_move(recent[0])
    
    # استفاده از ترکیب استراتژی‌ها
    return random_choice()

def beat_kris(history):
    """شکست Kris (تکرار با تاخیر)"""
    if len(history) < 4:
        return random_choice()
    
    # Kris حرکت i-4 را تکرار می‌کند
    kris_next = history[-4]
    return counter_move(kris_next)

def beat_mrugesh(history):
    """شکست Mrugesh با استراتژی معکوس"""
    if len(history) < 5:
        return random_choice()
    
    recent = history[-10:]
    
    # محاسبه فراوانی حرکات
    counts = {"R": 0, "P": 0, "S": 0}
    for move in recent:
        counts[move] += 1
    
    # پیدا کردن کمترین حرکت استفاده شده
    least_common = min(counts, key=counts.get)
    
    # Mrugesh بیشترین حرکت را انتخاب می‌کند، پس ما برعکس عمل می‌کنیم
    # گاهی Mrugesh استراتژی خود را عوض می‌کند، پس تنوع ایجاد می‌کنیم
    if len(history) > 20 and len(set(history[-15:])) == 1:
        # اگر Mrugesh یک حرکت را تکرار می‌کند
        return counter_move(history[-1])
    
    # استراتژی ترکیبی
    if random.random() < 0.3:  # 30% مواقع تصادفی برای ایجاد تنوع
        return random_choice()
    
    return counter_move(least_common)

def predict_pattern(prev_play, opponent_history, sequences, stride):
    """استراتژی اصلی پیش‌بینی الگو (کد اصلی شما)"""
    # به‌روزرسانی توالی‌ها
    if len(opponent_history) > stride + 1:
        opponent_history.pop(0)
    
    # افزایش توالی آخر
    seq = "".join(opponent_history)
    sequences[seq] = sequences.get(seq, 0) + 1
    
    # پیش‌بینی حرکت بعدی
    seq = "".join(opponent_history[-stride:])
    predict = max([seq + "R", seq + "P", seq + "S"],
                  key=lambda key: sequences.get(key, 0))[-1]
    
    # برگرداندن حرکت برنده
    return counter_move(predict)

def counter_move(move):
    """برگرداندن حرکت برنده"""
    if move == "R":
        return "P"
    elif move == "P":
        return "S"
    else:  # "S"
        return "R"

def random_choice():
    """انتخاب تصادفی با وزن‌های مساوی"""
    import random
    return random.choice(["R", "P", "S"])
