"""
Модуль для создания и работы с семантическими эмбеддингами товаров.
Автор: Гребцов Никита Юрьевич
Тема ВКР: Разработка интеллектуального помощника по подбору товаров
"""

import pandas as pd
import torch
from pathlib import Path
from sentence_transformers import SentenceTransformer



def create_product_embeddings(data_dir: Path, model_name: str = "BAAI/bge-m3"):
    print("Загрузка данных товаров")
    products_path = data_dir / "products.csv"
    
    if not products_path.exists():
        raise FileNotFoundError(f"Файл {products_path} не найден.")

    df = pd.read_csv(products_path)

    df['text_for_embedding'] = df.apply(
        lambda row: f"{row['name']}. {row['category']}. {row['description']} "
                    f"test_min_{row.get('test_min', 'nan')} "
                    f"test_max_{row.get('test_max', 'nan')}", axis=1)

    print(f"Загружено {len(df)} товаров. Генерация эмбеддингов с моделью {model_name}")

    model = SentenceTransformer(model_name)

    embeddings = model.encode(
        df['text_for_embedding'].tolist(), 
        show_progress_bar=True,
        convert_to_tensor=True
    )

    embeddings_path = data_dir / "product_embeddings.pt"
    torch.save(embeddings, embeddings_path)

    df.to_csv(data_dir / "products_with_text.csv", index=False)

    print(f"Эмбеддинги успешно созданы с моделью {model_name}")
    print(f"Размер эмбеддингов: {embeddings.shape}")

    return df, embeddings

# Загружает ранее сохранённые эмбеддинги и dataset
def load_embeddings(data_dir: Path):

    embeddings_path = data_dir / "product_embeddings.pt"
    products_path = data_dir / "products_with_text.csv"

    if not embeddings_path.exists() or not products_path.exists():
        raise FileNotFoundError("Эмбеддинги не найдены.")

    df = pd.read_csv(products_path)
    embeddings = torch.load(embeddings_path)

    print(f"Загружены {len(df)} товары и эмбеддинги размером {embeddings.shape}")
    return df, embeddings

# Для тестирования
if __name__ == "__main__":
    data_dir = Path("data")
    create_product_embeddings(data_dir)