"""
Модель для прототипа Streamlit
Автор: Гребцов Никита Юрьевич
Тема ВКР: Разработка интеллектуального помощника по подбору товаров
"""

import torch
import pandas as pd
import re
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Достает фильтры по цене
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
    query_lower = query.lower()

  # Распознавание параметров
    recognized = {
        'target_fish': None,
        'is_bank_fishing': False,
        'test_min': None,
        'test_max': None,
        'min_price': None,
        'max_price': None
    }

    query_lower = query.lower()

    # 1 ТЕСТ 
    min_test_req, max_test_req = extract_test_filter(query)
    if min_test_req is not None or max_test_req is not None:
        recognized['test_min'] = min_test_req
        recognized['test_max'] = max_test_req

    # 2 ЦЕНА
    min_price_match = re.search(
        r'(?:от|минимум|не\s*дешевле|бюджет\s*от)\s*(\d+)(?=\s*(?:руб|бюджет|₽|рублей|руб\.|$))',
        query_lower
    )
    if min_price_match:
        recognized['min_price'] = int(min_price_match.group(1))

    max_price_match = re.search(
        r'(?:до|не\s*дороже|бюджет\s*до|максимум)\s*(\d+)(?=\s*(?:руб|бюджет|₽|рублей|руб\.|$))',
        query_lower
    )
    if max_price_match:
        recognized['max_price'] = int(max_price_match.group(1))

    
    if any(word in query_lower for word in ['рубл', 'руб ', 'руб.', 'бюджет', '₽']) and \
       recognized['min_price'] is None and recognized['max_price'] is None:
        numbers = re.findall(r'\d+', query_lower)
        if numbers:
            last = int(numbers[-1])
            if last > 500:
                if 'от' in query_lower or 'минимум' in query_lower:
                    recognized['min_price'] = last
                elif 'до' in query_lower or 'максимум' in query_lower:
                    recognized['max_price'] = last

    # 3. Целевая рыба
    fish_variations = {
        'щука': ['щука', 'щуку', 'щуки', 'на щуку', 'для щуки'],
        'окунь': ['окунь', 'окуня', 'окуни', 'на окуня', 'для окуня'],
        'судак': ['судак', 'судака', 'судаку', 'на судака'],
        'жерех': ['жерех', 'жереха', 'на жереха'],
        'голавль': ['голавль', 'голавля', 'на голавля'],
        'берш': ['берш', 'берша', 'на берша'],
        'сом': ['сом', 'сома', 'на сома'],
        'налим': ['налим', 'налима', 'на налима'],
        'язь': ['язь', 'язя', 'на язя']
    }
    for fish, forms in fish_variations.items():
        if any(form in query_lower for form in forms):
            recognized['target_fish'] = fish
            break

    # 4. Береговая ловля
    if any(x in query_lower for x in ['береговая', 'с берега', 'берега', 'береговой', 'берегу', 'берег']):
        recognized['is_bank_fishing'] = True

    # Фильтры по цене
    if recognized['min_price'] is not None:
        df = df[df['price'] >= recognized['min_price']].copy()

    if recognized['max_price'] is not None:
        df = df[df['price'] <= recognized['max_price']].copy()

    # Фильтр по категория
    if any(k in query_lower for k in ['тест', 'от ', 'грамм', 'г ', 'удилище', 'спиннинг', 'фидер', 'палка']):
        df = df[df['category'].str.contains('Спиннинг|Удилищ|Фидер|Карповые', na=False, case=False)]

    # Логика по тесту
    if recognized.get('test_min') is not None or recognized.get('test_max') is not None:
        df['test_score'] = -18.0                    
        df.loc[df['test_min'].isna(), 'test_score'] = -65.0

        t_min_req = recognized.get('test_min')
        t_max_req = recognized.get('test_max')

        # 1 только от X г 
        if t_min_req is not None and t_max_req is None:
            df['deviation'] = df['test_min'] - t_min_req
            ideal = (df['test_min'].notna() & 
                    (df['deviation'] >= -4) & (df['deviation'] <= 8) &
                    (df['test_max'].isna() | (df['test_max'] >= t_min_req)))
            df.loc[ideal, 'test_score'] = 29.0

            good = (df['test_min'].notna() & 
                   (df['deviation'] >= -9) &
                   (df['test_max'].isna() | (df['test_max'] >= t_min_req)))
            df.loc[good & (df['test_score'] < 0), 'test_score'] = 15.0

            df.loc[(df['test_min'].notna()) & (df['deviation'] < -9), 'test_score'] = -42.0
            df.loc[(df['test_min'].notna()) & (df['deviation'] > 13), 'test_score'] = -50.0

        # 2 Только до X г 
        elif t_max_req is not None and t_min_req is None:
            # штрафы за превышение
            df.loc[(df['test_min'].notna()) & (df['test_min'] > t_max_req + 3), 'test_score'] = -62.0
            df.loc[(df['test_max'].notna()) & (df['test_max'] > t_max_req + 6), 'test_score'] = -58.0

            # Идеально
            ideal = (df['test_min'].notna()) & \
                    (df['test_min'] <= t_max_req + 2) & \
                    (df['test_max'].isna() | (df['test_max'] <= t_max_req + 5))
            df.loc[ideal, 'test_score'] = 30.0

            # Хорошо
            good = (df['test_min'].notna()) & \
                   (df['test_min'] <= t_max_req + 4) & \
                   (df['test_max'].isna() | (df['test_max'] <= t_max_req + 8))
            df.loc[good & (df['test_score'] < 0), 'test_score'] = 16.0

            # Слабо, но приемлемо
            ok = (df['test_min'].notna()) & (df['test_min'] <= t_max_req + 6)
            df.loc[ok & (df['test_score'] < 0), 'test_score'] = 3.0

        # 3 Диапазон X-Y г
        else:
            ideal_range = (df['test_min'].notna()) & \
                         (df['test_min'] <= t_max_req) & \
                         (df['test_max'].isna() | (df['test_max'] >= t_min_req))
            df.loc[ideal_range, 'test_score'] = 28.0

            good_range = (df['test_min'].notna()) & \
                        (df['test_min'] <= t_max_req + 5) & \
                        (df['test_max'].isna() | (df['test_max'] >= t_min_req - 5))
            df.loc[good_range & (df['test_score'] < 0), 'test_score'] = 16.0

            weak = (df['test_min'].notna()) & (df['test_min'] <= t_max_req + 9)
            df.loc[weak & (df['test_score'] < 0), 'test_score'] = 4.0

            # Штрафы за выход из диапазона
            df.loc[(df['test_max'].notna()) & (df['test_max'] > t_max_req + 14), 'test_score'] = -47.0
            df.loc[(df['test_min'].notna()) & (df['test_min'] > t_max_req + 7), 'test_score'] = -45.0
    else:
        df['test_score'] = df['semantic_score'] * 3

    # Бонусы
    df['business_bonus'] = 0.0

    if recognized['target_fish']:
        df.loc[df['category'].str.contains('Спиннинг|Удилищ', na=False, case=False), 'business_bonus'] += 35.0
        df.loc[df['category'].str.contains('Фидер|Карповые', na=False, case=False), 'business_bonus'] -= 20.0

    elif recognized['is_bank_fishing']:
        df.loc[df['category'].str.contains('Фидер', na=False, case=False), 'business_bonus'] += 28.0
        df.loc[df['category'].str.contains('Спиннинг|Удилищ', na=False, case=False), 'business_bonus'] -= 12.0

    # Счет
    df['final_score'] = (
        df['semantic_score'] * 0.18 +   
        df['test_score'] * 9.0 +        
        df['business_bonus']
    )

    df = df.sort_values(by=['final_score', 'price'], ascending=[False, True]).head(top_k)

    # Результаты
    results = []
    for _, row in df.iterrows():
        if min_test_req is not None and pd.notna(row.get('test_min')):
            reason = f"Тест {int(row['test_min'])}–{int(row.get('test_max', 999))} г — идеально"
        else:
            reason = "Отлично подходит по описанию"
        
        if recognized['target_fish']:
            reason += f" + для {recognized['target_fish']}"
        if recognized['is_bank_fishing']:
            reason += " + береговая ловля"
        if recognized['min_price'] is not None:
            reason += f" (от {recognized['min_price']} ₽)"
        if recognized['max_price'] is not None:
            reason += f" (до {recognized['max_price']} ₽)"

        results.append({
            'name': row['name'],
            'price': float(row['price']),
            'category': row.get('category', ''),
            'test_min': row.get('test_min'),
            'test_max': row.get('test_max'),
            'reason': reason
        })

    return results, recognized

# Для тестирования
if __name__ == "__main__":
    results = semantic_search("Палка с тестом от 5 г", top_k=8)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['name']} | Цена: {r['price']} | Score: {r['score']:.4f}")

# Рекомендации 
def get_recommended_accessories(main_item, data_dir: Path = None):
    if data_dir is None:
        data_dir = Path("data")

    df = pd.read_csv(data_dir / "products_with_text.csv")
    category = str(main_item.get('category', '')).lower()

    kit = {}

    if 'спиннинг' in category or 'удилище' in category:
        # Случайная катушка из 5 самых подходящих по цене 
        cat_recs = df[df['category'] == 'Катушки']
        if not cat_recs.empty:
            kit["Рекомендуемая катушка"] = cat_recs.sample(n=1, random_state=None).to_dict('records')[0]

        # Шнур / леска
        line_recs = df[df['category'] == 'Лески и шнуры']
        if not line_recs.empty:
            kit["Шнур / леска"] = line_recs.sample(n=1, random_state=None).to_dict('records')[0]

        # Приманки на хищника 2 шт
        lure_recs = df[df['category'] == 'Приманки']
        if not lure_recs.empty:
            kit["Приманки на хищника"] = lure_recs.sample(n=2, random_state=None).to_dict('records')

    elif 'фидер' in category or 'карпов' in category:
        # Для фидеров 
        if not df[df['category'] == 'Катушки'].empty:
            kit["Рекомендуемая катушка"] = df[df['category'] == 'Катушки'].sample(n=1, random_state=None).to_dict('records')[0]
        if not df[df['category'] == 'Кормушки'].empty:
            kit["Кормушка"] = df[df['category'] == 'Кормушки'].sample(n=1, random_state=None).to_dict('records')[0]
        if not df[df['category'] == 'Прикормка'].empty:
            kit["Прикормка"] = df[df['category'] == 'Прикормка'].sample(n=1, random_state=None).to_dict('records')[0]

    
    kit = {k: v for k, v in kit.items() if v is not None}
    return kit

# Похожие товары, функция возвращает товары, похожие на выбранный
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

    # Создаём массив с результатами
    df_sim = df.copy()
    df_sim['similarity_score'] = similarity
    df_sim = df_sim.drop(index=idx)                    

    # Сортируем и берём k
    df_sim = df_sim.sort_values(by='similarity_score', ascending=False).head(top_k)

    results = []
    for _, row in df_sim.iterrows():
        results.append({
            'name': row['name'],
            'price': float(row['price']),
            'category': row.get('category', ''),
            'test_min': row.get('test_min'),
            'test_max': row.get('test_max'),
            'score': float(row['similarity_score']),
            'reason': f"Схожесть {row['similarity_score']:.3f}"
        })
    return results