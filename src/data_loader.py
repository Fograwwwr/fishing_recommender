"""
Загрузки данных для интеллектуального помощника по рыбалке
Автор: Гребцов Никита Юрьевич
Тема ВКР: Разработка интеллектуального помощника по подбору товаров
"""

import pandas as pd
from pathlib import Path

def load_products(data_dir: Path):
    """
    Загружает товары.
    """
    products_path = data_dir / "products.csv"
    
    if not products_path.exists():
        st_error = f"Файл {products_path} не найден."
        print(st_error)
        return None
    
    df = pd.read_csv(products_path)
    print(f"Загружено {len(df)} товаров из {products_path}")
    
    # Добавление id
    if 'id' not in df.columns:
        df = df.reset_index(drop=True)
        df.insert(0, 'id', df.index)          
        print("Добавлена колонка 'id' (автоматически по индексу)")
    
    # Приведение типов в числа 
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    if 'test_min' in df.columns:
        df['test_min'] = pd.to_numeric(df['test_min'], errors='coerce')
    if 'test_max' in df.columns:
        df['test_max'] = pd.to_numeric(df['test_max'], errors='coerce')
    
    # Сохранение обновлённого CSV
    df.to_csv(products_path, index=False, encoding='utf-8')
    print("CSV обновлён с колонкой 'id'")
    
    return df