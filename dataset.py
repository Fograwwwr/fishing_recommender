"""
Создание датасета
Тема ВКР: Разработка интеллектуального помощника по подбору товаров
Автор: Гребцов Никита Юрьевич
"""

import pandas as pd
from pathlib import Path

def dataset():
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    quality_products = [
    {"name": "Спиннинг Shimano Catana DX 240ML 5-20г", "description": "Лёгкий и чувствительный спиннинг для микроджига и ловли окуня. Быстрый строй.", "price": 6490, "category": "Спиннинги", "test_min": 5, "test_max": 20},
    {"name": "Спиннинг Lucky John Progress Jig 24 10-30г", "description": "Универсальный спиннинг для береговой ловли щуки и судака.", "price": 4390, "category": "Спиннинги", "test_min": 10, "test_max": 30},
    {"name": "Спиннинг Maximus High Energy-X 21L 3-15г", "description": "Лайт спиннинг для мелких приманок и осторожного окуня.", "price": 3790, "category": "Спиннинги", "test_min": 3, "test_max": 15},
    {"name": "Спиннинг Волжанка Метеор 270 7-28г", "description": "Надёжный бюджетный спиннинг российского производства.", "price": 2990, "category": "Спиннинги", "test_min": 7, "test_max": 28},
    {"name": "Спиннинг Shimano Exage 270 8-28г", "description": "Качественный спиннинг среднего класса.", "price": 7990, "category": "Спиннинги", "test_min": 8, "test_max": 28},
    {"name": "Спиннинг Daiwa Ninja Spin 240 10-30г", "description": "Хороший спиннинг по доступной цене.", "price": 5890, "category": "Спиннинги", "test_min": 10, "test_max": 30},

    {"name": "Катушка Shimano Stradic FL C3000", "description": "Одна из лучших катушек в среднем ценовом сегменте с плавным ходом.", "price": 12990, "category": "Катушки"},
    {"name": "Катушка Daiwa Ninja 2500A", "description": "Популярная катушка для лёгкого и среднего спиннинга.", "price": 5590, "category": "Катушки"},
    {"name": "Катушка Ryobi Exia 3000", "description": "Надёжная бюджетная катушка с хорошей укладкой лески.", "price": 3490, "category": "Катушки"},
    {"name": "Катушка Okuma Ceymar C-30", "description": "Компактная и мощная катушка для ультралайтовой ловли.", "price": 4690, "category": "Катушки"},
    {"name": "Катушка Shimano Twin Power 3000", "description": "Флагманская катушка премиум-класса.", "price": 18900, "category": "Катушки"},

    {"name": "Фидер Salmo Sniper Feeder 360 120г", "description": "Мощный фидер для дальнего заброса на реке.", "price": 5890, "category": "Фидеры", "test_min": 0, "test_max": 120},
    {"name": "Фидер Волжанка Оптима 390 150г", "description": "Классический фидер для любительской ловли.", "price": 5190, "category": "Фидеры", "test_min": 0, "test_max": 150},

    {"name": "Воблер Rapala X-Rap 100", "description": "Один из самых популярных воблеров для ловли щуки и судака.", "price": 1350, "category": "Воблеры"},
    {"name": "Воблер Yo-Zuri L-Minnow 66", "description": "Компактный воблер с агрессивной игрой.", "price": 950, "category": "Воблеры"},
    {"name": "Воблер Salmo Hornet 5см", "description": "Недорогой, но очень уловистый воблер.", "price": 690, "category": "Воблеры"},

    {"name": "Силикон Keitech Swing Impact 3.8\" (10 шт)", "description": "Очень уловистый виброхвост для щуки и крупного окуня.", "price": 1050, "category": "Приманки"},
    {"name": "Силикон Mann's Predator 4\" (8 шт)", "description": "Классическая силиконовая приманка.", "price": 780, "category": "Приманки"},
    {"name": "Блесна Mepps Aglia №3 золотая", "description": "Легендарная вращающаяся блесна.", "price": 480, "category": "Блесны"},
    {"name": "Блесна Blue Fox Vibrax №4", "description": "Качественная блесна с сильной вибрацией.", "price": 650, "category": "Блесны"},

    {"name": "Зимний костюм Norfin Discovery", "description": "Тёплый мембранный костюм для зимней рыбалки.", "price": 16200, "category": "Одежда"},
    {"name": "Демисезонный костюм Azura Pro", "description": "Универсальный костюм для весны и осени.", "price": 9200, "category": "Одежда"},
    {"name": "Подсак телескопический 200см треугольный", "description": "Удобный подсак для вываживания крупной рыбы.", "price": 2650, "category": "Аксессуары"},
    {"name": "Рыболовный ящик Plano 1364", "description": "Прочный ящик с множеством отсеков.", "price": 4150, "category": "Аксессуары"},

    {"name": "Спиннинг Abu Garcia Vendetta VRC702M 7-28г", "description": "Надёжный средне-быстрый спиннинг с качественной фурнитурой.", "price": 7590, "category": "Спиннинги", "test_min": 7, "test_max": 28},
    {"name": "Спиннинг Black Hole NS Matrix 240 5-21г", "description": "Лёгкий и сбалансированный спиннинг для джига и воблеров.", "price": 5690, "category": "Спиннинги", "test_min": 5, "test_max": 21},
    {"name": "Спиннинг Zemex Spider Pro 240 10-32г", "description": "Универсальный спиннинг с большим тестом для трофейной рыбы.", "price": 4890, "category": "Спиннинги", "test_min": 10, "test_max": 32},
    {"name": "Спиннинг Favorite Blue Bird 270 8-28г", "description": "Хороший бюджетный спиннинг для начинающих и опытных рыбаков.", "price": 3490, "category": "Спиннинги", "test_min": 8, "test_max": 28},
    {"name": "Спиннинг Major Craft N-One 180 0.5-5г", "description": "Ультралайтовый спиннинг для ловли на микроприманки.", "price": 6790, "category": "Спиннинги", "test_min": 0.5, "test_max": 5},
    {"name": "Спиннинг Stinger Ultralight 2.13м 1-7г", "description": "Ультралайт для окуня и форели с мягкой вершинкой.", "price": 2990, "category": "Спиннинги", "test_min": 1, "test_max": 7},
    {"name": "Спиннинг Maximus Black Widow 23L 4-16г", "description": "Яркий и звонкий спиннинг для активного твичинга.", "price": 4190, "category": "Спиннинги", "test_min": 4, "test_max": 16},
    {"name": "Спиннинг Kosadaka Menace 240 15-40г", "description": "Мощный спиннинг для больших приманок и крупной щуки.", "price": 3390, "category": "Спиннинги", "test_min": 15, "test_max": 40},
    {"name": "Спиннинг Lucky John Basara 27 10-35г", "description": "Спиннинг быстрого строя для джиговой ловли судака.", "price": 4690, "category": "Спиннинги", "test_min": 10, "test_max": 35},

    {"name": "Катушка Daiwa Legalis LT 2500D", "description": "Лёгкая и надёжная катушка с технологией Air Rotor.", "price": 7590, "category": "Катушки"},
    {"name": "Катушка Shimano Nasci FB 2500", "description": "Выносливая катушка с холоднокованым ротором.", "price": 8790, "category": "Катушки"},
    {"name": "Катушка Abu Garcia Revo X 3000", "description": "Мощная и плавная катушка для серьёзных нагрузок.", "price": 9990, "category": "Катушки"},
    {"name": "Катушка Ryobi Virago 1000", "description": "Компактная катушка для ультралайта с тонкой настройкой фрикциона.", "price": 3790, "category": "Катушки"},
    {"name": "Катушка Okuma Helios SX 30", "description": "Катушка с дисковым тормозом и облегчённым корпусом.", "price": 5490, "category": "Катушки"},
    {"name": "Катушка Favorite X1 2000", "description": "Бюджетная модель с хорошей тягой для лёгкого спиннинга.", "price": 2890, "category": "Катушки"},
    {"name": "Катушка Tsurinoya Spirit Fox 2500", "description": "Популярная китайская катушка с отличным соотношением цена/качество.", "price": 4590, "category": "Катушки"},
    {"name": "Катушка Spro Zalt M 2500", "description": "Универсальная катушка с металлическим корпусом.", "price": 6890, "category": "Катушки"},
    {"name": "Катушка Stinger Power 3000", "description": "Бюджетная катушка с хорошей укладкой лески.", "price": 2590, "category": "Катушки"},

    {"name": "Фидер Daiwa Whisker 330 100г", "description": "Лёгкий и точный фидер для стоячей воды.", "price": 8490, "category": "Фидеры", "test_min": 0, "test_max": 100},
    {"name": "Фидер Shimano Beastmaster Feeder 360 120г", "description": "Премиальный фидер с высокой чувствительностью.", "price": 13490, "category": "Фидеры", "test_min": 0, "test_max": 120},
    {"name": "Фидер Mikado Sensei Feeder 390 150г", "description": "Надёжный фидер для реки и озера с быстрым строем.", "price": 6190, "category": "Фидеры", "test_min": 0, "test_max": 150},
    {"name": "Фидер Browning Black Viper 360 140г", "description": "Универсальный фидер с запасом мощности.", "price": 7790, "category": "Фидеры", "test_min": 0, "test_max": 140},
    {"name": "Фидер Salmo Sniper Feeder 390 180г", "description": "Мощный фидер для дальнего заброса тяжёлых кормушек.", "price": 6290, "category": "Фидеры", "test_min": 0, "test_max": 180},

    {"name": "Воблер Kosadaka Ion 65S", "description": "Уловистый составной воблер для твичинга судака.", "price": 750, "category": "Воблеры"},
    {"name": "Воблер ZipBaits Orbit 80 SSR", "description": "Дальнобойный воблер с реалистичной игрой.", "price": 1450, "category": "Воблеры"},
    {"name": "Воблер Strike Pro Midge Vibe 5.5см", "description": "Маленькая вибрирующая приманка для окуня.", "price": 520, "category": "Воблеры"},
    {"name": "Воблер Jackall Chubby 38F", "description": "Крошечный плавающий воблер для форели и окуня.", "price": 1100, "category": "Воблеры"},
    {"name": "Воблер Megabass Vision Oneten", "description": "Культовый японский воблер с уникальной игрой.", "price": 1850, "category": "Воблеры"},
    {"name": "Воблер Googan Squad Rattlin' Ned 3.5см", "description": "Шумящий воблер для ловли в траве.", "price": 820, "category": "Воблеры"},
    {"name": "Воблер Daiwa Dr. Minnow 50SP", "description": "Суспендер с реалистичной формой малька.", "price": 1280, "category": "Воблеры"},

    {"name": "Виброхвост Relax Twister 4\" (10 шт)", "description": "Классический твистер для щуки и окуня.", "price": 550, "category": "Приманки"},
    {"name": "Твистер Mann's Samba 3\" (8 шт)", "description": "Универсальный твистер с яркой игрой.", "price": 680, "category": "Приманки"},
    {"name": "Силиконовый рак Kosadaka Diesel 3\" (6 шт)", "description": "Реалистичный рак для джига, любимое лакомство судака.", "price": 520, "category": "Приманки"},
    {"name": "Силикон Berkley PowerBait Rib Shad 4\" (5 шт)", "description": "Поглощающий запах виброхвост с ребристой поверхностью.", "price": 890, "category": "Приманки"},
    {"name": "Виброхвост Keitech Easy Shiner 4\" (8 шт)", "description": "Мягкий и очень подвижный виброхвост для равномерной проводки.", "price": 1150, "category": "Приманки"},
    {"name": "Слаг FishUp Dart 3.5\" (8 шт)", "description": "Пассивная приманка для ловли пассивного хищника.", "price": 490, "category": "Приманки"},
    {"name": "Поролоновая рыбка 5см (5 шт)", "description": "Легендарная приманка для ловли судака на джиг.", "price": 390, "category": "Приманки"},
    {"name": "Силиконовый червь Zoom Trick Worm 6\" (10 шт)", "description": "Уловистый червь с большой амплитудой игры.", "price": 720, "category": "Приманки"},

    {"name": "Блесна вращ. Mepps Aglia Long №2 серебро", "description": "Дальнобойная вращающаяся блесна с лепестком Aglia.", "price": 450, "category": "Блесны"},
    {"name": "Блесна Daiwa Silver Creek Spinner R 2.5г", "description": "Лёгкая блесна с отличной аэродинамикой.", "price": 620, "category": "Блесны"},
    {"name": "Колебалка Salmo Series 4 6.5см 12г", "description": "Колеблющаяся блесна для ловли щуки на глубине.", "price": 680, "category": "Блесны"},
    {"name": "Колебалка Abu Garcia Toby 18г", "description": "Знаменитая колебалка с широкой игрой.", "price": 750, "category": "Блесны"},
    {"name": "Блесна Blue Fox Matrixx Spinner №3", "description": "Вращалка с сердечником, создающим сильную вибрацию.", "price": 580, "category": "Блесны"},
    {"name": "Блесна вращ. Smith Niakis 9г", "description": "Японская вращалка для ловли на быстрой воде.", "price": 890, "category": "Блесны"},

    {"name": "Плетеный шнур Sunline Siglon PE 0.6# 135м", "description": "Качественная японская плетёнка с высокой разрывной нагрузкой.", "price": 1890, "category": "Лески и шнуры"},
    {"name": "Шнур плетёный Power Phantom 0.08мм 150м", "description": "Четырёхжильный шнур с гладким покрытием.", "price": 890, "category": "Лески и шнуры"},
    {"name": "Леска монофильная Trabucco T-Force 0.25мм 150м", "description": "Износостойкий монофил для поводков и оснасток.", "price": 490, "category": "Лески и шнуры"},
    {"name": "Флюорокарбон Sunline Sniper 100м 0.285мм", "description": "Невидимый в воде флюорокарбон для ответственных монтажей.", "price": 1350, "category": "Лески и шнуры"},
    {"name": "Леска плетёная YGK BornRush PE 0.8 150м", "description": "Очень прочная плетёнка для тяжёлого джига.", "price": 2150, "category": "Лески и шнуры"},
    {"name": "Леска монофильная Owner Broad 0.20мм 100м", "description": "Мягкая леска с хорошим узловязанием.", "price": 370, "category": "Лески и шнуры"},

    {"name": "Крючки Owner Mosquito Light №8 (20 шт)", "description": "Острые лёгкие крючки для поплавочной ловли.", "price": 390, "category": "Крючки"},
    {"name": "Крючки Gamakatsu F-1 508 №10 (15 шт)", "description": "Тонкие и прочные крючки для мотыля и опарыша.", "price": 280, "category": "Крючки"},
    {"name": "Крючки Mustad 32648 IN №4 (10 шт)", "description": "Кованые крючки для червя с бородкой.", "price": 210, "category": "Крючки"},
    {"name": "Офсетные крючки VMC 7117 №2/0 (10 шт)", "description": "Офсетники с широким зевом для крупного силикона.", "price": 450, "category": "Крючки"},
    {"name": "Двойник Owner №6 (10 шт)", "description": "Прочные двойники для оснащения воблеров и блёсен.", "price": 320, "category": "Крючки"},

    {"name": "Поплавок Colmic Cronos 2г", "description": "Спортивный поплавок с высокой чувствительностью.", "price": 180, "category": "Поплавки"},
    {"name": "Поплавок Maver Styl 1.5г", "description": "Лёгкий поплавок из бальзы для стоячей воды.", "price": 220, "category": "Поплавки"},
    {"name": "Поплавок Preston Durafloat 2.5г", "description": "Плавающий поплавок с отличной видимостью.", "price": 160, "category": "Поплавки"},
    {"name": "Поплавок скользящий 5г универсальный", "description": "Скользящий поплавок для дальнего заброса.", "price": 140, "category": "Поплавки"},

    {"name": "Кормушка металлическая 30г (клетка)", "description": "Классическая флет-кормушка для фидера.", "price": 190, "category": "Кормушки"},
    {"name": "Кормушка пластиковая 40г методная", "description": "Методная кормушка для быстрого прикармливания.", "price": 230, "category": "Кормушки"},
    {"name": "Кормушка Feeder basket 20г", "description": "Лёгкая корзинка для стартового закорма.", "price": 160, "category": "Кормушки"},
    {"name": "Кормушка Method feeder 30г", "description": "Кормушка с плоским дном для стоячей воды.", "price": 210, "category": "Кормушки"},

    {"name": "Прикормка Trapper Лещ-Плотва 1кг", "description": "Готовая прикормка с ароматом ванили для леща.", "price": 390, "category": "Прикормка"},
    {"name": "Прикормка Dunaev Premium Фидер 1.5кг", "description": "Универсальная фидерная прикормка с крупной фракцией.", "price": 470, "category": "Прикормка"},
    {"name": "Прикормка Sensas 3000 Match 2кг", "description": "Французская прикормка для матчевой ловли.", "price": 650, "category": "Прикормка"},

    {"name": "Сапоги болотные Nordman X", "description": "Лёгкие и прочные вейдерсы для ходовой рыбалки.", "price": 4390, "category": "Одежда"},
    {"name": "Перчатки Rapala Insulated зимние", "description": "Тёплые перчатки с отстёгивающимися пальцами.", "price": 1790, "category": "Одежда"},
    {"name": "Куртка летняя Daiwa Protection", "description": "Дышащая куртка с защитой от солнца и насекомых.", "price": 5890, "category": "Одежда"},

    {"name": "Садок резиновый 3м", "description": "Вместительный складной садок для сохранения улова.", "price": 1650, "category": "Аксессуары"},
    {"name": "Эхолот Garmin Striker Vivid 4cv", "description": "Компактный эхолот с цветным экраном и датчиком.", "price": 21900, "category": "Аксессуары"},
    {"name": "Сумка-холодильник Salmo 20л", "description": "Термосумка для сохранения улова и продуктов в жару.", "price": 3450, "category": "Аксессуары"},
    {"name": "Чехол для удилищ двуручный 1.6м", "description": "Мягкий чехол с карманами на две рукоятки.", "price": 1290, "category": "Аксессуары"},
    {"name": "Багорик телескопический с пробковой рукояткой", "description": "Надёжный багорик для извлечения крупной щуки.", "price": 1150, "category": "Аксессуары"},

    {"name": "Ножницы для лески Victorinox", "description": "Острые ножницы из нержавейки с чехлом.", "price": 1890, "category": "Инструменты"},
    {"name": "Плоскогубцы рыболовные с фиксатором", "description": "Многофункциональный инструмент для монтажа оснасток.", "price": 890, "category": "Инструменты"},

    # Спиннинги 
    {"name": "Спиннинг Graphiteleader Corto GLCCS-682L 2-10г", "description": "Высококачественный японский спиннинг для легкого джига.", "price": 18900, "category": "Спиннинги", "test_min": 2, "test_max": 10},
    {"name": "Спиннинг Norstream Areal 240 2-15г", "description": "Универсальный спиннинг для береговой ловли с быстрым строем.", "price": 8490, "category": "Спиннинги", "test_min": 2, "test_max": 15},
    {"name": "Спиннинг Maximus Dreamer 27L 3-18г", "description": "Дальнобойный спиннинг для микроджига и легких воблеров.", "price": 5990, "category": "Спиннинги", "test_min": 3, "test_max": 18},
    {"name": "Спиннинг Black Hole Bassmania S-240 7-28г", "description": "Бюджетный спиннинг для ловли на воблеры и блесны.", "price": 3290, "category": "Спиннинги", "test_min": 7, "test_max": 28},
    {"name": "Спиннинг Zemex Bass Force 240M 10-38г", "description": "Мощный спиннинг для трофейной щуки и судака.", "price": 5190, "category": "Спиннинги", "test_min": 10, "test_max": 38},
    {"name": "Спиннинг Major Craft K.G.Lights 23L 1-5г", "description": "Ультралайт премиум-класса для ловли форели.", "price": 9990, "category": "Спиннинги", "test_min": 1, "test_max": 5},

    # Катушки 
    {"name": "Катушка Shimano Ultegra 2500S", "description": "Легкая катушка с холоднокованым ротором, плавный ход.", "price": 10990, "category": "Катушки"},
    {"name": "Катушка Daiwa Freams LT 2500D", "description": "Мощная и легкая катушка с технологией MagSealed.", "price": 11990, "category": "Катушки"},
    {"name": "Катушка Abu Garcia Elite Max 30", "description": "Надежная катушка с двойным тормозом для больших нагрузок.", "price": 8990, "category": "Катушки"},
    {"name": "Катушка Ryobi Zauber 2000", "description": "Компактная катушка для ультралайта с фрикционом точной настройки.", "price": 4590, "category": "Катушки"},
    {"name": "Катушка Okuma RTX-30S", "description": "Скоростная катушка с облегченным ротором.", "price": 6290, "category": "Катушки"},
    {"name": "Катушка Favorite White Bird 2000", "description": "Бюджетная катушка с хорошей тягой для легких приманок.", "price": 2190, "category": "Катушки"},
    {"name": "Мультипликатор Shimano Curado DC 151", "description": "Мультипликаторная катушка с цифровой системой контроля заброса.", "price": 22900, "category": "Катушки"},
    {"name": "Мультипликатор Daiwa Tatula 100H", "description": "Популярный мультипликатор с системой T-Wing.", "price": 15990, "category": "Катушки"},
    {"name": "Мультипликатор Abu Garcia Ambassadeur SX 5600", "description": "Классический круглый мультипликатор для тяжелого джига.", "price": 12490, "category": "Катушки"},
    {"name": "Мультипликатор Favorite Extractor 7.3:1", "description": "Скоростной мультипликатор для твичинга.", "price": 8790, "category": "Катушки"},

    # Фидеры 
    {"name": "Фидер Preston Monster Feeder 390 150г", "description": "Профессиональный фидер для ловли крупной рыбы.", "price": 12490, "category": "Фидеры", "test_min": 0, "test_max": 150},
    {"name": "Фидер Shimano Tribal TX-2 360 100г", "description": "Универсальный фидер с высокой чувствительностью вершинки.", "price": 9490, "category": "Фидеры", "test_min": 0, "test_max": 100},
    {"name": "Фидер Волжанка Мастер 420 180г", "description": "Мощный фидер для дальнего заброса на крупных реках.", "price": 6690, "category": "Фидеры", "test_min": 0, "test_max": 180},

    # Карповые удилища 
    {"name": "Карповое удилище Fox Horizon XTC 120г", "description": "Премиальное карповое удилище с высокой прочностью.", "price": 18900, "category": "Карповые удилища", "test_min": 0, "test_max": 120},
    {"name": "Карповое удилище Shimano Tribal Velocity 130г", "description": "Универсальное удилище для карпятника.", "price": 11990, "category": "Карповые удилища", "test_min": 0, "test_max": 130},
    {"name": "Карповое удилище Mikado Carp Spirit 366 150г", "description": "Бюджетное карповое удилище с хорошим строем.", "price": 5490, "category": "Карповые удилища", "test_min": 0, "test_max": 150},

    # Зимние удочки 
    {"name": "Зимняя удочка Salmo Ice Fighter 60см", "description": "Легкая удочка для блеснения окуня.", "price": 1290, "category": "Зимние удочки", "test_min": None, "test_max": None},
    {"name": "Зимняя удочка Lucky John MGS 55см", "description": "Удочка с кивком для ловли на мормышку.", "price": 890, "category": "Зимние удочки", "test_min": None, "test_max": None},
    {"name": "Зимняя удочка Stinger Power Ice 70см", "description": "Мощная удочка для балансира и крупной щуки.", "price": 1590, "category": "Зимние удочки", "test_min": None, "test_max": None},

    # Воблеры 
    {"name": "Воблер OSP Rudra 130SP", "description": "Крупный составной воблер для трофейной щуки.", "price": 2200, "category": "Воблеры"},
    {"name": "Воблер Ever Green M-1 Invisible 80", "description": "Уловистый воблер-минноу нейтральной плавучести.", "price": 1600, "category": "Воблеры"},
    {"name": "Воблер Pontoon 21 Crackjack 78MR", "description": "Дальнобойный воблер с активной игрой.", "price": 1100, "category": "Воблеры"},
    {"name": "Воблер Lucky Craft Pointer 100SP", "description": "Классический суспендер для твичинга судака.", "price": 1500, "category": "Воблеры"},
    {"name": "Воблер Rapala Shadow Rap 11см", "description": "Плавающий воблер для ловли на мелководье.", "price": 1350, "category": "Воблеры"},

    # Приманки 
    {"name": "Силикон Bass Assassin 4\" (10 шт)", "description": "Универсальный виброхвост с интенсивной игрой.", "price": 690, "category": "Приманки"},
    {"name": "Слаг Reins Palpunt 4\" (8 шт)", "description": "Имитация малька с пассивной игрой для пассивного хищника.", "price": 850, "category": "Приманки"},
    {"name": "Силиконовая креатура Geecrack Bellows Gill 3.8\" (6 шт)", "description": "Реалистичная имитация лягушки для ловли щуки.", "price": 980, "category": "Приманки"},
    {"name": "Поролоновая рыбка Акелла 6см (5 шт)", "description": "Судаковая поролонка с отличной плавучестью.", "price": 420, "category": "Приманки"},
    {"name": "Силикон Kosadaka Revolt 3.5\" (10 шт)", "description": "Съедобный силикон с запахом чеснока.", "price": 550, "category": "Приманки"},

    # Блесны 
    {"name": "Колебалка Kuusamo Professor 3 18г", "description": "Финская колебалка с уникальной игрой для щуки.", "price": 950, "category": "Блесны"},
    {"name": "Вертушка Myran Tinsel 12г", "description": "Шведская вращалка с красной шерстинкой.", "price": 520, "category": "Блесны"},
    {"name": "Блесна Acme Kastmaster 7г", "description": "Универсальная блесна для дальнего заброса.", "price": 380, "category": "Блесны"},

    # Балансиры 
    {"name": "Балансир Rapala Jigging Rap 5см 9г", "description": "Уловистый балансир для зимней ловли окуня и судака.", "price": 780, "category": "Балансиры"},
    {"name": "Балансир Lucky John Classic 4см 10г", "description": "Балансир с широкой амплитудой игры.", "price": 490, "category": "Балансиры"},
    {"name": "Балансир Scorana Ice Crystal 5см 12г", "description": "Балансир с яркой голограммой для привлечения хищника.", "price": 650, "category": "Балансиры"},

    # Мормышки 
    {"name": "Мормышка капля 0.5г вольфрам", "description": "Тяжелая мормышка для ловли на глубине.", "price": 95, "category": "Мормышки"},
    {"name": "Мормышка Salmo Diamond Moth 0.3г", "description": "Безмотыльная мормышка с бриллиантовой огранкой.", "price": 120, "category": "Мормышки"},
    {"name": "Мормышка Lucky John GLK 0.6г", "description": "Крупная мормышка с крючком Owner.", "price": 110, "category": "Мормышки"},

    # Лески и шнуры 
    {"name": "Плетеный шнур Daiwa J-Braid 8x 0.13мм 150м", "description": "Восьмижильная плетенка с круглым сечением.", "price": 1490, "category": "Лески и шнуры"},
    {"name": "Флюорокарбон Owner Fluoro 0.235мм 50м", "description": "Жесткий флюорокарбон для поводков.", "price": 620, "category": "Лески и шнуры"},

    # Крючки 
    {"name": "Крючки Kamasan B560 №6 (10 шт)", "description": "Прочные крючки для фидера и поплавка.", "price": 290, "category": "Крючки"},
    {"name": "Крючки карповые Gardner Mugga 2 (10 шт)", "description": "Усиленные крючки с тефлоновым покрытием.", "price": 420, "category": "Крючки"},
    {"name": "Крючки Owner 53144 №12 (15 шт)", "description": "Тонкие крючки для мотыля.", "price": 250, "category": "Крючки"},

    # Поплавки 
    {"name": "Поплавок Drennan Crystal 2г", "description": "Прозрачный поплавок с хорошей остойчивостью.", "price": 210, "category": "Поплавки"},
    {"name": "Поплавок Tubertini Minifloat 1г", "description": "Миниатюрный поплавок для штекерной ловли.", "price": 190, "category": "Поплавки"},

    # Кормушки 
    {"name": "Кормушка-пуля Preston 20г", "description": "Обтекаемая кормушка для дальнего заброса.", "price": 175, "category": "Кормушки"},
    {"name": "Кормушка флэт методная 45г средняя", "description": "Методная кормушка с огрузкой.", "price": 240, "category": "Кормушки"},

    # Прикормка 
    {"name": "Прикормка Dynamite Baits Swim Stim Betaine Green 1кг", "description": "Английская прикормка с бетаином для карпа.", "price": 590, "category": "Прикормка"},
    {"name": "Прикормка Browning Black Viper 1кг", "description": "Универсальная прикормка темного цвета.", "price": 420, "category": "Прикормка"},

    # Одежда 
    {"name": "Зимний костюм Shimano Kairiki", "description": "Теплый костюм с мембраной для суровых условий.", "price": 22500, "category": "Одежда"},
    {"name": "Летние брюки Daiwa Airdrive", "description": "Легкие дышащие брюки с защитой от УФ.", "price": 4990, "category": "Одежда"},
    {"name": "Куртка флисовая Norfin Wild", "description": "Утепляющий слой для межсезонья.", "price": 3890, "category": "Одежда"},
    {"name": "Вейдерсы водостойкие Rapala Vario 2", "description": "Полукомбинезон из неопрена 3 мм.", "price": 8990, "category": "Одежда"},

    # Аксессуары 
    {"name": "Садок пластиковый 2.5м", "description": "Плавающий садок с мелкой ячеей.", "price": 1450, "category": "Аксессуары"},
    {"name": "Подсак Fox Rage Predator 90см", "description": "Подсак с прорезиненной сеткой для хищника.", "price": 3890, "category": "Аксессуары"},
    {"name": "Стойка под удилище Carp Zoom 2 шт.", "description": "Регулируемые стойки с сигнализатором.", "price": 1790, "category": "Аксессуары"},
    {"name": "Сигнализатор поклевки Fox Mini Micron", "description": "Электронный сигнализатор с регулировкой громкости.", "price": 2690, "category": "Аксессуары"},
    {"name": "Эхолот Lowrance Hook Reveal 5", "description": "Эхолот с GPS и картплоттером.", "price": 34900, "category": "Аксессуары"},
    {"name": "Зарядное устройство для аккумуляторов Norfin 12V", "description": "Интеллектуальное зарядное устройство.", "price": 2190, "category": "Аксессуары"},
    {"name": "Ящик для снастей Meiho VS-708", "description": "Компактный ящик с перегородками.", "price": 890, "category": "Аксессуары"},
    {"name": "Сумка поясная для приманок Flambeau", "description": "Удобная сумка с отделениями.", "price": 1550, "category": "Аксессуары"},
    {"name": "Чехол для катушек Daiwa", "description": "Защитный неопреновый чехол.", "price": 750, "category": "Аксессуары"},
    {"name": "Экстрактор хирургический 25см", "description": "Инструмент для извлечения крючков.", "price": 380, "category": "Аксессуары"},
    {"name": "Грузила каплевидные 10-30г набор", "description": "Набор грузил для джига.", "price": 490, "category": "Аксессуары"},
    {"name": "Поводки стальные 15см (10 шт)", "description": "Надежные поводки для щуки.", "price": 320, "category": "Аксессуары"},

    # Инструменты 
    {"name": "Ножницы для плетенки Cuda", "description": "Титановые ножницы с чехлом.", "price": 1290, "category": "Инструменты"},
    {"name": "Щипцы для снятия крючков Fox Rage", "description": "Длинные щипцы с фиксатором.", "price": 790, "category": "Инструменты"},

    # Палатки 
    {"name": "Палатка зимняя Norfin Winter 2-мест.", "description": "Быстросборная палатка с утепленным дном.", "price": 11500, "category": "Палатки"},
    {"name": "Палатка летняя Carp Zoom Easy Shelter", "description": "Легкая палатка для карпфишинга.", "price": 6990, "category": "Палатки"},

    # Электроника 
    {"name": "Видеокамера для рыбалки GoFish Cam", "description": "Подводная камера для съемки поклевок.", "price": 8900, "category": "Электроника"},

    
    {"name": "Спиннинг G.Loomis E6X 240 5-15г", "description": "Премиальный американский спиннинг с высокой чувствительностью.", "price": 27900, "category": "Спиннинги", "test_min": 5, "test_max": 15},
    {"name": "Катушка Penn Battle III 2500", "description": "Мощная катушка для морской и пресноводной ловли.", "price": 7990, "category": "Катушки"},
    {"name": "Воблер Duo Realis Jerkbait 120SP", "description": "Составной воблер с размашистой игрой.", "price": 1450, "category": "Воблеры"},
    {"name": "Силикон Gary Yamamoto Senko 5\" (7 шт)", "description": "Знаменитый червь для техасской оснастки.", "price": 650, "category": "Приманки"},
    {"name": "Сумка для удилищ Lucky John 1.5м", "description": "Мягкая сумка на два отделения.", "price": 1390, "category": "Аксессуары"},
    {"name": "Застёжка-карабин Owner №1 (10 шт)", "description": "Надёжные застёжки для быстрой смены приманок.", "price": 290, "category": "Аксессуары"},
     # Спиннинги 
    {"name": "Спиннинг Norstream Areal New 270 3-18г", "description": "Обновлённая версия популярного спиннинга с быстрым строем.", "price": 8990, "category": "Спиннинги", "test_min": 3, "test_max": 18},
    {"name": "Спиннинг Favorite X1 Ultra 210 1-7г", "description": "Ультралайтовый спиннинг для деликатных приманок.", "price": 3490, "category": "Спиннинги", "test_min": 1, "test_max": 7},
    {"name": "Спиннинг Zemex Spider Pro 270 10-32г", "description": "Универсальный спиннинг с большим тестом для трофейной рыбы.", "price": 5090, "category": "Спиннинги", "test_min": 10, "test_max": 32},
    {"name": "Спиннинг Black Hole NS Matrix II 240 5-21г", "description": "Второе поколение лёгкого и сбалансированного спиннинга.", "price": 5890, "category": "Спиннинги", "test_min": 5, "test_max": 21},
    {"name": "Спиннинг Major Craft Solpara SPS-S240ML 5-20г", "description": "Надёжный спиннинг с чувствительным бланком для джига.", "price": 7690, "category": "Спиннинги", "test_min": 5, "test_max": 20},
    {"name": "Спиннинг Stinger Manic 27 10-30г", "description": "Бюджетный спиннинг быстрого строя для береговой ловли.", "price": 2790, "category": "Спиннинги", "test_min": 10, "test_max": 30},
    {"name": "Спиннинг Maximus Black Widow 24L 5-18г", "description": "Лёгкий и звонкий спиннинг для твичинга и лёгкого джига.", "price": 4490, "category": "Спиннинги", "test_min": 5, "test_max": 18},
    {"name": "Спиннинг Kosadaka Menace 270 15-45г", "description": "Мощный спиннинг для крупных приманок и трофейной щуки.", "price": 3690, "category": "Спиннинги", "test_min": 15, "test_max": 45},
    {"name": "Спиннинг Lucky John Progress Jig 27 10-30г", "description": "Универсальный спиннинг средне-быстрого строя.", "price": 4590, "category": "Спиннинги", "test_min": 10, "test_max": 30},
    {"name": "Спиннинг Graphiteleader Aspro 210 2-12г", "description": "Премиальный лёгкий спиннинг для микроджига и воблеров.", "price": 21500, "category": "Спиннинги", "test_min": 2, "test_max": 12},
    {"name": "Спиннинг Abu Garcia Veritas 240 7-28г", "description": "Прочный и лёгкий спиннинг с технологией Powerlux.", "price": 8990, "category": "Спиннинги", "test_min": 7, "test_max": 28},

    # Катушки 
    {"name": "Катушка Shimano Vanford 2500", "description": "Лёгкая и мощная катушка с фрикционом MGL.", "price": 15490, "category": "Катушки"},
    {"name": "Катушка Daiwa Ballistic LT 2500D", "description": "Профессиональная катушка с технологией Zaion.", "price": 14990, "category": "Катушки"},
    {"name": "Катушка Abu Garcia Revo Rocket 30", "description": "Скоростная катушка (7.6:1) для активной ловли.", "price": 10990, "category": "Катушки"},
    {"name": "Катушка Ryobi Exia MX 3000", "description": "Обновлённая версия с улучшенной укладкой лески.", "price": 3990, "category": "Катушки"},
    {"name": "Катушка Okuma Ceymar XT 30", "description": "Бюджетная катушка с дисковым тормозом.", "price": 4690, "category": "Катушки"},
    {"name": "Катушка Favorite White Bird 3000", "description": "Надёжная бюджетная катушка для средних нагрузок.", "price": 2590, "category": "Катушки"},
    {"name": "Катушка Tsurinoya Spirit Fox 3000", "description": "Популярная катушка с отличной тягой для джига.", "price": 4890, "category": "Катушки"},
    {"name": "Катушка Spro Zalt X 2500", "description": "Усовершенствованная модель с усиленным механизмом.", "price": 7290, "category": "Катушки"},
    {"name": "Катушка Stinger Power 4000", "description": "Бюджетная катушка для тяжёлого джига.", "price": 2990, "category": "Катушки"},
    {"name": "Катушка Mitchell 300 Pro", "description": "Современная классика с плавным ходом.", "price": 5590, "category": "Катушки"},
    {"name": "Катушка Penn Battle III 3000", "description": "Мощная катушка для морской и пресноводной ловли.", "price": 8490, "category": "Катушки"},
    {"name": "Катушка Shimano Sahara FJ 2500", "description": "Обновлённая бюджетная катушка с холоднокованым ротором.", "price": 7490, "category": "Катушки"},

    # Фидеры 
    {"name": "Фидер Salmo Sniper Feeder 420 150г", "description": "Мощный фидер для дальнего заброса кормушек до 150г.", "price": 6490, "category": "Фидеры", "test_min": 0, "test_max": 150},
    {"name": "Фидер Волжанка Оптима 420 180г", "description": "Удлинённый фидер для ловли на крупных водоёмах.", "price": 5690, "category": "Фидеры", "test_min": 0, "test_max": 180},
    {"name": "Фидер Shimano Beastmaster Feeder 420 140г", "description": "Премиальный фидер с идеальной сенсорикой.", "price": 14490, "category": "Фидеры", "test_min": 0, "test_max": 140},
    {"name": "Фидер Daiwa Whisker 390 120г", "description": "Лёгкий и точный фидер для стоячей воды.", "price": 8990, "category": "Фидеры", "test_min": 0, "test_max": 120},
    {"name": "Фидер Preston Monster Feeder 420 180г", "description": "Профессиональный фидер для трофейной рыбы.", "price": 13490, "category": "Фидеры", "test_min": 0, "test_max": 180},
    {"name": "Фидер Browning Black Viper 390 120г", "description": "Универсальный фидер с быстрым строем.", "price": 7990, "category": "Фидеры", "test_min": 0, "test_max": 120},

    # Карповые удилища 
    {"name": "Карповое удилище Fox Horizon XTC 150г", "description": "Премиальное удилище с высокой прочностью.", "price": 19900, "category": "Карповые удилища", "test_min": 0, "test_max": 150},
    {"name": "Карповое удилище Shimano Tribal Velocity 160г", "description": "Универсальное удилище для карпятника.", "price": 12990, "category": "Карповые удилища", "test_min": 0, "test_max": 160},
    {"name": "Карповое удилище Mikado Carp Spirit 396 180г", "description": "Бюджетное удилище с параболическим строем.", "price": 5890, "category": "Карповые удилища", "test_min": 0, "test_max": 180},
    {"name": "Карповое удилище Daiwa Longbow 360 120г", "description": "Лёгкое удилище с отличной бросковостью.", "price": 10990, "category": "Карповые удилища", "test_min": 0, "test_max": 120},
    {"name": "Карповое удилище Sonik SKS 366 150г", "description": "Надёжное удилище с высококачественной фурнитурой.", "price": 8990, "category": "Карповые удилища", "test_min": 0, "test_max": 150},
    {"name": "Карповое удилище JRC Contact 360 130г", "description": "Проверенное временем карповое удилище.", "price": 7490, "category": "Карповые удилища", "test_min": 0, "test_max": 130},

    # Зимние удочки 
    {"name": "Зимняя удочка Rapala Ice Pro 60см 2-6г", "description": "Лёгкая удочка для блеснения окуня с чувствительным кивком.", "price": 1490, "category": "Зимние удочки", "test_min": 2, "test_max": 6},
    {"name": "Зимняя удочка Lucky John MGS Ice 60см 1-4г", "description": "Удочка с кивком для деликатной ловли на мормышку.", "price": 990, "category": "Зимние удочки", "test_min": 1, "test_max": 4},
    {"name": "Зимняя удочка Stinger Power Ice Pro 70см 4-10г", "description": "Мощная удочка для балансира и крупной щуки.", "price": 1790, "category": "Зимние удочки", "test_min": 4, "test_max": 10},
    {"name": "Зимняя удочка Salmo Ice Rod 50см 1-5г", "description": "Компактная удочка для ловли в палатке.", "price": 1190, "category": "Зимние удочки", "test_min": 1, "test_max": 5},
    {"name": "Зимняя удочка Favorite Frost 55см 2-8г", "description": "Универсальная зимняя удочка для блёсен и балансиров.", "price": 1390, "category": "Зимние удочки", "test_min": 2, "test_max": 8},

    # Воблеры 
    {"name": "Воблер ZipBaits Rigge 70S", "description": "Тонущий воблер для скоростного твичинга.", "price": 1350, "category": "Воблеры"},
    {"name": "Воблер OSP Varuna 110SP", "description": "Суспендер с размашистой игрой для щуки.", "price": 2100, "category": "Воблеры"},
    {"name": "Воблер Ever Green Showerblows 105", "description": "Поверхностный воблер для ловли над травой.", "price": 1700, "category": "Воблеры"},
    {"name": "Воблер Pontoon 21 Bet-A 70F", "description": "Плавающий воблер с активной игрой для окуня.", "price": 900, "category": "Воблеры"},
    {"name": "Воблер Lucky Craft Flash Pointer 115MR", "description": "Дальнобойный суспендер для морских и речных хищников.", "price": 1550, "category": "Воблеры"},
    {"name": "Воблер Rapala BX Minnow 10", "description": "Воблер из бальсы с живой игрой для трофейной щуки.", "price": 1450, "category": "Воблеры"},
    {"name": "Воблер Megabass Giant Dog-X", "description": "Крупный поппер для зрелищных поклёвок.", "price": 1950, "category": "Воблеры"},
    {"name": "Воблер Jackall Rerange 110", "description": "Высокотехнологичный воблер с магнитной системой дальнего заброса.", "price": 1800, "category": "Воблеры"},
    {"name": "Воблер Daiwa Lezard 85SP", "description": "Суспендер с реалистичной формой малька.", "price": 1350, "category": "Воблеры"},
    {"name": "Воблер Googan Squad Scout 4.0", "description": "Плавающий воблер с шумовой камерой.", "price": 980, "category": "Воблеры"},

    # Приманки (силикон поролон) 
    {"name": "Виброхвост Keitech Fat Swing Impact 4.8\" (10 шт)", "description": "Широкое тело и мощная игра для крупного хищника.", "price": 1150, "category": "Приманки"},
    {"name": "Твистер Relax Twister 3\" (10 шт)", "description": "Миниатюрный твистер для окуня и форели.", "price": 480, "category": "Приманки"},
    {"name": "Слаг Kosadaka Diesel Slug 4\" (8 шт)", "description": "Пассивная приманка для ловли пассивного хищника.", "price": 510, "category": "Приманки"},
    {"name": "Силикон Berkley PowerBait MaxScent Flat Worm 4.25\" (6 шт)", "description": "Плоский червь с запахом, привлекающий рыбу.", "price": 920, "category": "Приманки"},
    {"name": "Виброхвост Bass Assassin Turbo Shad 5\" (8 шт)", "description": "Крупный виброхвост с интенсивной игрой.", "price": 790, "category": "Приманки"},
    {"name": "Силиконовый рак Keitech Sexy Impact 3\" (6 шт)", "description": "Реалистичная имитация рака для джига.", "price": 880, "category": "Приманки"},
    {"name": "Поролоновая рыбка Акелла 8см (5 шт)", "description": "Крупная поролонка для трофейного судака.", "price": 460, "category": "Приманки"},
    {"name": "Силиконовая креатура Geecrack Bellows Gill 4.8\" (6 шт)", "description": "Увеличенная имитация лягушки для летней ловли.", "price": 1050, "category": "Приманки"},

    # Блесны 
    {"name": "Колебалка Atom 15г", "description": "Легендарная советская колебалка с широкой игрой.", "price": 420, "category": "Блесны"},
    {"name": "Вертушка Mepps Aglia Long №3 медь", "description": "Дальнобойная вращалка с медным лепестком.", "price": 470, "category": "Блесны"},
    {"name": "Колебалка Abu Garcia Pike 25г", "description": "Тяжёлая колебалка для глубинной ловли щуки.", "price": 820, "category": "Блесны"},
    {"name": "Блесна Acme Little Cleo 10г", "description": "Универсальная колебалка для форели и окуня.", "price": 410, "category": "Блесны"},

    # Балансиры 
    {"name": "Балансир Nils Master Jigging Shad 5см 12г", "description": "Финский балансир с объёмной игрой.", "price": 850, "category": "Балансиры"},
    {"name": "Балансир Striker Turbo 4см 10г", "description": "Компактный балансир для окуня.", "price": 520, "category": "Балансиры"},

    # Мормышки 
    {"name": "Мормышка диск 0.4г вольфрам", "description": "Плоская мормышка для безмотыльной ловли.", "price": 100, "category": "Мормышки"},

    # Лески и шнуры 
    {"name": "Плетеный шнур Shimano Kairiki 8 0.10мм 150м", "description": "Восьмижильная плетёнка с высокой абразивостойкостью.", "price": 1690, "category": "Лески и шнуры"},
    {"name": "Леска монофильная Daiwa Sensor 0.22мм 150м", "description": "Прозрачная монофильная леска с отличной прочностью.", "price": 450, "category": "Лески и шнуры"},
    {"name": "Флюорокарбон Sunline Sniper BMS 0.26мм 50м", "description": "Мягкий и невидимый в воде флюорокарбон.", "price": 720, "category": "Лески и шнуры"},
    {"name": "Шнур плетёный Varivas High Grade PE 0.8 150м", "description": "Японская плетёнка премиум-класса с круглым сечением.", "price": 2390, "category": "Лески и шнуры"},
    {"name": "Леска монофильная Trabucco Strong 0.30мм 150м", "description": "Усиленная монофильная леска для карповой ловли.", "price": 520, "category": "Лески и шнуры"},

    # Крючки 
    {"name": "Крючки Owner 50922 №8 (15 шт)", "description": "Тонкие крючки для поплавочной ловли.", "price": 350, "category": "Крючки"},
    {"name": "Крючки Gamakatsu LS-5313N №5 (10 шт)", "description": "Универсальные крючки с лопаткой для насаживания червя.", "price": 270, "category": "Крючки"},
    {"name": "Крючки Mustad Ultra Point 32608 №2 (10 шт)", "description": "Кованые крючки с супер-острым жалом.", "price": 230, "category": "Крючки"},
    {"name": "Офсетные крючки VMC 7119 №3/0 (10 шт)", "description": "Широкие офсетники для объёмных силиконовых приманок.", "price": 470, "category": "Крючки"},
    {"name": "Крючки карповые Korda Wide Gape 4 (10 шт)", "description": "Популярные крючки для волосяной оснастки.", "price": 390, "category": "Крючки"},

    # Поплавки 
    {"name": "Поплавок Drennan Crystal 3г", "description": "Прозрачный поплавок для осторожной рыбы.", "price": 240, "category": "Поплавки"},
    {"name": "Поплавок Maver Styl 2г", "description": "Лёгкий бальзовый поплавок для матчевой ловли.", "price": 250, "category": "Поплавки"},
    {"name": "Поплавок Preston Durafloat 3г", "description": "Плавающий поплавок с отличной видимостью.", "price": 180, "category": "Поплавки"},
    {"name": "Поплавок Colmic Cronos 3г", "description": "Спортивный поплавок с высокой чувствительностью.", "price": 200, "category": "Поплавки"},
    {"name": "Поплавок скользящий 8г", "description": "Скользящий поплавок для дальнего заброса.", "price": 150, "category": "Поплавки"},

    # Кормушки 
    {"name": "Кормушка металлическая 50г (клетка)", "description": "Тяжёлая флет-кормушка для сильного течения.", "price": 220, "category": "Кормушки"},
    {"name": "Кормушка методная 60г", "description": "Крупная кормушка для быстрого закорма.", "price": 260, "category": "Кормушки"},
    {"name": "Кормушка флэт 30г", "description": "Плоская кормушка для стоячей воды.", "price": 185, "category": "Кормушки"},
    {"name": "Кормушка-пуля Preston 30г", "description": "Обтекаемая кормушка для точного заброса.", "price": 195, "category": "Кормушки"},
    {"name": "Кормушка Feeder basket 40г", "description": "Универсальная корзинка для стартового закорма.", "price": 170, "category": "Кормушки"},

    # Прикормка 
    {"name": "Прикормка Sensas 3000 Carp 2кг", "description": "Французская прикормка для карпа с крупными фракциями.", "price": 690, "category": "Прикормка"},
    {"name": "Прикормка Dunaev Premium Универсал 1.5кг", "description": "Сбалансированная прикормка для разной рыбы.", "price": 490, "category": "Прикормка"},
    {"name": "Прикормка Trapper Карась 1кг", "description": "Ароматная прикормка с запахом аниса для карася.", "price": 370, "category": "Прикормка"},

    # Одежда 
    {"name": "Зимний костюм Shimano Kairiki Pro", "description": "Усиленный мембранный костюм для экстремальных условий.", "price": 24500, "category": "Одежда"},
    {"name": "Летний костюм Norfin Air", "description": "Максимально дышащий костюм для жары.", "price": 10900, "category": "Одежда"},
    {"name": "Демисезонный костюм Daiwa Airdrive", "description": "Лёгкий непродуваемый костюм для весны и осени.", "price": 9900, "category": "Одежда"},
    {"name": "Куртка зимняя Rapala Max", "description": "Тёплая куртка с утеплителем Thinsulate.", "price": 13900, "category": "Одежда"},
    {"name": "Перчатки флисовые Norfin", "description": "Мягкие перчатки для прохладной погоды.", "price": 990, "category": "Одежда"},
    {"name": "Шапка зимняя Lucky John", "description": "Тёплая шапка с флисовой подкладкой.", "price": 790, "category": "Одежда"},
    {"name": "Ботинки зимние EVA Nordman Pro", "description": "Лёгкие и тёплые ботинки для зимней рыбалки.", "price": 4990, "category": "Одежда"},
    {"name": "Сапоги болотные Norfin Hike", "description": "Высокие сапоги с усиленной подошвой.", "price": 4590, "category": "Одежда"},
    {"name": "Жилет спасательный автоматический", "description": "Надувной жилет с ручным и автоматическим срабатыванием.", "price": 6990, "category": "Одежда"},
    {"name": "Костюм поплавковый Fox", "description": "Лёгкий водоотталкивающий костюм для лета.", "price": 11900, "category": "Одежда"},

    # Аксессуары 
    {"name": "Ящик для снастей Plano 7771", "description": "Вместительный ящик с водонепроницаемым уплотнителем.", "price": 5590, "category": "Аксессуары"},
    {"name": "Сумка-холодильник Salmo 30л", "description": "Увеличенная термосумка для крупного улова.", "price": 4450, "category": "Аксессуары"},
    {"name": "Подсак телескопический 250см", "description": "Удлинённый подсак для ловли с обрывистого берега.", "price": 3190, "category": "Аксессуары"},
    {"name": "Стойки под удилище Daiwa", "description": "Устойчивые треноги с резьбовым креплением.", "price": 2190, "category": "Аксессуары"},
    {"name": "Сигнализатор поклевки Delkim TXi", "description": "Премиальный сигнализатор с вибро- и звуковой индикацией.", "price": 3590, "category": "Аксессуары"},
    {"name": "Эхолот Garmin EchoMAP UHD 73sv", "description": "Эхолот с картплоттером и ультрачётким дисплеем.", "price": 56900, "category": "Аксессуары"},
    {"name": "Зарядное устройство для LiFePO4 аккумуляторов 12В", "description": "Интеллектуальное ЗУ для современных литиевых батарей.", "price": 2790, "category": "Аксессуары"},
    {"name": "Экстрактор пластиковый 20см", "description": "Лёгкий экстрактор для извлечения крючков у некрупной рыбы.", "price": 290, "category": "Аксессуары"},
    {"name": "Грузила джиг-головки набор", "description": "Набор джиг-головок разного веса с крючком.", "price": 590, "category": "Аксессуары"},
    {"name": "Поводки стальные 20см (10 шт)", "description": "Удлинённые поводки для крупной щуки.", "price": 360, "category": "Аксессуары"},
    {"name": "Чехол для удилищ жёсткий 1.5м", "description": "Жёсткий тубус для безопасной перевозки спиннингов.", "price": 2190, "category": "Аксессуары"},
    {"name": "Ножницы для лески Fiskars", "description": "Острые ножницы с возвратной пружиной.", "price": 1490, "category": "Аксессуары"},

    # Инструменты 
    {"name": "Мультитул Leatherman Wave+", "description": "Многофункциональный инструмент премиум-класса.", "price": 11900, "category": "Инструменты"},
    {"name": "Плоскогубцы рыболовные с бокорезами Rapala", "description": "Универсальный инструмент для монтажа и резки лески.", "price": 1190, "category": "Инструменты"},
    {"name": "Ножницы для плетенки Gerber Magnum", "description": "Мощные ножницы с титановым покрытием.", "price": 1590, "category": "Инструменты"},
    {"name": "Щипцы для снятия крючков Daiwa", "description": "Длинные щипцы с изогнутыми губками.", "price": 890, "category": "Инструменты"},
    {"name": "Зажим для лески", "description": "Компактный зажим для фиксации лески на шпуле.", "price": 220, "category": "Инструменты"},

    # Палатки и кемпинг 
    {"name": "Палатка зимняя Tramp Ice", "description": "Утеплённая палатка-автомат с быстрой сборкой.", "price": 12500, "category": "Палатки"},
    {"name": "Палатка летняя QuickFish 2", "description": "Лёгкая одноместная палатка для карпфишинга.", "price": 5490, "category": "Палатки"},
    {"name": "Спальный мешок Norfin Comfort -10", "description": "Тёплый спальник с капюшоном для весны и осени.", "price": 4990, "category": "Палатки"},
    {"name": "Кресло карповое Carp Zoom", "description": "Удобное складное кресло с регулируемыми ножками.", "price": 3490, "category": "Палатки"},
    {"name": "Стол складной алюминиевый", "description": "Лёгкий стол для приготовления прикормки.", "price": 2390, "category": "Палатки"}

]
    df = pd.DataFrame(quality_products)

    # Удалем дубликаты по названию
    df = df.drop_duplicates(subset=['name'], keep='first')

    # +уникальный id с 1
    df = df.reset_index(drop=True)
    df.insert(0, 'id', range(1, len(df) + 1))

    # Сохраняем 
    df.to_csv(data_dir / "products.csv", index=False, encoding='utf-8')

    # Создание файла для эмбеддингов
    df['text_for_embedding'] = df.apply(
        lambda row: f"{row['name']}. {row['category']}. {row['description']} "
                    f"test_min_{row.get('test_min', 'nan')} "
                    f"test_max_{row.get('test_max', 'nan')}", axis=1 )
    df.to_csv(data_dir / "products_with_text.csv", index=False, encoding='utf-8')

    print(f"Создано {len(df)} товаров")
    print(f"products.csv с id")
    print(f"products_with_text.csv готов")
    print(df[['id', 'name', 'category', 'price']].head(10))

if __name__ == "__main__":
    dataset()