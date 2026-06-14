"""
Каталог товаров: группировка категорий и карточки товаров.
"""

from pathlib import Path
import pandas as pd
# Константы
CATEGORY_GROUPS = {
    "Удилища": [
        "Спиннинги", "Фидеры", "Карповые удилища", "Зимние удочки",
    ],
    "Снасти": [
        "Катушки", "Приманки", "Воблеры", "Блесны", "Лески и шнуры",
        "Крючки", "Кормушки", "Прикормка", "Поплавки", "Балансиры",
        "Мормышки", "Инструменты", "Электроника",
    ],
    "Одежда и экипировка": [
        "Одежда", "Аксессуары", "Палатки",
    ],
}

GROUP_IMAGES = {
    "Удилища": "rods.svg",
    "Снасти": "tackle.svg",
    "Одежда и экипировка": "clothing.svg",
}

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets" / "images"


def get_group_for_category(category: str) -> str:
    for group, categories in CATEGORY_GROUPS.items():
        if category in categories:
            return group
    return "Снасти"


def get_image_path(category: str) -> Path:
    group = get_group_for_category(category)
    filename = GROUP_IMAGES.get(group, "default.svg")
    return ASSETS_DIR / filename


def truncate_text(text: str, max_len: int = 120) -> str:
    if not text or pd.isna(text):
        return ""
    text = str(text).strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rsplit(" ", 1)[0] + "..."

# Форматирование информации
def format_test_info(item: dict) -> str:
    t_min = item.get("test_min")
    t_max = item.get("test_max")
    if pd.isna(t_min) and pd.isna(t_max):
        return ""
    if pd.notna(t_min) and pd.notna(t_max):
        return f"Тест: {int(t_min) if t_min == int(t_min) else t_min}–{int(t_max) if t_max == int(t_max) else t_max} г"
    if pd.notna(t_min):
        return f"Тест: от {int(t_min) if t_min == int(t_min) else t_min} г"
    if pd.notna(t_max):
        return f"Тест: до {int(t_max) if t_max == int(t_max) else t_max} г"
    return ""


def load_catalog(data_dir: Path) -> pd.DataFrame:
    path = data_dir / "products.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["group"] = df["category"].apply(get_group_for_category)
    return df


def filter_catalog(
    df: pd.DataFrame,
    group: str | None = None,
    category: str | None = None,
    search_text: str | None = None,) -> pd.DataFrame:
    result = df.copy()
    if group and group != "Все":
        result = result[result["group"] == group]
    if category and category != "Все":
        result = result[result["category"] == category]
    if search_text:
        q = search_text.lower().strip()
        mask = (
            result["name"].str.lower().str.contains(q, na=False)
            | result["description"].str.lower().str.contains(q, na=False)
            | result["category"].str.lower().str.contains(q, na=False)
        )
        result = result[mask]
    return result


def get_categories_for_group(df: pd.DataFrame, group: str | None) -> list[str]:
    if group and group != "Все":
        subset = df[df["group"] == group]
    else:
        subset = df
    return sorted(subset["category"].dropna().unique().tolist())


DEFAULT_PER_PAGE = 12
PER_PAGE_OPTIONS = [8, 12, 16, 24]

# Разбитие даатасета на страницы
def paginate_dataframe(df: pd.DataFrame, page: int, per_page: int) -> tuple[pd.DataFrame, int, int]:
    total = len(df)
    if total == 0:
        return df, 1, 0
    total_pages = max(1, (total + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page
    return df.iloc[start:end].copy(), total_pages, total


def row_to_cart_item(row) -> dict:
    return {
        "id": int(row["id"]) if pd.notna(row.get("id")) else None,
        "name": row["name"],
        "price": float(row["price"]),
        "category": row.get("category", ""),
        "test_min": row.get("test_min"),
        "test_max": row.get("test_max"),
        "description": row.get("description", ""),
    }