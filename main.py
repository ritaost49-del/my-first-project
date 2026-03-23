import json
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter.font import Font
#проверка22
# Имя файла для хранения данных
DATA_FILE = "mood_diary.json"


class MoodDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Дневник настроения")
        self.root.geometry("500x700")
        self.root.configure(bg="#f5f5f5")

        # Загружаем записи
        self.entries = self.load_entries()

        # Создаем интерфейс
        self.setup_ui()

        # Показываем главный экран
        self.show_main_screen()

    def load_entries(self):
        """Загружает записи из файла"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_entries(self):
        """Сохраняет записи в файл"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)

    def setup_ui(self):
        """Настраивает основной интерфейс"""
        # Создаем основной контейнер
        self.main_container = tk.Frame(self.root, bg="#f5f5f5")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Шапка приложения
        header = tk.Frame(self.main_container, bg="#4a90e2", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(header, text="📔 Дневник настроения",
                         font=("Arial", 20, "bold"),
                         bg="#4a90e2", fg="white")
        title.pack(pady=20)

        # Контейнер для контента
        self.content_frame = tk.Frame(self.main_container, bg="#f5f5f5")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Нижняя панель с кнопками
        bottom_frame = tk.Frame(self.main_container, bg="#f5f5f5")
        bottom_frame.pack(fill=tk.X, padx=15, pady=10)

        btn_style = {"font": ("Arial", 11), "bg": "#4a90e2", "fg": "white",
                     "relief": tk.FLAT, "padx": 20, "pady": 8}

        btn_add = tk.Button(bottom_frame, text="➕ Новая запись",
                            command=self.show_add_screen, **btn_style)
        btn_add.pack(side=tk.LEFT, padx=5)

        btn_stats = tk.Button(bottom_frame, text="📊 Статистика",
                              command=self.show_stats_screen, **btn_style)
        btn_stats.pack(side=tk.LEFT, padx=5)

        btn_all = tk.Button(bottom_frame, text="📖 Все записи",
                            command=self.show_all_entries_screen, **btn_style)
        btn_all.pack(side=tk.LEFT, padx=5)

    def clear_content(self):
        """Очищает контентную область"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_main_screen(self):
        """Показывает главный экран с последними записями"""
        self.clear_content()

        # Заголовок
        title = tk.Label(self.content_frame, text="Последние заметки",
                         font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#333")
        title.pack(pady=(0, 15))

        if not self.entries:
            empty_label = tk.Label(self.content_frame,
                                   text="📭 Нет записей\n\nНажмите «Новая запись», чтобы добавить первую заметку",
                                   font=("Arial", 12), bg="#f5f5f5", fg="#999")
            empty_label.pack(expand=True)
            return

        # Создаем canvas для прокрутки
        canvas = tk.Canvas(self.content_frame, bg="#f5f5f5", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f5f5f5")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Показываем последние 5 записей
        recent_entries = self.entries[-5:][::-1]

        for entry in recent_entries:
            self.create_note_card(scrollable_frame, entry)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_note_card(self, parent, entry):
        """Создает карточку заметки"""
        # Получаем дату в читаемом формате
        timestamp = datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S")
        date_str = timestamp.strftime("%d.%m.%Y %H:%M")

        # Карточка
        card = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=1)
        card.pack(fill=tk.X, pady=5, padx=5)

        # Верхняя часть с датой и эмоцией
        top_frame = tk.Frame(card, bg="white")
        top_frame.pack(fill=tk.X, padx=12, pady=(10, 5))

        # Иконка эмоции
        emotion_icons = {
            "радость": "😊", "грусть": "😢", "спокойствие": "😌",
            "злость": "😠", "страх": "😨", "удивление": "😲"
        }
        icon = emotion_icons.get(entry['emotion'], "😐")

        date_label = tk.Label(top_frame, text=f"{date_str}  {icon} {entry['emotion']}",
                              font=("Arial", 10), bg="white", fg="#666")
        date_label.pack(side=tk.LEFT)

        # Оценка настроения
        score_frame = tk.Frame(card, bg="white")
        score_frame.pack(fill=tk.X, padx=12, pady=5)

        score_text = f"Оценка: {entry['score']}/10"
        score_color = "#4caf50" if entry['score'] >= 7 else "#ff9800" if entry['score'] >= 4 else "#f44336"
        score_label = tk.Label(score_frame, text=score_text,
                               font=("Arial", 11, "bold"), bg="white", fg=score_color)
        score_label.pack(side=tk.LEFT)

        # Заметка
        note_text = entry['note'] if entry['note'] else "Нет заметки"
        note_label = tk.Label(card, text=note_text,
                              font=("Arial", 11), bg="white", fg="#333",
                              wraplength=400, justify=tk.LEFT)
        note_label.pack(fill=tk.X, padx=12, pady=(0, 10))

    def show_add_screen(self):
        """Показывает экран добавления записи"""
        self.clear_content()

        # Заголовок
        title = tk.Label(self.content_frame, text="Новая заметка",
                         font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333")
        title.pack(pady=(0, 20))

        # Форма
        form_frame = tk.Frame(self.content_frame, bg="white", relief=tk.RAISED, bd=1)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Эмоция
        emotion_frame = tk.Frame(form_frame, bg="white")
        emotion_frame.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(emotion_frame, text="Эмоция:", font=("Arial", 12, "bold"),
                 bg="white", fg="#333").pack(anchor=tk.W)

        self.emotion_var = tk.StringVar(value="радость")
        emotions = ["радость", "грусть", "спокойствие", "злость", "страх", "удивление"]
        emotion_menu = ttk.Combobox(emotion_frame, textvariable=self.emotion_var,
                                    values=emotions, state="readonly", font=("Arial", 11))
        emotion_menu.pack(fill=tk.X, pady=5)

        # Оценка настроения
        score_frame = tk.Frame(form_frame, bg="white")
        score_frame.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(score_frame, text="Оценка настроения (1-10):",
                 font=("Arial", 12, "bold"), bg="white", fg="#333").pack(anchor=tk.W)

        self.score_var = tk.IntVar(value=7)
        score_scale = tk.Scale(score_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                               variable=self.score_var, bg="white", highlightthickness=0,
                               length=300, sliderlength=20)
        score_scale.pack(pady=5)

        # Заметка
        note_frame = tk.Frame(form_frame, bg="white")
        note_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        tk.Label(note_frame, text="Заметка:", font=("Arial", 12, "bold"),
                 bg="white", fg="#333").pack(anchor=tk.W)

        self.note_text = scrolledtext.ScrolledText(note_frame, height=8,
                                                   font=("Arial", 11), wrap=tk.WORD)
        self.note_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Кнопки
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.pack(fill=tk.X, padx=20, pady=20)

        save_btn = tk.Button(btn_frame, text="💾 Сохранить запись",
                             command=self.save_new_entry,
                             bg="#4caf50", fg="white", font=("Arial", 12, "bold"),
                             relief=tk.FLAT, padx=20, pady=10)
        save_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = tk.Button(btn_frame, text="❌ Отмена",
                               command=self.show_main_screen,
                               bg="#f44336", fg="white", font=("Arial", 12),
                               relief=tk.FLAT, padx=20, pady=10)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def save_new_entry(self):
        """Сохраняет новую запись"""
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        emotion = self.emotion_var.get()
        score = self.score_var.get()
        note = self.note_text.get("1.0", tk.END).strip()

        entry = {
            "timestamp": timestamp,
            "emotion": emotion,
            "score": score,
            "note": note if note else ""
        }

        self.entries.append(entry)
        self.save_entries()

        messagebox.showinfo("Успех", "Запись успешно сохранена!")
        self.show_main_screen()

    def show_all_entries_screen(self):
        """Показывает все записи"""
        self.clear_content()

        if not self.entries:
            empty_label = tk.Label(self.content_frame,
                                   text="📭 Нет записей",
                                   font=("Arial", 12), bg="#f5f5f5", fg="#999")
            empty_label.pack(expand=True)
            return

        # Заголовок
        title = tk.Label(self.content_frame, text=f"Все записи ({len(self.entries)})",
                         font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#333")
        title.pack(pady=(0, 15))

        # Создаем canvas для прокрутки
        canvas = tk.Canvas(self.content_frame, bg="#f5f5f5", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f5f5f5")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Показываем все записи в обратном порядке
        for entry in reversed(self.entries):
            self.create_note_card(scrollable_frame, entry)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def show_stats_screen(self):
        """Показывает статистику"""
        self.clear_content()

        if not self.entries:
            empty_label = tk.Label(self.content_frame,
                                   text="📭 Нет записей для статистики",
                                   font=("Arial", 12), bg="#f5f5f5", fg="#999")
            empty_label.pack(expand=True)
            return

        # Заголовок
        title = tk.Label(self.content_frame, text="Статистика настроения",
                         font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333")
        title.pack(pady=(0, 20))

        # Контейнер для статистики
        stats_frame = tk.Frame(self.content_frame, bg="white", relief=tk.RAISED, bd=1)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        now = datetime.now()

        # Статистика за разные периоды
        periods = [
            ("За последние 24 часа", 1),
            ("За последние 7 дней", 7),
            ("За последние 30 дней", 30),
            ("За всё время", None)
        ]

        row = 0
        for period_name, days in periods:
            avg, count = self.calculate_average(days)

            if avg is not None:
                # Фон в зависимости от настроения
                if avg >= 7:
                    color = "#e8f5e9"
                    mood = "🌞 Хорошее"
                elif avg >= 4:
                    color = "#fff3e0"
                    mood = "🌥️ Среднее"
                else:
                    color = "#ffebee"
                    mood = "🌧️ Плохое"

                period_frame = tk.Frame(stats_frame, bg=color)
                period_frame.pack(fill=tk.X, padx=15, pady=10)

                # Название периода
                name_label = tk.Label(period_frame, text=period_name,
                                      font=("Arial", 12, "bold"), bg=color, fg="#333")
                name_label.pack(anchor=tk.W, padx=10, pady=(10, 5))

                # Количество записей
                count_label = tk.Label(period_frame, text=f"📊 Записей: {count}",
                                       font=("Arial", 10), bg=color, fg="#666")
                count_label.pack(anchor=tk.W, padx=10)

                # Средняя оценка
                score_text = f"Средняя оценка: {avg:.1f}/10"
                score_label = tk.Label(period_frame, text=score_text,
                                       font=("Arial", 14, "bold"), bg=color, fg="#333")
                score_label.pack(anchor=tk.W, padx=10, pady=5)

                # Настроение
                mood_label = tk.Label(period_frame, text=mood,
                                      font=("Arial", 11), bg=color, fg="#666")
                mood_label.pack(anchor=tk.W, padx=10, pady=(0, 10))

        # Анализ эмоций
        emotions = {}
        for entry in self.entries:
            emotion = entry['emotion']
            emotions[emotion] = emotions.get(emotion, 0) + 1

        if emotions:
            most_common = max(emotions, key=emotions.get)

            emotion_frame = tk.Frame(stats_frame, bg="#e3f2fd")
            emotion_frame.pack(fill=tk.X, padx=15, pady=10)

            emotion_label = tk.Label(emotion_frame, text="🎭 Частая эмоция",
                                     font=("Arial", 12, "bold"), bg="#e3f2fd", fg="#333")
            emotion_label.pack(anchor=tk.W, padx=10, pady=(10, 5))

            emotion_icons = {
                "радость": "😊", "грусть": "😢", "спокойствие": "😌",
                "злость": "😠", "страх": "😨", "удивление": "😲"
            }
            icon = emotion_icons.get(most_common, "😐")

            common_label = tk.Label(emotion_frame,
                                    text=f"{icon} {most_common} ({emotions[most_common]} раз)",
                                    font=("Arial", 14), bg="#e3f2fd", fg="#1976d2")
            common_label.pack(anchor=tk.W, padx=10, pady=(0, 10))

        # Кнопка назад
        back_btn = tk.Button(self.content_frame, text="← Назад",
                             command=self.show_main_screen,
                             bg="#4a90e2", fg="white", font=("Arial", 11),
                             relief=tk.FLAT, padx=20, pady=8)
        back_btn.pack(pady=10)

    def calculate_average(self, period_days=None):
        """Вычисляет среднюю оценку настроения за период"""
        if not self.entries:
            return None, 0

        now = datetime.now()
        filtered_entries = []

        for entry in self.entries:
            entry_date = datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S")

            if period_days is None:
                filtered_entries.append(entry)
            else:
                days_ago = now - entry_date
                if days_ago.days < period_days:
                    filtered_entries.append(entry)

        if not filtered_entries:
            return None, 0

        total_score = sum(e['score'] for e in filtered_entries)
        average = total_score / len(filtered_entries)

        return average, len(filtered_entries)


def main():
    root = tk.Tk()
    app = MoodDiaryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
