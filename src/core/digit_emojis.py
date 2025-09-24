DIGIT_EMOJI = {
    "0": "0️⃣",
    "1": "1️⃣",
    "2": "2️⃣",
    "3": "3️⃣",
    "4": "4️⃣",
    "5": "5️⃣",
    "6": "6️⃣",
    "7": "7️⃣",
    "8": "8️⃣",
    "9": "9️⃣",
    "-": "➖",
}


def number_to_digit_emojis(n: int) -> str:
    s = str(n)
    return "".join(DIGIT_EMOJI.get(ch, ch) for ch in s)
