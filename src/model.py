"""
Модель для прототипа Streamlit
Автор: Гребцов Никита Юрьевич
Тема ВКР: Разработка интеллектуального помощника по подбору товаров
"""

import torch
import pandas as pd
import re
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

FISH_TEST_HINTS = {
    'щука': (10, 40),
    'окунь': (1, 15),
    'судак': (7, 28),
    'жерех': (5, 21),
    'голавль': (3, 18),
    'берш': (7, 25),
    'сом': (50, 200),
    'налим': (5, 25),
    'язь': (3, 15),
}

CATEGORY_KEYWORDS = {
    'Спиннинги': ['спиннинг', 'спинн', 'палка', 'удилище', 'удочка', 'спининг'],
    'Катушки': ['катушка', 'катушку', 'катушки', 'безынерционка', 'мультипликатор'],
    'Фидеры': ['фидер', 'фидерное', 'фидерка'],
    'Карповые удилища': ['карповое', 'карповый', 'карпятник', 'карповые'],
    'Зимние удочки': ['зимняя удочка', 'зимней удочки', 'для зимы', 'зимняя ловля', 'блеснение'],
    'Воблеры': ['воблер', 'воблеры', 'минноу', 'кренк'],
    'Приманки': ['приманка', 'приманки', 'силикон', 'виброхвост', 'твистер', 'джиг'],
    'Блесны': ['блесна', 'блесны', 'колебалка', 'вертушка'],
    'Лески и шнуры': ['леска', 'леску', 'шнур', 'плетенка', 'флюорокарбон'],
    'Одежда': ['костюм', 'куртка', 'сапоги', 'перчатки', 'вейдерсы', 'одежда'],
    'Аксессуары': ['подсак', 'садок', 'эхолот', 'ящик', 'чехол'],
}

FISH_VARIATIONS = {
    'щука': ['щука', 'щуку', 'щуки', 'на щуку', 'для щуки', 'щук'],
    'окунь': ['окунь', 'окуня', 'окуни', 'на окуня', 'для окуня'],
    'судак': ['судак', 'судака', 'судаку', 'на судака', 'для судака'],
    'жерех': ['жерех', 'жереха', 'на жереха'],
    'голавль': ['голавль', 'голавля', 'на голавля'],
    'берш': ['берш', 'берша', 'на берша'],
    'сом': ['сом', 'сома', 'на сома'],
    'налим': ['налим', 'налима', 'на налима'],
    'язь': ['язь', 'язя', 'на язя'],
    'карп': ['карп', 'карпа', 'на карпа', 'карповую'],
    'лещ': ['лещ', 'леща', 'на леща'],
    'карась': ['карась', 'карася', 'на карася'],
}

# Нормализация запроса
def _normalize_query(query: str) -> str:
    q = query.lower().replace('ё', 'е')
    q = q.replace('грамм', 'г').replace('г.', 'г').replace('гр', 'г').replace('грам', 'г')
    q = re.sub(r'(\d+)\s*к\b', lambda m: str(int(m.group(1)) * 1000), q)
    q = re.sub(r'(\d+)\s*тысяч', lambda m: str(int(m.group(1)) * 1000), q)
    q = re.sub(r'(\d+)\s*тыс', lambda m: str(int(m.group(1)) * 1000), q)
    return q


def extract_price_filters(query: str):
    query_lower = query.lower()
    min_price = None
    max_price = None

    min_match = re.search(r'(?:от|более|дороже|свыше)\s*(\d+)', query_lower)
    if min_match:
        min_price = int(min_match.group(1))

    max_match = re.search(r'(?:до|менее|дешевле)\s*(\d+)', query_lower)
    if max_match:
        max_price = int(max_match.group(1))

    return min_price, max_price

# Парсер
def extract_test_filter(query: str):
    q = query.lower().replace('грамм', 'г').replace('г.', 'г').replace('гр', 'г').replace('грам', 'г')

    min_test = None
    max_test = None

    # 1. "от X до Y г" — приоритет
    from_to_match = re.search(r'(?:от|свыше)\s*(\d+)\s*(?:до|–|-)\s*(\d+)\s*г?', q)
    if from_to_match:
        min_test = int(from_to_match.group(1))
        max_test = int(from_to_match.group(2))

    # 2. Диапазон X-Yг
    if min_test is None:
        range_match = re.search(r'(\d+)\s*[-–]\s*(\d+)\s*г?', q)
        if range_match:
            min_test = int(range_match.group(1))
            max_test = int(range_match.group(2))

    # 3. "до X г"
    if max_test is None:
        max_match = re.search(r'(?:до|максимум|max|не\s*более)\s*(\d+)\s*г', q)
        if max_match:
            max_test = int(max_match.group(1))

    # 4. "от X г"
    if min_test is None:
        min_match = re.search(r'(?:от|минимум|не\s*менее|свыше)\s*(\d+)\s*г', q)
        if min_match:
            min_test = int(min_match.group(1))

    # 5. "тест X г"
    if min_test is None and max_test is None:
        test_match = re.search(r'(?:тест|тестом|test)[\s:]*(\d+)', q)
        if test_match:
            val = int(test_match.group(1))
            min_test = val
            max_test = val + 20

    # 6. Просто "X г"
    if min_test is None and max_test is None:
        single_match = re.search(r'\b([1-9]\d{0,2})\s*г\b', q)
        if single_match:
            val = int(single_match.group(1))
            if val <= 300:
                min_test = val

    # Защита от цен
    if min_test and min_test > 300: min_test = None
    if max_test and max_test > 300: max_test = None

    return min_test, max_test

# Определяем на какую категорию намекает запрос
def detect_category_intent(query_lower: str) -> str | None:
    matches = []
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            pos = query_lower.find(kw)
            if pos >= 0:
                matches.append((pos, len(kw), category))
    if not matches:
        return None
    matches.sort(key=lambda x: (x[0], -x[1]))
    return matches[0][2]

# Парсинг по параметрам
def parse_query_params(query: str) -> dict:
    query_lower = _normalize_query(query)
    recognized = {
        'target_fish': None,
        'is_bank_fishing': False,
        'is_boat_fishing': False,
        'is_ultralight': False,
        'is_heavy': False,
        'is_budget': False,
        'is_premium': False,
        'category_intent': None,
        'test_min': None,
        'test_max': None,
        'min_price': None,
        'max_price': None,
    }
# Извлекаем тест
    min_test_req, max_test_req = extract_test_filter(query)
    recognized['test_min'] = min_test_req
    recognized['test_max'] = max_test_req
# Извлекаем цену
    min_price_match = re.search(
        r'(?:от|минимум|бюджет\s*от)\s*(\d+)(?=\s*(?:руб|бюджет|₽|рублей|руб\.|$))',
        query_lower,
    )
    if not min_price_match and 'не дороже' not in query_lower:
        min_price_match = re.search(
            r'дороже\s*(\d+)(?=\s*(?:руб|бюджет|₽|рублей|руб\.|$))',
            query_lower,
        )
    if min_price_match:
        recognized['min_price'] = int(min_price_match.group(1))

    max_price_match = re.search(
        r'(?:до|не\s*дороже|бюджет\s*до|максимум|дешевле)\s*(\d+)(?=\s*(?:руб|бюджет|₽|рублей|руб\.|$))',
        query_lower,
    )
    if max_price_match:
        recognized['max_price'] = int(max_price_match.group(1))
# Логика определения бюджета и премиум
    if any(w in query_lower for w in ['рубл', 'руб ', 'руб.', 'бюджет', '₽']) and \
       recognized['min_price'] is None and recognized['max_price'] is None:
        numbers = re.findall(r'\d+', query_lower)
        if numbers:
            last = int(numbers[-1])
            if last > 500:
                if 'не дороже' in query_lower or 'не более' in query_lower:
                    recognized['max_price'] = last
                elif any(w in query_lower for w in ['до', 'максимум', 'дешевле']):
                    recognized['max_price'] = last
                elif any(w in query_lower for w in ['от', 'минимум']) or (
                    'дороже' in query_lower and 'не дороже' not in query_lower
                ):
                    recognized['min_price'] = last
                elif 'в пределах' in query_lower or 'около' in query_lower:
                    recognized['max_price'] = int(last * 1.15)
                    recognized['min_price'] = int(last * 0.6)

    if any(w in query_lower for w in ['недорог', 'дешев', 'бюджетн', 'не разоряться', 'подешевле']):
        recognized['is_budget'] = True
        if recognized['max_price'] is None:
            recognized['max_price'] = 6000

    if any(w in query_lower for w in ['премиум', 'топов', 'флагман', 'лучший', 'качественн']):
        recognized['is_premium'] = True
        if recognized['min_price'] is None:
            recognized['min_price'] = 10000
# Определяем целевую рыбу
    for fish, forms in FISH_VARIATIONS.items():
        if any(form in query_lower for form in forms):
            recognized['target_fish'] = fish
            break
# Тип ловли
    if any(x in query_lower for x in ['береговая', 'с берега', 'берега', 'береговой', 'берегу', 'берег']):
        recognized['is_bank_fishing'] = True
    if any(x in query_lower for x in ['с лодки', 'с катера', 'с берега и лодки', 'на лодке', 'с лодки']):
        recognized['is_boat_fishing'] = True
# Стиль ловли
    if any(x in query_lower for x in ['ультралайт', 'ультра лайт', 'микроджиг', 'лайт', 'легк']):
        recognized['is_ultralight'] = True
    if any(x in query_lower for x in ['мощн', 'тяжел', 'трофей', 'крупн']):
        recognized['is_heavy'] = True

    recognized['category_intent'] = detect_category_intent(query_lower)
# Подсказки по тесту для конкретной рыбы
    if recognized['target_fish'] and recognized['test_min'] is None and recognized['test_max'] is None:
        hint = FISH_TEST_HINTS.get(recognized['target_fish'])
        if hint:
            recognized['test_min'], recognized['test_max'] = hint
# Корректировки для ультралайта и хэви
    if recognized['is_ultralight'] and recognized['test_max'] is None:
        recognized['test_min'] = recognized['test_min'] or 1
        recognized['test_max'] = min(recognized['test_max'] or 12, 12)
    if recognized['is_heavy'] and recognized['test_min'] is None:
        recognized['test_min'] = max(recognized['test_min'] or 15, 15)
        recognized['test_max'] = recognized['test_max'] or 60

    return recognized

# Добавляем товарам счетчик в зависимости от теста
def _apply_test_scoring(df: pd.DataFrame, recognized: dict) -> pd.DataFrame:
    t_min_req = recognized.get('test_min')
    t_max_req = recognized.get('test_max')

    if t_min_req is None and t_max_req is None:
        df['test_score'] = df['semantic_score'] * 3
        return df

    df['test_score'] = -18.0
    df.loc[df['test_min'].isna(), 'test_score'] = -65.0
# Логика счетчика в зависимости от того, что запрошено
    if t_min_req is not None and t_max_req is None:
        df['deviation'] = df['test_min'] - t_min_req
        ideal = (
            df['test_min'].notna()
            & (df['deviation'] >= -4) & (df['deviation'] <= 8)
            & (df['test_max'].isna() | (df['test_max'] >= t_min_req))
        )
        df.loc[ideal, 'test_score'] = 29.0
        good = (
            df['test_min'].notna()
            & (df['deviation'] >= -9)
            & (df['test_max'].isna() | (df['test_max'] >= t_min_req))
        )
        df.loc[good & (df['test_score'] < 0), 'test_score'] = 15.0
        df.loc[(df['test_min'].notna()) & (df['deviation'] < -9), 'test_score'] = -42.0
        df.loc[(df['test_min'].notna()) & (df['deviation'] > 13), 'test_score'] = -50.0

    elif t_max_req is not None and t_min_req is None:
        df.loc[(df['test_min'].notna()) & (df['test_min'] > t_max_req + 3), 'test_score'] = -62.0
        df.loc[(df['test_max'].notna()) & (df['test_max'] > t_max_req + 6), 'test_score'] = -58.0
        ideal = (
            (df['test_min'].notna())
            & (df['test_min'] <= t_max_req + 2)
            & (df['test_max'].isna() | (df['test_max'] <= t_max_req + 5))
        )
        df.loc[ideal, 'test_score'] = 30.0
        good = (
            (df['test_min'].notna())
            & (df['test_min'] <= t_max_req + 4)
            & (df['test_max'].isna() | (df['test_max'] <= t_max_req + 8))
        )
        df.loc[good & (df['test_score'] < 0), 'test_score'] = 16.0
        ok = (df['test_min'].notna()) & (df['test_min'] <= t_max_req + 6)
        df.loc[ok & (df['test_score'] < 0), 'test_score'] = 3.0

    else:
        ideal_range = (
            (df['test_min'].notna())
            & (df['test_min'] <= t_max_req)
            & (df['test_max'].isna() | (df['test_max'] >= t_min_req))
        )
        df.loc[ideal_range, 'test_score'] = 28.0
        good_range = (
            (df['test_min'].notna())
            & (df['test_min'] <= t_max_req + 5)
            & (df['test_max'].isna() | (df['test_max'] >= t_min_req - 5))
        )
        df.loc[good_range & (df['test_score'] < 0), 'test_score'] = 16.0
        weak = (df['test_min'].notna()) & (df['test_min'] <= t_max_req + 9)
        df.loc[weak & (df['test_score'] < 0), 'test_score'] = 4.0
        df.loc[(df['test_max'].notna()) & (df['test_max'] > t_max_req + 14), 'test_score'] = -47.0
        df.loc[(df['test_min'].notna()) & (df['test_min'] > t_max_req + 7), 'test_score'] = -45.0

    return df

# Обоснование, почему товар рекомендован
def _build_reason(row, recognized: dict) -> str:
    parts = []
    if pd.notna(row.get('test_min')):
        tmax = int(row['test_max']) if pd.notna(row.get('test_max')) else '∞'
        parts.append(f"Тест {int(row['test_min'])}–{tmax} г")
    else:
        parts.append("Подходит по описанию")

    if recognized.get('target_fish'):
        parts.append(f"для {recognized['target_fish']}")
    if recognized.get('is_bank_fishing'):
        parts.append("береговая ловля")
    if recognized.get('is_ultralight'):
        parts.append("ультралайт")
    if recognized.get('is_budget'):
        parts.append("бюджет")
    if recognized.get('min_price') is not None:
        parts.append(f"от {recognized['min_price']} ₽")
    if recognized.get('max_price') is not None:
        parts.append(f"до {recognized['max_price']} ₽")

    return " · ".join(parts)

# Семантический поиск
def semantic_search(query: str, top_k: int = 8, data_dir: Path = None):
    if data_dir is None:
        data_dir = Path("data")

    df = pd.read_csv(data_dir / "products_with_text.csv")
    embeddings = torch.load(data_dir / "product_embeddings.pt")

    model_emb = SentenceTransformer("BAAI/bge-m3")
    query_emb = model_emb.encode(query, convert_to_tensor=True).unsqueeze(0)

    semantic_scores = torch.nn.functional.cosine_similarity(
        query_emb, embeddings, dim=1
    ).cpu().numpy()

    df = df.copy()
    df['semantic_score'] = semantic_scores
    query_lower = _normalize_query(query)
    recognized = parse_query_params(query)
# Фильтрация по цене
    if recognized['min_price'] is not None:
        df = df[df['price'] >= recognized['min_price']].copy()
    if recognized['max_price'] is not None:
        df = df[df['price'] <= recognized['max_price']].copy()
# Фильтрация по категории
    if recognized['category_intent']:
        df = df[df['category'] == recognized['category_intent']].copy()
    elif any(k in query_lower for k in ['тест', 'от ', 'грамм', ' г', 'удилище', 'спиннинг', 'фидер', 'палка', 'удочка']):
        df = df[df['category'].str.contains('Спиннинг|Удилищ|Фидер|Карповые|Зимние', na=False, case=False)].copy()

    if df.empty:
        return [], recognized

    df = _apply_test_scoring(df, recognized)
# Бизнес-логика
    df['business_bonus'] = 0.0
    predator_fish = {'щука', 'окунь', 'судак', 'жерех', 'берш', 'налим'}
    peaceful_fish = {'карп', 'лещ', 'карась', 'язь'}

    if recognized['target_fish'] in predator_fish:
        df.loc[df['category'].str.contains('Спиннинг|Удилищ', na=False, case=False), 'business_bonus'] += 35.0
        df.loc[df['category'].str.contains('Воблер|Приманк|Блесн', na=False, case=False), 'business_bonus'] += 12.0
        df.loc[df['category'].str.contains('Фидер|Карповые|Прикорм', na=False, case=False), 'business_bonus'] -= 18.0
    elif recognized['target_fish'] in peaceful_fish:
        df.loc[df['category'].str.contains('Фидер|Карповые|Поплавк|Кормуш', na=False, case=False), 'business_bonus'] += 30.0
        df.loc[df['category'].str.contains('Спиннинг', na=False, case=False), 'business_bonus'] -= 10.0
    elif recognized['is_bank_fishing']:
        df.loc[df['category'].str.contains('Фидер', na=False, case=False), 'business_bonus'] += 28.0
        df.loc[df['category'].str.contains('Спиннинг|Удилищ', na=False, case=False), 'business_bonus'] -= 8.0

    if recognized['is_ultralight']:
        df.loc[(df['test_max'].notna()) & (df['test_max'] <= 15), 'business_bonus'] += 15.0
    if recognized['is_heavy']:
        df.loc[(df['test_min'].notna()) & (df['test_min'] >= 15), 'business_bonus'] += 15.0
    if recognized['is_premium']:
        df.loc[df['price'] >= 10000, 'business_bonus'] += 10.0
    if recognized['is_budget']:
        df.loc[df['price'] <= 6000, 'business_bonus'] += 10.0
        df.loc[df['price'] > 12000, 'business_bonus'] -= 12.0

    if recognized['category_intent']:
        df.loc[df['category'] == recognized['category_intent'], 'business_bonus'] += 20.0

    df['final_score'] = (
        df['semantic_score'] * 0.22
        + df['test_score'] * 9.0
        + df['business_bonus']
    )

    df = df.sort_values(by=['final_score', 'price'], ascending=[False, True]).head(top_k)

    results = []
    for _, row in df.iterrows():
        results.append({
            'name': row['name'],
            'price': float(row['price']),
            'category': row.get('category', ''),
            'test_min': row.get('test_min'),
            'test_max': row.get('test_max'),
            'reason': _build_reason(row, recognized),
        })

    return results, recognized

# Для тестирования
if __name__ == "__main__":
    results = semantic_search("Палка с тестом от 5 г", top_k=8)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['name']} | Цена: {r['price']} | Score: {r['score']:.4f}")

def _item_to_dict(row) -> dict:
    return {
        'id': int(row['id']) if pd.notna(row.get('id')) else None,
        'name': row['name'],
        'price': float(row['price']),
        'category': row.get('category', ''),
        'test_min': row.get('test_min'),
        'test_max': row.get('test_max'),
        'description': row.get('description', ''),
    }


def _select_accessories(df: pd.DataFrame, category: str, target_price: float, seed: int, count: int = 1):
    subset = df[df['category'] == category].copy()
    if subset.empty:
        return []

    ratio = 0.65 if category == 'Катушки' else 0.35
    ideal_price = max(target_price * ratio, 300)
    subset['fit_score'] = abs(subset['price'] - ideal_price) / max(ideal_price, 1)
    subset = subset.sort_values(['fit_score', 'price']).reset_index(drop=True)

    start = seed % max(1, len(subset) - count + 1)
    picked = subset.iloc[start:start + count]
    return [_item_to_dict(row) for _, row in picked.iterrows()]


# Рекомендации
def get_recommended_accessories(main_item, data_dir: Path = None):
    if data_dir is None:
        data_dir = Path("data")

    df = pd.read_csv(data_dir / "products_with_text.csv")
    category = str(main_item.get('category', '')).lower()
    price = float(main_item.get('price', 5000))
    seed = int(main_item.get('id', 1) or 1)

    kit = {}

    if 'спиннинг' in category or 'удилище' in category or 'зимн' in category:
        reels = _select_accessories(df, 'Катушки', price, seed, 1)
        if reels:
            kit["Рекомендуемая катушка"] = reels[0]

        lines = _select_accessories(df, 'Лески и шнуры', price, seed + 1, 1)
        if lines:
            kit["Шнур / леска"] = lines[0]

        lures = _select_accessories(df, 'Приманки', price, seed + 2, 2)
        if len(lures) == 1:
            kit["Приманки на хищника"] = lures[0]
        elif lures:
            kit["Приманки на хищника"] = lures

        wobblers = _select_accessories(df, 'Воблеры', price * 0.2, seed + 3, 1)
        if wobblers:
            kit["Воблер"] = wobblers[0]

        extras = _select_accessories(df, 'Аксессуары', price * 0.15, seed + 4, 1)
        if extras:
            kit["Аксессуар к комплекту"] = extras[0]

    elif 'фидер' in category or 'карпов' in category:
        reels = _select_accessories(df, 'Катушки', price, seed, 1)
        if reels:
            kit["Рекомендуемая катушка"] = reels[0]

        feeders = _select_accessories(df, 'Кормушки', price * 0.1, seed + 1, 1)
        if feeders:
            kit["Кормушка"] = feeders[0]

        bait = _select_accessories(df, 'Прикормка', price * 0.1, seed + 2, 1)
        if bait:
            kit["Прикормка"] = bait[0]

        lines = _select_accessories(df, 'Лески и шнуры', price * 0.2, seed + 3, 1)
        if lines:
            kit["Леска / шнур"] = lines[0]

    elif 'катуш' in category:
        rods = df[df['category'].isin(['Спиннинги', 'Фидеры', 'Карповые удилища'])].copy()
        if not rods.empty:
            rods['fit_score'] = abs(rods['price'] - price / 0.65)
            rod = rods.sort_values('fit_score').iloc[seed % len(rods)]
            kit["Подходящее удилище"] = _item_to_dict(rod)

    kit = {k: v for k, v in kit.items() if v is not None}
    return kit

# Функция возвращает товары, похожие на выбранный
def get_similar_products(item_name_or_id, top_k: int = 8, data_dir: Path = None):
    if data_dir is None:
        data_dir = Path("data")

    df = pd.read_csv(data_dir / "products_with_text.csv")
    embeddings = torch.load(data_dir / "product_embeddings.pt")

    # Поиск индекса выбранного товара
    if isinstance(item_name_or_id, str):
        # Ищем по имени
        mask = df['name'].str.contains(item_name_or_id, case=False, na=False)
        if not mask.any():
            return []
        idx = df[mask].index[0]
    else:
        # По id
        idx = df[df['id'] == item_name_or_id].index
        if len(idx) == 0:
            return []
        idx = idx[0]

    # Вычисляем схожесть
    item_emb = embeddings[idx].unsqueeze(0)
    similarity = torch.nn.functional.cosine_similarity(
        item_emb, embeddings, dim=1 ).cpu().numpy()

    main_row = df.loc[idx]
    main_category = main_row.get('category', '')
    main_price = float(main_row['price'])
    main_test_min = main_row.get('test_min')
    main_test_max = main_row.get('test_max')

    df_sim = df.copy()
    df_sim['similarity_score'] = similarity
    df_sim = df_sim.drop(index=idx)

    df_sim['category_bonus'] = np.where(df_sim['category'] == main_category, 0.12, 0.0)
    df_sim['price_penalty'] = abs(df_sim['price'] - main_price) / max(main_price, 500) * 0.08

    if pd.notna(main_test_min):
        df_sim['test_penalty'] = abs(df_sim['test_min'].fillna(main_test_min) - main_test_min) * 0.01
    else:
        df_sim['test_penalty'] = 0.0

    df_sim['final_similarity'] = (
        df_sim['similarity_score']
        + df_sim['category_bonus']
        - df_sim['price_penalty']
        - df_sim['test_penalty']
    )

    df_sim = df_sim.sort_values(by='final_similarity', ascending=False).head(top_k)

    results = []
    for _, row in df_sim.iterrows():
        reason_parts = [f"Схожесть {row['similarity_score']:.3f}"]
        if row['category'] == main_category:
            reason_parts.append("та же категория")
        if abs(row['price'] - main_price) <= main_price * 0.25:
            reason_parts.append("похожая цена")

        results.append({
            'name': row['name'],
            'price': float(row['price']),
            'category': row.get('category', ''),
            'test_min': row.get('test_min'),
            'test_max': row.get('test_max'),
            'score': float(row['final_similarity']),
            'reason': " · ".join(reason_parts),
        })
    return results