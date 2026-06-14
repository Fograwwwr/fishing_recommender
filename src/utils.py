"""
Оценочные функции для интеллектуального помощника, создание / обновление test_queries.json
Автор: Гребцов Никита Юрьевич
Тема ВКР: Разработка интеллектуального помощника по подбору товаров
"""

import json
import math
from pathlib import Path

import pandas as pd

from src.model import semantic_search

# Реальные запросы 
BASE_QUERIES = [
    # Удилища и тест
    "Палка с тестом от 5 г",
    "Палка с тестом от 5 г до 6000 рублей",
    "спиннинг тест 10-30г",
    "спиннинг с тестом от 10 г",
    "спиннинг с тестом от 2 г до 15 г",
    "нужна удочка на окуня недорогая",
    "что взять на щуку с берега до 8 тысяч",
    "посоветуй спиннинг на судака от 7000 рублей",
    "ищу лёгкий спиннинг для микроджига",
    "мощный спиннинг на трофейную щуку",
    "ультралайт палка на форель и окуня",
    "спиннинг на щуку с берега",
    "удилище для джига тест 7-28 г",
    "палка до 5 грамм бюджетная",
    "спиннинг не дороже 5000 руб",

    # Рыба + бюджет
    "На щуку тест от 5 до 20 г до 6000 рублей",
    "На судака тест от 7 до 28 г от 7000 руб",
    "Палка на окуня от 3 г",
    "что купить на жереха с берега",
    "снасти на голавля весной",
    "на карася и леща что посоветуешь",

    # Фидер и карп
    "фидер для реки недорогой",
    "карповое удилище до 15000",
    "фидерка на леща с кормушкой",
    "удочка для карпятника мощная",

    # Зима
    "зимняя удочка для блеснения окуня",
    "снасти для зимней ловли судака",

    # Катушки и оснастка
    "катушка для спиннинга до 6000",
    "безынерционка на ультралайт",
    "плетёнка для джига 150 метров",
    "воблеры на щуку недорогие",
    "силикон на судака",

    # Одежда и аксессуары
    "зимний костюм для рыбалки",
    "непромокаемые сапоги для рыбалки",
    "подсак для щуки",
    "эхолот недорогой для лодки",
]


def update_test_queries(data_dir: Path = None, top_k_relevant: int = 6):
    if data_dir is None:
        data_dir = Path("data")

    df = pd.read_csv(data_dir / "products.csv")
    name_to_id = dict(zip(df["name"], df["id"]))

    test_queries = []

    print("Обновление test_queries.json...")
    print(f"Используется {len(BASE_QUERIES)} запросов\n")

    for i, query in enumerate(BASE_QUERIES, 1):
        print(f"{i}. Обработка запроса: '{query}'")
        results, _ = semantic_search(query, top_k=10, data_dir=data_dir)

        relevant_ids = []
        for item in results[:top_k_relevant]:
            name = item.get("name")
            if name in name_to_id:
                relevant_ids.append(int(name_to_id[name]))

        test_queries.append({
            "query": query,
            "relevant_ids": relevant_ids,
        })

        print(f"Добавлено {len(relevant_ids)} релевантных товаров")

    test_path = data_dir / "test_queries.json"
    with open(test_path, "w", encoding="utf-8") as f:
        json.dump(test_queries, f, ensure_ascii=False, indent=2)

    print(f"\ntest_queries.json успешно обновлён ({len(test_queries)} запросов)")
    print(f"Файл сохранён: {test_path}")
    return test_queries

# Вычисляем положение релевантных результатов 
def _dcg(relevances: list[int]) -> float:
    return sum(rel / math.log2(i + 2) for i, rel in enumerate(relevances))

# Показывает, насколько хорошо ранжированы релевантные товары в топе 
def _ndcg_at_k(retrieved_ids: list[int], relevant_ids: set[int], k: int = 5) -> float:
    relevances = [1 if rid in relevant_ids else 0 for rid in retrieved_ids[:k]]
    ideal = sorted(relevances, reverse=True)
    ideal_dcg = _dcg(ideal)
    if ideal_dcg == 0:
        return 0.0
    return _dcg(relevances) / ideal_dcg

# Вычисляем точность на каждой позиции
def _average_precision(retrieved_ids: list[int], relevant_ids: set[int]) -> float:
    if not relevant_ids:
        return 0.0
    score = 0.0
    hits = 0
    for i, rid in enumerate(retrieved_ids, 1):
        if rid in relevant_ids:
            hits += 1
            score += hits / i
    return score / len(relevant_ids)

# Функция оценки 
def compute_retrieval_metrics(data_dir: Path = None):
    if data_dir is None:
        data_dir = Path("data")

    df = pd.read_csv(data_dir / "products.csv")
    name_to_id = dict(zip(df["name"], df["id"]))

    test_path = data_dir / "test_queries.json"
    with open(test_path, "r", encoding="utf-8") as f:
        test_queries = json.load(f)

    print(f"Загружено {len(test_queries)} тестовых запросов")
    print(f"Всего товаров в датасете: {len(df)}")

    metrics = {
        "Precision@5": [],
        "Recall@5": [],
        "NDCG@5": [],
        "MAP": [],
        "MRR": [],
    }

    for idx, test in enumerate(test_queries):
        query = test["query"]
        relevant_ids = set(test.get("relevant_ids", []))

        print(f"\nТест {idx + 1}: '{query}'")
        print(f"  Ожидаемые ID ({len(relevant_ids)}): {sorted(relevant_ids)[:8]}{'...' if len(relevant_ids) > 8 else ''}")

        results, recognized = semantic_search(query, top_k=10, data_dir=data_dir)

        retrieved_ids = []
        for item in results:
            name = item.get("name")
            if name in name_to_id:
                rid = int(name_to_id[name])
                retrieved_ids.append(rid)
                print(f"  Найден: ID {rid} | {name[:70]}")

        if not retrieved_ids:
            print("  Ничего не найдено!")

        if recognized.get("target_fish"):
            print(f"  Распознано: рыба={recognized['target_fish']}", end="")
            if recognized.get("test_min") or recognized.get("test_max"):
                print(f", тест={recognized.get('test_min')}-{recognized.get('test_max')} г", end="")
            if recognized.get("max_price"):
                print(f", бюджет до {recognized['max_price']} ₽", end="")
            print()
        # Расчёт метрик
        top5 = set(retrieved_ids[:5])
        prec5 = len(top5 & relevant_ids) / 5 if relevant_ids else 0
        rec5 = len(top5 & relevant_ids) / len(relevant_ids) if relevant_ids else 0
        ndcg5 = _ndcg_at_k(retrieved_ids, relevant_ids, k=5)
        ap = _average_precision(retrieved_ids, relevant_ids)

        mrr = 0.0
        for rank, rid in enumerate(retrieved_ids, 1):
            if rid in relevant_ids:
                mrr = 1.0 / rank
                break

        metrics["Precision@5"].append(prec5)
        metrics["Recall@5"].append(rec5)
        metrics["NDCG@5"].append(ndcg5)
        metrics["MAP"].append(ap)
        metrics["MRR"].append(mrr)

        print(
            f"  Precision@5={prec5:.3f} | Recall@5={rec5:.3f} | "
            f"NDCG@5={ndcg5:.3f} | MAP={ap:.3f} | MRR={mrr:.3f}"
        )
    # Итоговые средние значения
    final_metrics = {k: round(sum(v) / len(v), 3) for k, v in metrics.items() if v}

    print("\n" + "=" * 60)
    print("ИТОГОВЫЕ МЕТРИКИ КАЧЕСТВА МОДЕЛИ:")
    for k, v in final_metrics.items():
        print(f"{k:15} = {v}")

    return final_metrics


if __name__ == "__main__":
    print("Запуск оценки метрик качества модели")
    print("=" * 60)

    update_test_queries()
    metrics = compute_retrieval_metrics()

    print("\nМетрики успешно рассчитаны!")
    for metric, value in metrics.items():
        print(f"   {metric:20} = {value:.3f}")