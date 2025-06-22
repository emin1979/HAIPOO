# semantic_field.py

class ConceptUnit:
    """
    Представляет собой базовую единицу смысла, которая может быть
    словом, понятием или мыслью. Включает различные "плоскости" представления
    и механизм для создания связей с другими единицами.
    """
    _next_id = 1 # Для автоматической генерации уникальных ID, если не задан вручную

    def __init__(self, word_representation: str = None, concept_id: str = None, description: str = None, initial_value: float = 0.0):
        """
        Инициализирует ConceptUnit.

        :param word_representation: Текстовое представление (Слово).
        :param concept_id: Уникальный идентификатор понятия (Понятие).
        :param description: Описание или ассоциированная мысль (Мысль).
        :param initial_value: Начальное числовое значение, прототип "силы заряда" или "интенсивности".
        """
        self.word = word_representation
        
        # Если concept_id не задан, генерируем его автоматически
        if concept_id is None:
            self.concept_id = f"CONCEPT_{ConceptUnit._next_id}"
            ConceptUnit._next_id += 1
        else:
            self.concept_id = concept_id
            
        self.description = description
        self.value = initial_value # Прототип "силы заряда"
        self.connections = [] # Связи с другими ConceptUnit

    def add_connection(self, other_concept_unit: 'ConceptUnit', relationship_type: str = "related_to", strength: float = 1.0):
        """
        Добавляет связь с другим ConceptUnit.

        :param other_concept_unit: Другая единица понятия, с которой устанавливается связь.
        :param relationship_type: Тип отношения (например, "is_a", "has_part", "causes", "contradicts").
        :param strength: Сила связи, прототип "силы поля".
        """
        if isinstance(other_concept_unit, ConceptUnit):
            self.connections.append({
                "concept": other_concept_unit,
                "type": relationship_type,
                "strength": strength
            })
        else:
            print(f"Ошибка: '{other_concept_unit}' не является экземпляром ConceptUnit.")

    def get_connections(self, relationship_type: str = None):
        """
        Возвращает список связей, возможно, отфильтрованный по типу.
        """
        if relationship_type:
            return [conn for conn in self.connections if conn['type'] == relationship_type]
        return self.connections

    def __str__(self):
        """
        Представление объекта для вывода.
        """
        return (f"ConceptUnit(ID: '{self.concept_id}', Word: '{self.word}', "
                f"Value: {self.value}, Description: '{self.description[:30]}...')")

    def __repr__(self):
        """
        Более формальное представление для отладки.
        """
        return self.__str__()

# --- Примеры использования и базовые "уравнения" (функции взаимодействия) ---

def combine_concepts(concept1: ConceptUnit, concept2: ConceptUnit, new_word: str = None, new_description: str = None) -> ConceptUnit:
    """
    Пример "сложения" двух концепций.
    Объединяет их значения и описания, создавая новую концепцию.
    Это очень примитивный прототип нашего "уравнения сложения смыслов".
    """
    combined_value = concept1.value + concept2.value
    combined_description = f"Объединение: ({concept1.description}) и ({concept2.description})"
    if new_description:
        combined_description = new_description
    
    # Попытка создать более осмысленное слово для новой концепции
    if new_word:
        combined_word = new_word
    elif concept1.word and concept2.word:
        combined_word = f"{concept1.word}_{concept2.word}_combined"
    else:
        combined_word = None

    new_concept = ConceptUnit(
        word_representation=combined_word,
        description=combined_description,
        initial_value=combined_value
    )
    new_concept.add_connection(concept1, "component_of", concept1.value)
    new_concept.add_connection(concept2, "component_of", concept2.value)
    return new_concept

# --- Тестирование ---
if __name__ == "__main__":
    print("--- Создание базовых ConceptUnit ---")
    love = ConceptUnit("любовь", description="глубокое чувство привязанности", initial_value=10.0)
    respect = ConceptUnit("уважение", description="признание достоинства", initial_value=8.0)
    knowledge = ConceptUnit("знание", description="информация, полученная через обучение", initial_value=15.0)
    action = ConceptUnit("действие", description="процесс осуществления чего-либо", initial_value=7.0)

    print(love)
    print(respect)
    print(knowledge)
    print(action)

    print("\n--- Добавление связей ---")
    love.add_connection(respect, "implies", 0.9)
    respect.add_connection(love, "supports", 0.8)
    knowledge.add_connection(action, "leads_to", 0.7)
    
    print(f"Связи для '{love.word}': {[f'{conn['concept'].word} ({conn['type']})' for conn in love.get_connections()]}")
    print(f"Связи для '{knowledge.word}': {[f'{conn['concept'].word} ({conn['type']})' for conn in knowledge.get_connections()]}")

    print("\n--- Прототип 'сложения' смыслов ---")
    # "Любовь" + "Уважение" = "Здоровые отношения"
    healthy_relations = combine_concepts(love, respect, "здоровые_отношения", "сочетание любви и уважения в отношениях")
    print(healthy_relations)
    print(f"Компоненты '{healthy_relations.word}': {[f'{conn['concept'].word} ({conn['type']})' for conn in healthy_relations.get_connections('component_of')]}")

    # "Знание" * "Действие" (умножение как синергия) - пока просто сложение, но идея заложена
    # Здесь пока используем combine_concepts, но в будущем это может быть другая функция (например, multiply_concepts)
    wisdom = combine_concepts(knowledge, action, "мудрость", "знания, примененные на практике")
    print(wisdom)
    print(f"Компоненты '{wisdom.word}': {[f'{conn['concept'].word} ({conn['type']})' for conn in wisdom.get_connections('component_of')]}")

    print("\n--- Тестирование автоматического ID ---")
    auto_concept = ConceptUnit("абстракция")
    print(auto_concept)
    another_auto = ConceptUnit("философия")
    print(another_auto)
