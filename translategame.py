import random

turkish = ["Elma", "Armut", "Yeşil", "Kırmızı", "Araba", "Uçak", "Fare",
           "Kedi", "Sırt Çantası", "Kemer"]

english = ["Apple", "Pear", "Green", "Red", "Car", "Plane", "Mouse", "Cat",
           "Backpack", "Belt"]

answer_key = list(zip(turkish, english))


def translateGame(translator):
    while True:
        question = random.choice(turkish)
        answer = input(f"{question} kelimesinin İngilizcesi: ")

        if (question, answer.title()) in answer_key:
            print("Tebrikler!!!")
            print("-"*30)
        else:
            index = turkish.index(question)
            print("Maalesef yanlış yaptınız, doğrusu: ", answer_key[index][1])
            print("-"*30)


translateGame(answer_key)