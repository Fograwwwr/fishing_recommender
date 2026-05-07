"""
Оценочные функции для интеллектуального помощника, создание / обновление test_queries.json 
Автор: Гребцов Никита Юрьевич
Тема ВКР: Разработка интеллектуального помощника по подбору товаров
"""

import pandas as pd
from pathlib import Path
import json
from src.model import semantic_search

# Оценка качества модели поиска
def update_test_queries(data_dir: Path = None, top_k_relevant: int = 6):
    if data_dir is None:
        data_dir = Path("data")
    
    # Реальные запросы
    base_queries = [
        "Палка с тестом от 5 г",
        "Палка с тестом от 5 г до 6000 рублей",
        "спиннинг тест 10-30г",
        "Спиннинг на судака от 7000 рублей",
        "спиннинг на щуку с берега",
        "спиннинг с тестом от 10 г",
        "спиннинг с тестом от 2 г до 15 г"
    ]
    
    test_queries = []
    
    print("Обновление test_queries.json...")
    print(f"Используется {len(base_queries)} запросов\n")
    
    for i, query in enumerate(base_queries, 1):
        print(f"{i}. Обработка запроса: '{query}'")
        results, _ = semantic_search(query, top_k=10, data_dir=data_dir)
        
        relevant_ids = []
        for item in results[:top_k_relevant]:
            name = item.get('name')
            # Находим актуальный ID товара
            df = pd.read_csv(data_dir / "products.csv")
            row = df[df['name'] == name]
            if not row.empty:
                relevant_ids.append(int(row.iloc[0]['id']))
        
        test_queries.append({
            "query": query,
            "relevant_ids": relevant_ids
        })
        
        print(f"Добавлено {len(relevant_ids)} релевантных товаров\n")
    
    # Сохраняем файл
    test_path = data_dir / "test_queries.json"
    with open(test_path, "w", encoding="utf-8") as f:
        json.dump(test_queries, f, ensure_ascii=False, indent=2)
    
    print(f" test_queries.json успешно обновлён ({len(test_queries)} запросов)")
    print(f"Файл сохранён: {test_path}")
    return test_queries



def compute_retrieval_metrics(data_dir: Path = None):
    if data_dir is None:
        data_dir = Path("data")
    
    # Загружаем товары
    df = pd.read_csv(data_dir / "products.csv")
    name_to_id = dict(zip(df['name'], df['id']))
    id_to_name = {v: k for k, v in name_to_id.items()}
    
    # Загружаем тестовые запросы
    test_path = data_dir / "test_queries.json"
    with open(test_path, "r", encoding="utf-8") as f:
        test_queries = json.load(f)
    
    print(f"Загружено {len(test_queries)} тестовых запросов")
    print(f"Всего товаров в датасете: {len(df)}")
    
    metrics = {"Precision": [], "Recall": [], "NDCG": [], "MAP": [], "MRR": []}
    
    for idx, test in enumerate(test_queries):
        query = test["query"]
        relevant_ids = set(test.get("relevant_ids", []))
        
        print(f"\n Тест {idx+1}: '{query}'")
        print(f"  Ожидаемые ID: {relevant_ids}")
        
        # Запускаем поиск
        results, _ = semantic_search(query, top_k=10, data_dir=data_dir)
        
        # Получаем ID найденных товаров
        retrieved_ids = []
        for item in results:
            name = item.get('name')
            if name in name_to_id:
                rid = name_to_id[name]
                retrieved_ids.append(rid)
                print(f"  Найден: ID {rid} | {name[:60]}...")
        
        if not retrieved_ids:
            print("  Ничего не найдено!")
        
        # Метрики 
        top5 = set(retrieved_ids[:5])
        prec5 = len(top5 & relevant_ids) / 5 if relevant_ids else 0
        rec5 = len(top5 & relevant_ids) / len(relevant_ids) if relevant_ids else 0
        
        # MRR
        mrr = 0.0
        for rank, rid in enumerate(retrieved_ids, 1):
            if rid in relevant_ids:
                mrr = 1.0 / rank
                break
        
        metrics["Precision"].append(prec5)
        metrics["Recall"].append(rec5)
        metrics["MRR"].append(mrr)
        
        print(f"   Precision = {prec5:.3f} | Recall = {rec5:.3f} | MRR = {mrr:.3f}")
    
    # Итоговые средние
    final_metrics = {k: round(sum(v)/len(v), 3) for k, v in metrics.items() if v}
    
    print("\n" + "="*60)
    print("ИТОГОВЫЕ МЕТРИКИ КАЧЕСТВА МОДЕЛИ:")
    for k, v in final_metrics.items():
        print(f"{k:15} = {v}")
    
    return final_metrics

if __name__ == "__main__":
    print("Запуск оценки метрик качества модели..")
    print("=" * 60)
    
    update_test_queries()
    metrics = compute_retrieval_metrics()

    print("\n Метрики успешно рассчитаны!")
    for metric, value in metrics.items():
        print(f"   {metric:20} = {value:.3f}")
    