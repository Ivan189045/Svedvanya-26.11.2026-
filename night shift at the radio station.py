# -*- coding: utf-8 -*-
"""
НОЧНАЯ СМЕНА НА РАДИОСТАНЦИИ
Текстовая игра: ты — ночной диджей «Радио Вечер 101.3 FM».
Держись до 06:00. Следи за рейтингом и рассудком.
Запуск: python night_shift_radio.py
"""

import random
import sys

# ---------- Состояние игры ----------

class Game:
    def __init__(self):
        self.hour = 0          # 00:00
        self.minute = 0
        self.rating = 60       # рейтинг эфира 0-100
        self.sanity = 100      # рассудок 0-100
        self.coffee = 2        # стаканы кофе в запасе
        self.listeners = 850   # слушателей
        self.caffeine = 0      # накопленный кофеин
        self.logs = []         # что помнишь за ночь
        self.over = False
        self.ending = ""

    def clock(self):
        return f"{self.hour:02d}:{self.minute:02d}"

    def advance(self, minutes):
        self.minute += minutes
        while self.minute >= 60:
            self.minute -= 60
            self.hour += 1
        if self.hour >= 6:
            self.finish()

    def clamp(self):
        self.rating = max(0, min(100, self.rating))
        self.sanity = max(0, min(100, self.sanity))
        self.listeners = max(0, self.listeners)

    def remember(self, text):
        self.logs.append(f"[{self.clock()}] {text}")

    def finish(self):
        self.over = True
        if self.sanity <= 0:
            self.ending = "ПОЛУНОЧНЫЙ ЭФИР"
        elif self.rating <= 0 or self.listeners < 50:
            self.ending = "ПОСЛЕДНИЙ ВЫХОД В ЭФИР"
        else:
            if self.sanity >= 80 and self.rating >= 80:
                self.ending = "ЛЕГЕНДА НОЧНОГО ЭФИРА"
            elif self.sanity >= 60:
                self.ending = "ЧИСТАЯ СМЕНА"
            else:
                self.ending = "НА ГРАНИ"

# ---------- Песни ----------

TRACKS = [
    ("Синий туман", "Весёлые утята не прыгали под эту"),
    ("Baker Street", "Gerry Rafferty — для одиноких шофёров"),
    ("Moonlight Drive", "The Doors — что-то шевелится в тумане"),
    ("Ночь", "группа «Машина времени» — уместно"),
    ("Strange Currencies", "R.E.M. — и правда странно"),
    ("Незнакомка", "что-то местное, из архива"),
    ("Wicked Game", "Chris Isaak — тает лёд и нервы"),
    ("Трек без названия", "не помнишь, когда это добавили в плейлист"),
]

# ---------- Звонки слушателей ----------

CALLERS = [
    {
        "name": "Алексей, таксист",
        "text": "«Здарова, диджей! Поставь чего-нибудь бодрого, я до утра по МКАД гоняю».",
        "options": [
            ("Поддержать разговор", "+rating +listeners"),
            ("Сразу поставить музыку", "+rating"),
        ],
    },
    {
        "name": "Наталья сontte окна",
        "text": "«Доброй ночи... не спится. Расскажите, как прошёл ваш день?»",
        "options": [
            ("Рассказать про свой день", "+sanity +rating"),
            ("Спросить, не спится ли ей часто", "?"),
        ],
    },
    {
        "name": "???",
        "text": "Шум. Помехи. Потом тихий голос: «Мы вас слушаем с 1987 года. Не переключайте.»",
        "options": [
            ("Спросить, кто говорит", "-sanity"),
            ("Ничего не отвечать, положить трубку", "-rating +sanity"),
            ("Сказать в эфир: «Рад, что вы с нами»", "+rating -sanity"),
        ],
    },
    {
        "name": "Дед Петрович",
        "text": "«Молодёжь! А вот в наше время...» — дальше 4 минуты без пауз.",
        "options": [
            ("Терпеливо слушать", "+rating -sanity"),
            ("Аккуратно свернуть разговор", "+rating"),
            ("Дать ему «просто ещё минуточку»", "+listeners -sanity"),
        ],
    },
    {
        "name": "Голос, похожий на твой",
        "text": "В трубке твой собственный голос произносит фразу, которую ты ещё не говорил. Но обязательно скажешь.",
        "options": [
            ("Записать её на бумажке", "-sanity +rating"),
            ("Положить трубку и не оборачиваться", "-rating +sanity"),
        ],
    },
    {
        "name": "Даша, 11 лет",
        "text": "«Извините, а музыка ещё будет? Мой братик не может уснуть».",
        "options": [
            ("Спеть колыбельную в эфир", "+sanity +rating"),
            ("Поставить спокойный трек", "+rating"),
        ],
    },
    {
        "name": "Сержант Ковалёв",
        "text": "«Это радиоточка города. У нас в сводке... хм. Слушай, а у вас там всё нормально в аппаратной?»",
        "options": [
            ("«Всё тихо»", "+rating"),
            ("«Тихо. Слишком тихо»", "-rating +sanity"),
        ],
    },
]

# ---------- События ----------

def event_power(g):
    print("\n⚡ Свет мигнул. Аппаратная на секунду погрузилась в темноту.")
    if g.sanity < 50:
        print("В темноте ты различил силуэт в кресле напротив. Кресло пустое. Оно было пустое.")
        g.sanity -= 15
    else:
        print("Пересдали, работает. Ничего страшного.")
        g.sanity -= 5
    g.remember("мигнул свет")

def event_request(g):
    print("\n📻 В эфир пробился запрос без входящего звонка:")
    print("   «Передайте: она смотрит на вас через студийное стекло.»")
    choice = input("Поставить запрос в эфир? (y/n): ").strip().lower()
    if choice == "y":
        g.sanity -= 10
        g.rating += 8
        g.listeners += random.randint(50, 150)
        g.remember("выполнил странный запрос")
        print("Слушателям зашло. Тебе — нет.")
    else:
        g.sanity += 5
        print("Ты не стал. За стеклом ничего не изменилось. Ты не стал это проверять.")

def event_silence(g):
    print("\n🎧 Плейлист молчит. В наушниках — только твоё дыхание и гул антенны.")
    g.sanity -= 5
    print("Через минуту музыка возвращается сама. Ты не включал её.")
    g.remember("эфир молчал")

def event_phone(g):
    print("\n📞 Телефон в студии звонит. Звонит. И звонит. Ты уже снял трубку.")
    g.sanity -= 8
    g.remember("телефон не замолкал")

def random_event(g):
    events = [event_power, event_request, event_silence, event_phone]
    if random.random() < 0.45:
        random.choice(events)(g)

# ---------- Действия ----------

def play_track(g):
    title, note = random.choice(TRACKS)
    print(f"\n🎵 Ты ставишь: «{title}» — {note}.")
    delta = random.randint(-3, 10)
    g.rating += delta
    g.listeners += random.randint(-40, 90)
    g.sanity += 2
    g.advance(30)
    g.remember(f"поставил «{title}»")
    print(f"Реакция эфира: {delta:+d} к рейтингу.")

def take_call(g):
    caller = random.choice(CALLERS)
    print(f"\n☎️ НА ЛИНИИ: {caller['name']}")
    print(caller["text"])
    for i, (opt, _) in enumerate(caller["options"], 1):
        print(f"  {i}. {opt}")
    try:
        idx = int(input("Твой ответ: ")) - 1
        if not 0 <= idx < len(caller["options"]):
            raise ValueError
    except ValueError:
        idx = 0
        print("Ты растерялся и просто сказал: «Э-э... да.»")

    opt, eff = caller["options"][idx]
    effects = {
        "+rating": (0, 5, 0), "-rating": (0, -5, 0),
        "+sanity": (5, 0, 0), "-sanity": (-12, 0, 0),
        "+listeners": (0, 2, 120),
    }
    if eff == "?":
        if "не спится" in opt or "кто" in opt.lower():
            g.sanity -= 10
            g.rating += 3
            print("Разговор зашёл не туда. Ответ был страннее, чем ты хотел.")
        else:
            g.sanity += 8
            g.rating += 5
            print("Разговор получился тёплым. Она улыбнулась — ты услышал это.")
    else:
        for part in eff.split():
            ds, dr, dl = effects.get(part, (0, 0, 0))
            g.sanity += ds
            g.rating += dr
            g.listeners += dl
        print("Эфир прореагировал.")
    g.advance(30)
    g.remember(f"звонок от {caller['name']}")

def read_news(g):
    news = [
        "Мэр открыл новую набережную. Толпа благодарных горожан стояла слишком неподвижно.",
        "В городе открыли ночную кофейню. Владелец обещает «кофе как в 1998-м». Многие помнят, каков был кофе в 1998-м.",
        "Дорожная сводка: на объездной фура. Место аварии совпадает с тем, где фура уже стояла в марте.",
        "Погода: до утра будет туман. Радиофизики советуют вечером слушать радио не один.",
    ]
    print(f"\n📰 НОВОСТИ СВЕЖИМ ЧИСЛОМ: {random.choice(news)}")
    g.rating += random.randint(2, 7)
    g.sanity += random.randint(-2, 4)
    g.advance(20)
    g.remember("прочитал новости")

def drink_coffee(g):
    if g.coffee <= 0:
        print("\n☕ Кофе кончился. Автомат в коридоре глухо бормочет: «Не сейчас.»")
        return
    g.coffee -= 1
    g.caffeine += 1
    g.sanity += 12
    print(f"\n☕ Глоток горячего кофе. В машине остаётся {g.coffee} стакан(а). Нервы выравниваются.")
    if g.caffeine >= 4:
        print("Руки слегка подрагивают. Ты замечаешь, что произносишь тишину вслух.")
        g.sanity -= 5
    g.advance(10)
    g.remember("выпил кофе")

def speak_on_air(g):
    print("\n🎤 Ты выключаешь музыку и говоришь в эфир (напиши фразу):")
    text = input("> ").strip() or "С вами ночной эфир «Радио Вечер»."
    bonus = len(text) // 10
    g.rating += min(bonus, 8)
    g.listeners += min(len(text) // 5, 100)
    if "помоги" in text.lower() or "свет" in text.lower():
        g.sanity -= 4
    print("Вэфире повисла тишина. Потом — отклик. Всегда есть отклик.")
    g.advance(15)
    g.remember(f"сказал: «{text}»")

def check_frequencies(g):
    print("\n📡 Крутишь ручку настройки:")
    found = [
        "101.3 — ты сам. Пока.",
        "87.5 — молитва. На старославянском. Идёт полчаса, не прерываясь.",
        "108.0 — детский хор. Дети поют песню, которой ещё не написали.",
        "95.2 — твой собственный голос из вчерашнего эфира. Ты его не записывал.",
        "Шум. Чистый белый шум. Он звучит как аплодисменты.",
    ]
    pick = random.choice(found)
    print(f"   {pick}")
    g.sanity -= random.choice([0, 3, 5, 8])
    g.advance(10)
    g.remember(f"поймал частоту: {pick}")

def rest(g):
    print("\n🪑 Ты пять минут просто сидишь и смотришь на индикаторы.")
    g.sanity += 6
    g.rating -= 3
    g.advance(20)
    g.remember("молча сидел у пульта")

# ---------- Главное ----------

MENU = """
══════════════════════════════════════════
  ДЕЙСТВИЯ:
  1 — Поставить трек
  2 — Взять звонок слушателя
  3 — Прочитать новости
  4 — Выпить кофе
  5 — Сказать в эфир
  6 — Проверить частоты
  7 — Просто посидеть
  0 — Уйти со смены (плохая идея)
──────────────────────────────────────────
"""

def status(g):
    print(f"\n── {g.clock()} ─ РЕЙТИНГ: {g.rating} | НЕРВЫ: {g.sanity} | СЛУШАЮТ: {g.listeners} | КОФЕ: {g.coffee}")

def intro():
    print("=" * 46)
    print("  РАДИО ВЕЧЕР 101.3 FM — НОЧНАЯ СМЕНА")
    print("=" * 46)
    print("00:00. Студия пуста. За стеклом — тёмный город.")
    print("Ты диджей до шести утра. Держись до рассвета.\n")

def main():
    g = Game()
    intro()
    while not g.over:
        status(g)
        print(MENU)
        choice = input("Выбор: ").strip()
        actions = {
            "1": play_track, "2": take_call, "3": read_news,
            "4": drink_coffee, "5": speak_on_air, "6": check_frequencies,
            "7": rest,
        }
        if choice == "0":
            print("\nТы снимаешь наушники и уходишь. Эфир остаётся включённым.")
            print("Утром техник найдёт студию, но не найдёт тебя.")
            g.ending = "ДВЕРЬ ОСТАЛАСЬ ОТКРЫТОЙ"
            g.over = True
            break
        act = actions.get(choice)
        if act:
            act()
            if not g.over:
                random_event(g)
                g.clamp()
                if g.sanity <= 0:
                    g.finish()
        else:
            print("Такой кнопки на пульте нет.")
    print_final(g)

def print_final(g):
    print("\n" + "=" * 46)
    print(f"  06:00. СМЕНА ЗАКОНЧЕНА. ФИНАЛ: {g.ending}")
    print("=" * 46)
    if g.ending == "ЛЕГЕНДА НОЧНОГО ЭФИРА":
        print("Ты дожил до рассвета и не сломался. Слушатели в восторге.")
        print("Начальник утром скажет: «А ты ночью был в ударе». Он не знает и половины.")
    elif g.ending == "ЧИСТАЯ СМЕНА":
        print("Солнце поднимается над городом. Ты уходишь домой живым и с рейтингом.")
    elif g.ending == "НА ГРАНИ":
        print("Ты доходишь до дома и первую неделю спишь с включённым светом.")
    elif g.ending == "ПОСЛЕДНИЙ ВЫХОД В ЭФИР":
        print("Слушателей нет. Рекламодатели ушли. Тебя «просят освободить должность».")
        print("Говорят, на твоей частоте теперь кто-то другой.")
    elif g.ending == "ПОЛУНОЧНЫЙ ЭФИР":
        print("Твоё имя сняли с графика. Но каждую ночь на 101.3 кто-то ведёт передачу.")
        print("Голос — твой. Ты не выходишь в эфир уже три года.")
    else:
        print("Дверь осталась открытой. С этой ночью всё и началось.")
    print("\nТвоя запись за ночь:")
    for line in g.logs:
        print(" ", line)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nСвязь прервана. 101.3 FM — прощание никогда не бывает окончательным.")
        sys.exit(0)
