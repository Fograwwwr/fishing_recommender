"""
Генерация и экспорт товаров .
"""

from __future__ import annotations

import json
import random
from pathlib import Path

import pandas as pd

TARGET_SIZE = 1000
RANDOM_SEED = 42

CATEGORY_QUOTAS = {
    "Спиннинги": 110,
    "Катушки": 110,
    "Фидеры": 55,
    "Карповые удилища": 45,
    "Зимние удочки": 35,
    "Воблеры": 90,
    "Приманки": 85,
    "Блесны": 55,
    "Балансиры": 35,
    "Мормышки": 30,
    "Лески и шнуры": 50,
    "Крючки": 45,
    "Поплавки": 35,
    "Кормушки": 35,
    "Прикормка": 30,
    "Одежда": 60,
    "Аксессуары": 90,
    "Инструменты": 35,
    "Палатки": 35,
    "Электроника": 20,
}

BRANDS = [
    "Shimano", "Daiwa", "Abu Garcia", "Rapala", "Salmo", "Norfin", "Lucky John",
    "Favorite", "Kosadaka", "Zemex", "Maximus", "Stinger", "Volzhanka", "Mikado",
    "Browning", "Fox", "Preston", "Maver", "Trabucco", "Owner", "Gamakatsu",
    "Mustad", "Keitech", "Mann's", "Berkley", "Mepps", "Blue Fox", "Pontoon21",
    "Jackall", "Megabass", "Okuma", "Ryobi", "Tsurinoya", "Graphiteleader",
]

SERIES = [
    "Pro", "Expert", "Master", "Sport", "Classic", "Ultra", "Power", "Light",
    "Elite", "Prime", "Force", "Strike", "Hunter", "River", "Lake", "Trophy",
]

COLORS = ["чёрный", "синий", "зелёный", "красный", "серебро", "золото", "натуральный"]
SIZES = ["S", "M", "L", "XL", "2XL", "3XL"]
WEIGHTS = [5, 7, 10, 12, 15, 18, 20, 25, 30, 40, 50, 60, 80, 100, 120, 150, 180]
LENGTHS = [180, 210, 240, 270, 300, 330, 360, 390, 420]
REEL_SIZES = [1000, 2000, 2500, 3000, 4000, 5000, 6000]
LURE_SIZES = [3.5, 4.5, 5.0, 6.5, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]


def _price(rng: random.Random, low: int, high: int) -> int:
    raw = rng.randint(low, high)
    return int(round(raw / 10) * 10)


def _pick(rng: random.Random, items: list):
    return items[rng.randrange(len(items))]


def _make_spinning(rng: random.Random, idx: int) -> dict:
    brand, series = _pick(rng, BRANDS), _pick(rng, SERIES)
    length = _pick(rng, LENGTHS)
    t_min = _pick(rng, [1, 2, 3, 5, 7, 10, 15])
    t_max = t_min + _pick(rng, [10, 15, 20, 25, 30])
    price = _price(rng, 2500, 32000)
    name = f"Спиннинг {brand} {series} {length}см {t_min}-{t_max}г S-{idx:04d}"
    return {
        "name": name,
        "description": f"Спиннинг {brand} серии {series} длиной {length} см, тест {t_min}-{t_max} г. Подходит для активной ловли хищника.",
        "price": price,
        "category": "Спиннинги",
        "test_min": t_min,
        "test_max": t_max,
    }


def _make_reel(rng: random.Random, idx: int) -> dict:
    brand, series = _pick(rng, BRANDS), _pick(rng, SERIES)
    size = _pick(rng, REEL_SIZES)
    price = _price(rng, 1800, 28000)
    name = f"Катушка {brand} {series} {size} R-{idx:04d}"
    return {
        "name": name,
        "description": f"Катушка {brand} {series} размера {size} с плавным ходом и надёжным фрикционом.",
        "price": price,
        "category": "Катушки",
    }


def _make_feeder(rng: random.Random, idx: int) -> dict:
    brand = _pick(rng, BRANDS)
    length = _pick(rng, LENGTHS[4:])
    t_max = _pick(rng, WEIGHTS[8:])
    price = _price(rng, 3500, 18000)
    name = f"Фидер {brand} Feeder {length} {t_max}г F-{idx:04d}"
    return {
        "name": name,
        "description": f"Фидерное удилище {brand} длиной {length} см с тестом до {t_max} г для дальнего заброса.",
        "price": price,
        "category": "Фидеры",
        "test_min": 0,
        "test_max": t_max,
    }


def _make_carp_rod(rng: random.Random, idx: int) -> dict:
    brand = _pick(rng, BRANDS)
    length = _pick(rng, [330, 360, 390, 396])
    t_max = _pick(rng, [100, 120, 130, 150, 180])
    price = _price(rng, 4500, 24000)
    name = f"Карповое удилище {brand} Carp {length} {t_max}г C-{idx:04d}"
    return {
        "name": name,
        "description": f"Карповое удилище {brand} длиной {length} см, тест до {t_max} г.",
        "price": price,
        "category": "Карповые удилища",
        "test_min": 0,
        "test_max": t_max,
    }


def _make_ice_rod(rng: random.Random, idx: int) -> dict:
    brand = _pick(rng, BRANDS)
    length = _pick(rng, [45, 50, 55, 60, 65, 70])
    t_min, t_max = _pick(rng, [1, 2, 4]), _pick(rng, [5, 8, 10])
    price = _price(rng, 690, 2500)
    name = f"Зимняя удочка {brand} Ice {length}см {t_min}-{t_max}г I-{idx:04d}"
    return {
        "name": name,
        "description": f"Зимняя удочка {brand} длиной {length} см для блеснения и ловли на мормышку.",
        "price": price,
        "category": "Зимние удочки",
        "test_min": t_min,
        "test_max": t_max,
    }


def _make_lure(rng: random.Random, idx: int, category: str, prefix: str) -> dict:
    brand = _pick(rng, BRANDS)
    size = _pick(rng, LURE_SIZES)
    color = _pick(rng, COLORS)
    price = _price(rng, 280, 2800)
    name = f"{prefix} {brand} {size}см {color} L-{idx:04d}"
    return {
        "name": name,
        "description": f"{prefix} {brand} длиной {size} см, цвет {color}. Уловистая приманка для хищной рыбы.",
        "price": price,
        "category": category,
    }


def _make_line(rng: random.Random, idx: int) -> dict:
    brand = _pick(rng, BRANDS)
    diameter = round(rng.uniform(0.08, 0.35), 2)
    length = _pick(rng, [100, 135, 150, 200])
    price = _price(rng, 320, 3200)
    name = f"Леска/шнур {brand} {diameter}мм {length}м N-{idx:04d}"
    return {
        "name": name,
        "description": f"Рыболовная леска или шнур {brand}, диаметр {diameter} мм, длина {length} м.",
        "price": price,
        "category": "Лески и шнуры",
    }


def _make_hook(rng: random.Random, idx: int) -> dict:
    brand = _pick(rng, ["Owner", "Gamakatsu", "Mustad", "Korda", "Kamasan"])
    num_str = _pick(rng, ["4", "6", "8", "10", "12", "2", "1", "1/0"])
    qty = _pick(rng, [10, 15, 20])
    price = _price(rng, 150, 650)
    name = f"Крючки {brand} №{num_str} ({qty} шт) H-{idx:04d}"
    return {
        "name": name,
        "description": f"Крючки {brand} номер {num_str}, упаковка {qty} шт. Острые и прочные.",
        "price": price,
        "category": "Крючки",
    }


def _make_float(rng: random.Random, idx: int) -> dict:
    brand = _pick(rng, BRANDS)
    weight = _pick(rng, [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 8.0])
    price = _price(rng, 120, 420)
    name = f"Поплавок {brand} {weight}г P-{idx:04d}"
    return {
        "name": name,
        "description": f"Поплавок {brand} грузоподъёмностью {weight} г для поплавочной ловли.",
        "price": price,
        "category": "Поплавки",
    }


def _make_feeder_basket(rng: random.Random, idx: int) -> dict:
    weight = _pick(rng, WEIGHTS[:10])
    ftype = _pick(rng, ["металлическая", "пластиковая", "методная", "пуля"])
    price = _price(rng, 140, 420)
    name = f"Кормушка {ftype} {weight}г B-{idx:04d}"
    return {
        "name": name,
        "description": f"Кормушка {ftype} весом {weight} г для фидерной ловли.",
        "price": price,
        "category": "Кормушки",
    }


def _make_bait_mix(rng: random.Random, idx: int) -> dict:
    brand = _pick(rng, BRANDS)
    fish = _pick(rng, ["лещ", "карп", "плотва", "карась", "фидер"])
    weight = _pick(rng, [1, 1.5, 2, 2.5])
    price = _price(rng, 280, 890)
    name = f"Прикормка {brand} {fish} {weight}кг M-{idx:04d}"
    return {
        "name": name,
        "description": f"Прикормка {brand} для ловли {fish}, фасовка {weight} кг.",
        "price": price,
        "category": "Прикормка",
    }


def _make_clothing(rng: random.Random, idx: int) -> dict:
    brand = _pick(rng, BRANDS)
    item = _pick(rng, ["костюм", "куртка", "брюки", "перчатки", "шапка", "сапоги", "жилет"])
    season = _pick(rng, ["зимний", "летний", "демисезонный"])
    size = _pick(rng, SIZES)
    price = _price(rng, 790, 28000)
    name = f"{season.capitalize()} {item} {brand} {size} CL-{idx:04d}"
    return {
        "name": name,
        "description": f"{season.capitalize()} {item} {brand}, размер {size}. Комфорт и защита на рыбалке.",
        "price": price,
        "category": "Одежда",
    }


def _make_accessory(rng: random.Random, idx: int) -> dict:
    brand = _pick(rng, BRANDS)
    item = _pick(rng, [
        "подсак", "садок", "ящик", "сумка", "чехол", "стойка", "сигнализатор",
        "багорик", "зажим", "поводки", "грузила", "карман", "органайзер",
    ])
    price = _price(rng, 250, 38000)
    name = f"{item.capitalize()} {brand} A-{idx:04d}"
    return {
        "name": name,
        "description": f"Рыболовный аксессуар: {item} {brand} для удобства и эффективной ловли.",
        "price": price,
        "category": "Аксессуары",
    }


def _make_tool(rng: random.Random, idx: int) -> dict:
    brand = _pick(rng, BRANDS)
    item = _pick(rng, ["ножницы", "плоскогубцы", "щипцы", "экстрактор", "мультитул", "зажим"])
    price = _price(rng, 220, 12500)
    name = f"{item.capitalize()} {brand} T-{idx:04d}"
    return {
        "name": name,
        "description": f"Рыболовный инструмент: {item} {brand} для монтажа и обслуживания снастей.",
        "price": price,
        "category": "Инструменты",
    }


def _make_tent(rng: random.Random, idx: int) -> dict:
    brand = _pick(rng, BRANDS)
    item = _pick(rng, ["палатка", "спальник", "кресло", "стол", "тент"])
    season = _pick(rng, ["зимняя", "летняя", "всесезонная"])
    price = _price(rng, 1800, 16000)
    name = f"{season.capitalize()} {item} {brand} TP-{idx:04d}"
    return {
        "name": name,
        "description": f"{season.capitalize()} {item} {brand} для комфортного отдыха на рыбалке.",
        "price": price,
        "category": "Палатки",
    }


def _make_electronics(rng: random.Random, idx: int) -> dict:
    brand = _pick(rng, ["Garmin", "Lowrance", "Humminbird", "Deeper", "Lucky", "Norfin"])
    item = _pick(rng, ["эхолот", "камера", "GPS-навигатор", "зарядное устройство"])
    price = _price(rng, 1900, 62000)
    name = f"{item.capitalize()} {brand} E-{idx:04d}"
    return {
        "name": name,
        "description": f"Электроника для рыбалки: {item} {brand} с современными функциями.",
        "price": price,
        "category": "Электроника",
    }


GENERATORS = {
    "Спиннинги": _make_spinning,
    "Катушки": _make_reel,
    "Фидеры": _make_feeder,
    "Карповые удилища": _make_carp_rod,
    "Зимние удочки": _make_ice_rod,
    "Воблеры": lambda r, i: _make_lure(r, i, "Воблеры", "Воблер"),
    "Приманки": lambda r, i: _make_lure(r, i, "Приманки", "Силикон"),
    "Блесны": lambda r, i: _make_lure(r, i, "Блесны", "Блесна"),
    "Балансиры": lambda r, i: _make_lure(r, i, "Балансиры", "Балансир"),
    "Мормышки": lambda r, i: _make_lure(r, i, "Мормышки", "Мормышка"),
    "Лески и шнуры": _make_line,
    "Крючки": _make_hook,
    "Поплавки": _make_float,
    "Кормушки": _make_feeder_basket,
    "Прикормка": _make_bait_mix,
    "Одежда": _make_clothing,
    "Аксессуары": _make_accessory,
    "Инструменты": _make_tool,
    "Палатки": _make_tent,
    "Электроника": _make_electronics,
}


def _normalize_product(product: dict) -> dict:
    item = {
        "name": str(product["name"]).strip(),
        "description": str(product.get("description", "")).strip(),
        "price": int(product["price"]),
        "category": str(product["category"]).strip(),
    }
    if "test_min" in product and product["test_min"] is not None and not pd.isna(product.get("test_min")):
        item["test_min"] = float(product["test_min"])
    if "test_max" in product and product["test_max"] is not None and not pd.isna(product.get("test_max")):
        item["test_max"] = float(product["test_max"])
    return item


def build_dataset(base_products: list[dict], target_size: int = TARGET_SIZE) -> pd.DataFrame:
    rng = random.Random(RANDOM_SEED)
    normalized = [_normalize_product(p) for p in base_products]
    seen_names = {p["name"] for p in normalized}
    by_category: dict[str, list[dict]] = {}
    for product in normalized:
        by_category.setdefault(product["category"], []).append(product)

    result = list(normalized)
    attempt = 0
    max_attempts = target_size * 20

    while len(result) < target_size and attempt < max_attempts:
        attempt += 1
        for category, quota in CATEGORY_QUOTAS.items():
            if len(result) >= target_size:
                break
            current = len(by_category.get(category, []))
            if current >= quota:
                continue
            generator = GENERATORS[category]
            candidate = _normalize_product(generator(rng, len(result) + attempt))
            if candidate["name"] in seen_names:
                continue
            seen_names.add(candidate["name"])
            result.append(candidate)
            by_category.setdefault(category, []).append(candidate)

    df = pd.DataFrame(result)
    df = df.drop_duplicates(subset=["name"], keep="first")
    if len(df) < target_size:
        raise RuntimeError(f"Не удалось сгенерировать {target_size} уникальных товаров, получено {len(df)}")

    df = df.head(target_size).reset_index(drop=True)
    df.insert(0, "id", range(1, len(df) + 1))
    return df


def add_embedding_text(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()
    enriched["text_for_embedding"] = enriched.apply(
        lambda row: (
            f"{row['name']}. {row['category']}. {row['description']} "
            f"test_min_{row.get('test_min', 'nan')} "
            f"test_max_{row.get('test_max', 'nan')}"
        ),
        axis=1,
    )
    return enriched


def export_dataset(df: pd.DataFrame, data_dir: Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    enriched = add_embedding_text(df)

    csv_path = data_dir / "products.csv"
    json_path = data_dir / "products.json"
    enriched_csv_path = data_dir / "products_with_text.csv"

    df.to_csv(csv_path, index=False, encoding="utf-8")
    enriched.to_csv(enriched_csv_path, index=False, encoding="utf-8")

    records = enriched.where(pd.notna(enriched), None).to_dict(orient="records")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return {
        "total": len(df),
        "csv": csv_path,
        "json": json_path,
        "with_text_csv": enriched_csv_path,
        "duplicate_names": int(df["name"].duplicated().sum()),
    }


def validate_dataset(df: pd.DataFrame, target_size: int = TARGET_SIZE) -> None:
    if len(df) != target_size:
        raise ValueError(f"Ожидалось {target_size} товаров, получено {len(df)}")
    if df["name"].duplicated().any():
        dupes = df[df["name"].duplicated(keep=False)]["name"].tolist()
        raise ValueError(f"Найдены дубликаты названий: {dupes[:5]}")