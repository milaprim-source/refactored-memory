"""
База знаний по физике для 10 класса на основе предоставленного документа
"""

physics_knowledge = {
    "mechanics": {
        "title": "Механика",
        "description": "Раздел физики, изучающий механическое движение тел",
        "topics": {
            "newton_laws": {
                "title": "Законы Ньютона",
                "first_law": {
                    "name": "I закон (Закон инерции)",
                    "description": "Любое тело будет оставаться в состоянии покоя или двигаться равномерно и прямолинейно, если на него не действуют внешние силы.",
                    "formula": "V = const ⟺ ∑F = 0",
                    "examples": "велосипед, бегун, чай в кружке, дверь"
                },
                "second_law": {
                    "name": "II закон (Основной закон классической механики)",
                    "description": "В инерциальной системе отсчета ускорение прямо пропорционально равнодействующей всех сил и обратно пропорционально массе тела.",
                    "formula": "a = F/m",
                    "notes": "Сила - причина ускорения, масса - мера инертности"
                },
                "third_law": {
                    "name": "III закон (Закон взаимодействия)",
                    "description": "Тела действуют друг на друга с силами, равными по модулю и противоположными по направлению.",
                    "formula": "F₁₂ = -F₂₁",
                    "examples": "притяжение Земли, удар боксера, ноутбук на столе"
                }
            },
            "gravity": {
                "title": "Закон всемирного тяготения",
                "description": "Все тела во Вселенной взаимно притягиваются друг к другу",
                "formula": "F = G(m₁m₂/R²)",
                "constant": "G = 6,67×10⁻¹¹ Н·м²/кг²"
            },
            "conservation": {
                "title": "Законы сохранения",
                "momentum": {
                    "name": "Закон сохранения импульса",
                    "description": "Сумма импульсов всех тел системы постоянна, если сумма внешних сил равна нулю",
                    "formula": "m₁v₁ + m₂v₂ = const"
                },
                "energy": {
                    "name": "Закон сохранения энергии",
                    "description": "Энергия не возникает и не исчезает, она переходит из одного вида в другой",
                    "formula": "Ек + Еп = const"
                }
            }
        }
    },
    "mkt": {
        "title": "МКТ и термодинамика",
        "description": "Молекулярно-кинетическая теория и термодинамика",
        "topics": {
            "gas_laws": {
                "title": "Газовые законы",
                "mendeleev_clapeyron": {
                    "name": "Уравнение Менделеева-Клапейрона",
                    "formula": "PV = νRT",
                    "R": "8,314 Дж/(моль·К)"
                },
                "isothermal": {
                    "name": "Изотермический процесс",
                    "formula": "PV = const",
                    "condition": "T = const"
                },
                "isobaric": {
                    "name": "Изобарный процесс",
                    "formula": "V/T = const",
                    "condition": "P = const"
                },
                "isochoric": {
                    "name": "Изохорный процесс",
                    "formula": "P/T = const",
                    "condition": "V = const"
                }
            },
            "thermodynamics": {
                "title": "Первый закон термодинамики",
                "description": "Количество теплоты идет на изменение внутренней энергии и совершение работы",
                "formula": "Q = ∆U + A"
            }
        }
    }
}

def search_knowledge(query):
    """Поиск информации в базе знаний по запросу"""
    results = []
    query = query.lower()
    
    # Прямой поиск по ключевым словам
    keywords = {
        "ньютон": ["newton_laws"],
        "инерция": ["newton_laws", "first_law"],
        "импульс": ["conservation", "momentum"],
        "энергия": ["conservation", "energy"],
        "тяготение": ["gravity"],
        "газ": ["gas_laws"],
        "изотерма": ["gas_laws", "isothermal"],
        "изобара": ["gas_laws", "isobaric"],
        "изохора": ["gas_laws", "isochoric"],
        "термодинамик": ["thermodynamics"],
        "менделеев": ["gas_laws", "mendeleev_clapeyron"],
        "клапейрон": ["gas_laws", "mendeleev_clapeyron"]
    }
    
    # Проверяем ключевые слова
    for keyword, paths in keywords.items():
        if keyword in query:
            for section in physics_knowledge.values():
                for topic_key, topic in section.get("topics", {}).items():
                    if topic_key in paths:
                        results.append(format_topic_info(topic))
    
    # Если ничего не найдено, ищем по заголовкам
    if not results:
        for section in physics_knowledge.values():
            if query in section["title"].lower():
                results.append(f"📚 **{section['title']}**\n{section.get('description', '')}")
            
            for topic_key, topic in section.get("topics", {}).items():
                if query in topic["title"].lower():
                    results.append(format_topic_info(topic))
    
    return results if results else ["К сожалению, информация по вашему запросу не найдена."]

def format_topic_info(topic):
    """Форматирование информации о теме"""
    result = f"📖 **{topic['title']}**\n"
    
    # Добавляем информацию о подтемах
    for key, value in topic.items():
        if isinstance(value, dict) and "name" in value:
            result += f"\n🔹 **{value['name']}**\n"
            if "description" in value:
                result += f"📝 {value['description']}\n"
            if "formula" in value:
                result += f"📐 Формула: {value['formula']}\n"
    
    return result