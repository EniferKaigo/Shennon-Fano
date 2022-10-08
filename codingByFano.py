from math import log2
from collections import Counter


class Symbol:
    def __init__(self, name: str, probability: float):
        self.name = name
        self.probability = probability
        self.code = ""

    def updateCode(self, digit: int):
        self.code += str(digit)

    def __str__(self):
        return f"Символ: {self.name} | Вероятность: {self.probability} | Код: {self.code}"


def createCodesByFano(symbols: list[Symbol]) -> list[Symbol]:
    def f(x: float):
        return abs(2 * x - sum(symbol.probability for symbol in symbols))

    if len(symbols) == 1:
        return symbols

    if len(symbols) == 2:
        sortedList = sorted(symbols, key=lambda x: x.probability)
        for i in range(len(symbols)):
            sortedList[i].updateCode(i)
        return sortedList

    sortedList = sorted(symbols, key=lambda x: x.probability, reverse=True)
    s = 0
    idx = 0

    while True:
        if idx == len(sortedList):
            break

        curr = sortedList[idx].probability
        if f(s + curr) < f(s):
            s += curr
        else:
            break

        idx += 1

    firstPart = sortedList[:idx]
    lastPart = sortedList[idx:]
    for s in firstPart:
        s.updateCode(1)

    for s in lastPart:
        s.updateCode(0)

    result = createCodesByFano(firstPart) + createCodesByFano(lastPart)
    return sorted(result, key=lambda x: x.probability)


def calculateProbabilities(text: str) -> list[Symbol]:
    extraSymbols = ".,!?:;*()-—–"
    countSigns = 3

    for c in extraSymbols:
        text = text.replace(c, "")

    text = text.replace("ё", "е").replace("ъ", "ь").replace(" ", "⎵").upper()
    count = Counter(text)
    result = []

    for entry in count.items():
        probability = round(entry[1] / len(text), countSigns)
        symbol = Symbol(name=entry[0], probability=probability)
        result.append(symbol)

    return result



def inputText() -> list[Symbol]:
    print("Введите текст")
    text = input()
    return calculateProbabilities(text)



def inputSymbols() -> list[Symbol]:
    n = int(input("Введите количество элементов -> "))
    symbols = []

    for _ in range(n):
        name = input("Символ: ")
        probability = float(input("Вероятность: "))
        symbols.append(Symbol(name, probability))
        print()

    return symbols



print("Выберите режим и введите его номер ниже:")
print("1. Ввод символов с вероятностями")
print("2. Ввод текста целиком")
mode = int(input())

if mode == 2:
    symbols = inputText()
else:
    symbols = inputSymbols()

result = createCodesByFano(symbols)
average = round(sum(len(symbol.code) * symbol.probability for symbol in result), 3)
entropy = round(sum(-symbol.probability * log2(symbol.probability) for symbol in result), 3)

print(f"Средняя длина кода: {average}")
print(f"Энтропия: {entropy}")
for s in result:
    print(s)
