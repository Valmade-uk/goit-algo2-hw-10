from dataclasses import dataclass, field
from typing import Set, List, Optional


@dataclass
class Teacher:
    first_name: str
    last_name: str
    age: int
    email: str
    can_teach_subjects: Set[str]
    assigned_subjects: Set[str] = field(default_factory=set)


def create_schedule(subjects: Set[str], teachers: List[Teacher]) -> Optional[List[Teacher]]:
    """
    Жадібний алгоритм покриття множини:
    - на кожному кроці обираємо викладача, який покриває найбільше ще не покритих предметів;
    - якщо таких кілька — обираємо наймолодшого;
    - якщо і вік однаковий — детермінований тай-брейк (прізвище, ім'я, email).
    Повертає список ОБРАНИХ викладачів з заповненим assigned_subjects або None.
    """
    uncovered = set(subjects)

    # Очистимо призначення (на випадок повторного запуску)
    for t in teachers:
        t.assigned_subjects.clear()

    # Працюємо з копією списку (але з тими ж об'єктами), щоб не чіпати сам список teachers
    available = list(teachers)
    selected: List[Teacher] = []

    while uncovered:
        best_teacher: Optional[Teacher] = None
        best_cover: Set[str] = set()

        for t in available:
            cover = t.can_teach_subjects & uncovered
            if not cover:
                continue

            if best_teacher is None:
                best_teacher = t
                best_cover = cover
                continue

            # 1) максимум покриття
            if len(cover) > len(best_cover):
                best_teacher = t
                best_cover = cover
                continue

            # 2) тай-брейк: наймолодший
            if len(cover) == len(best_cover):
                if t.age < best_teacher.age:
                    best_teacher = t
                    best_cover = cover
                    continue

                # 3) детермінізм при повній рівності
                if t.age == best_teacher.age:
                    key_t = (t.last_name, t.first_name, t.email)
                    key_best = (best_teacher.last_name, best_teacher.first_name, best_teacher.email)
                    if key_t < key_best:
                        best_teacher = t
                        best_cover = cover

        if best_teacher is None:
            return None

        best_teacher.assigned_subjects = set(best_cover)
        selected.append(best_teacher)
        uncovered -= best_cover
        available.remove(best_teacher)

    return selected


if __name__ == '__main__':
    # Множина предметів
    subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}

    # Список викладачів
    teachers = [
        Teacher("Олександр", "Іваненко", 45, "o.ivanenko@example.com", {"Математика", "Фізика"}),
        Teacher("Марія", "Петренко", 38, "m.petrenko@example.com", {"Хімія"}),
        Teacher("Сергій", "Коваленко", 50, "s.kovalenko@example.com", {"Інформатика", "Математика"}),
        Teacher("Наталія", "Шевченко", 29, "n.shevchenko@example.com", {"Біологія", "Хімія"}),
        Teacher("Дмитро", "Бондаренко", 35, "d.bondarenko@example.com", {"Фізика", "Інформатика"}),
        Teacher("Олена", "Гриценко", 42, "o.grytsenko@example.com", {"Біологія"}),
    ]

    # Створення розкладу
    schedule = create_schedule(subjects, teachers)

    # Виведення
    if schedule:
        print("Розклад занять:")
        for t in schedule:
            print(f"{t.first_name} {t.last_name}, {t.age} років, email: {t.email}")
            print(f"   Викладає предмети: {', '.join(sorted(t.assigned_subjects))}\n")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")