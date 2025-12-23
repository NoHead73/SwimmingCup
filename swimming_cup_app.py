import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os
import sys
import tempfile
from pathlib import Path

class SwimmingCupApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Кубок ВС РФ по плаванию")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)

        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        self.register_fonts()

        self.teams = []
        self.current_team = 1
        self.team_count = 0
        self.competition_info = {
            'city': '',
            'dates': '',
            'venue': '',
            'pool_length': '25 метров'
        }

        self.current_screen = None
        self.score_entries = []

        self.create_widgets()
        self.show_start_screen()

    def register_fonts(self):
        try:
            font_path = self.find_font_file('arial.ttf')
            if font_path:
                pdfmetrics.registerFont(TTFont('Arial', font_path))
                pdfmetrics.registerFont(TTFont('Arial-Bold', font_path))
                self.font_name = 'Arial'
            else:
                self.font_name = 'Helvetica'
        except:
            self.font_name = 'Helvetica'

    def find_font_file(self, font_name):
        search_paths = [
            os.path.dirname(os.path.abspath(__file__)),
            os.getcwd(),
            tempfile.gettempdir(),
            r'C:\Windows\Fonts',
            r'C:\Windows\Fonts\arial.ttf',
        ]

        if getattr(sys, 'frozen', False):
            search_paths.insert(0, sys._MEIPASS)

        for path in search_paths:
            font_path = os.path.join(path, font_name)
            if os.path.exists(font_path):
                return font_path

            font_path = os.path.join(path, 'arial.ttf')
            if os.path.exists(font_path):
                return font_path

        return None

    def create_widgets(self):
        self.title_label = tk.Label(
            self.root,
            text="КУБОК ВС РФ ПО ПЛАВАНИЮ",
            font=("Arial", 14, "bold"),
            bg="#2196F3",
            fg="white",
            height=2
        )
        self.title_label.pack(fill="x")

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        self.current_screen = "start"
        self.clear_main_frame()

        center_frame = ttk.Frame(self.main_frame)
        center_frame.pack(fill="both", expand=True)

        welcome_label = tk.Label(
            center_frame,
            text="Приложение для определения командных результатов\nКубка ВС РФ по плаванию среди мужчин",
            font=("Arial", 14),
            justify="center"
        )
        welcome_label.pack(pady=60)

        btn_frame = ttk.Frame(center_frame)
        btn_frame.pack(pady=30)

        self.start_btn = tk.Button(
            btn_frame,
            text="Начать",
            command=self.show_info_screen,
            font=("Arial", 11),
            bg="#2196F3",
            fg="white",
            width=25,
            height=2,
            relief="raised",
            bd=3
        )
        self.start_btn.pack(pady=10)

        self.start_btn.focus_set()
        self.start_btn.bind('<Return>', lambda e: self.show_info_screen())

    def show_info_screen(self, event=None):
        self.current_screen = "info"
        self.clear_main_frame()

        main_frame = ttk.Frame(self.main_frame)
        main_frame.pack(fill="both", expand=True, padx=40, pady=25)

        title = tk.Label(
            main_frame,
            text="Информация о соревнованиях",
            font=("Arial", 14, "bold")
        )
        title.pack(pady=15)

        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20, fill="x")

        fields = [
            ("Место проведения (город):", "city_entry", ""),
            ("Сроки проведения:", "dates_entry", "01.03.2026 - 06.03.2026"),
            ("Спортивный объект:", "venue_entry", ""),
        ]

        self.entries = {}

        for i, (label_text, key, default) in enumerate(fields):
            label = tk.Label(form_frame, text=label_text, font=("Arial", 10), anchor="w")
            label.grid(row=i, column=0, sticky="w", pady=10, padx=10)

            entry = tk.Entry(form_frame, width=35, font=("Arial", 10))
            if default:
                entry.insert(0, default)
            entry.grid(row=i, column=1, pady=10, padx=10)
            self.entries[key] = entry

            entry.bind('<Return>',
                       lambda e, idx=i: self.focus_next_field(idx, len(fields)))

        tk.Label(form_frame, text="Длина бассейна:", font=("Arial", 10)).grid(
            row=3, column=0, sticky="w", pady=10, padx=10)

        self.pool_var = tk.StringVar(value="25 метров")
        pool_combo = ttk.Combobox(
            form_frame,
            textvariable=self.pool_var,
            values=["25 метров", "50 метров"],
            state="readonly",
            width=33,
            font=("Arial", 10)
        )
        pool_combo.grid(row=3, column=1, pady=10, padx=10)
        pool_combo.bind('<Return>', lambda e: self.save_competition_info())

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=25)

        back_btn = tk.Button(
            btn_frame,
            text="Назад",
            command=self.show_start_screen,
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            width=13,
            height=1,
            relief="raised",
            bd=2
        )
        back_btn.pack(side="left", padx=15)

        next_btn = tk.Button(
            btn_frame,
            text="Далее",
            command=self.save_competition_info,
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            width=13,
            height=1,
            relief="raised",
            bd=3
        )
        next_btn.pack(side="left", padx=15)

        self.entries['city_entry'].focus_set()

    def focus_next_field(self, current_idx, total_fields):
        keys = list(self.entries.keys())
        if current_idx < len(keys) - 1:
            next_key = keys[current_idx + 1]
            self.entries[next_key].focus_set()

    def save_competition_info(self, event=None):
        city = self.entries['city_entry'].get().strip()
        dates = self.entries['dates_entry'].get().strip()
        venue = self.entries['venue_entry'].get().strip()

        if not all([city, dates, venue]):
            messagebox.showerror("Ошибка", "Заполните все поля!")
            self.entries['city_entry'].focus_set()
            return

        self.competition_info = {
            'city': city,
            'dates': dates,
            'venue': venue,
            'pool_length': self.pool_var.get()
        }

        self.show_team_count_screen()

    def show_team_count_screen(self):
        self.current_screen = "team_count"
        self.clear_main_frame()

        center_frame = ttk.Frame(self.main_frame)
        center_frame.pack(fill="both", expand=True, padx=40, pady=40)

        title = tk.Label(
            center_frame,
            text="Количество команд",
            font=("Arial", 14, "bold")
        )
        title.pack(pady=15)

        tk.Label(
            center_frame,
            text="Количество участвующих команд?",
            font=("Arial", 11)
        ).pack(pady=20)

        slider_frame = ttk.Frame(center_frame)
        slider_frame.pack(pady=20)

        self.team_count_var = tk.IntVar(value=10)

        tk.Label(slider_frame, text="1", font=("Arial", 9)).pack(side="left", padx=8)
        team_slider = tk.Scale(
            slider_frame,
            from_=1,
            to=100,
            variable=self.team_count_var,
            orient="horizontal",
            length=350,
            font=("Arial", 9),
            resolution=1
        )
        team_slider.pack(side="left", padx=8)
        tk.Label(slider_frame, text="100", font=("Arial", 9)).pack(side="left", padx=8)

        self.count_label = tk.Label(
            center_frame,
            text=f"{self.team_count_var.get()} команд",
            font=("Arial", 12, "bold"),
            fg="#2196F3"
        )
        self.count_label.pack(pady=15)

        def update_label(*args):
            self.count_label.config(text=f"{self.team_count_var.get()} команд")

        self.team_count_var.trace("w", update_label)

        btn_frame = ttk.Frame(center_frame)
        btn_frame.pack(pady=30)

        back_btn = tk.Button(
            btn_frame,
            text="Назад",
            command=self.show_info_screen,
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            width=13,
            height=1,
            relief="raised",
            bd=2
        )
        back_btn.pack(side="left", padx=20)

        start_btn = tk.Button(
            btn_frame,
            text="Начать ввод команд",
            command=self.start_teams_input,
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            width=18,
            height=1,
            relief="raised",
            bd=3
        )
        start_btn.pack(side="left", padx=20)

        start_btn.bind('<Return>', lambda e: self.start_teams_input())
        start_btn.focus_set()

    def start_teams_input(self, event=None):
        self.team_count = self.team_count_var.get()
        self.teams = []
        self.current_team = 1
        self.show_team_name_screen()

    def show_team_name_screen(self):
        self.current_screen = "team_name"
        self.clear_main_frame()

        container = ttk.Frame(self.main_frame)
        container.pack(fill="both", expand=True)

        top_frame = ttk.Frame(container)
        top_frame.pack(fill="x", padx=40, pady=20)

        title = tk.Label(
            top_frame,
            text=f"Команда {self.current_team} из {self.team_count}",
            font=("Arial", 14, "bold")
        )
        title.pack(pady=5)

        tk.Label(
            top_frame,
            text="Введите название команды:",
            font=("Arial", 11)
        ).pack(pady=10)

        self.team_name_entry = tk.Entry(
            top_frame,
            width=40,
            font=("Arial", 11)
        )
        self.team_name_entry.pack(pady=5)
        self.team_name_entry.focus_set()

        middle_frame = ttk.Frame(container)
        middle_frame.pack(fill="both", expand=True, padx=40, pady=10)

        if self.teams:
            sorted_teams = sorted(self.teams, key=lambda x: x['total'], reverse=True)

            for i, team in enumerate(sorted_teams):
                team['temp_position'] = i + 1

            results_frame = ttk.LabelFrame(middle_frame, text="Промежуточные результаты", padding=10)
            results_frame.pack(fill="both", expand=True)

            columns = ('temp_position', 'name', 'total')
            self.intermediate_tree = ttk.Treeview(
                results_frame,
                columns=columns,
                show='headings',
                height=8
            )

            self.intermediate_tree.heading('temp_position', text='Место')
            self.intermediate_tree.heading('name', text='Команда')
            self.intermediate_tree.heading('total', text='Очки')

            self.intermediate_tree.column('temp_position', width=80, anchor='center')
            self.intermediate_tree.column('name', width=300)
            self.intermediate_tree.column('total', width=100, anchor='center')

            tree_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.intermediate_tree.yview)
            self.intermediate_tree.configure(yscrollcommand=tree_scrollbar.set)

            self.intermediate_tree.pack(side="left", fill="both", expand=True)
            tree_scrollbar.pack(side="right", fill="y")

            for team in sorted_teams:
                self.intermediate_tree.insert(
                    '', 'end',
                    values=(team['temp_position'], team['name'], team['total'])
                )

        bottom_frame = ttk.Frame(container)
        bottom_frame.pack(fill="x", padx=40, pady=20)

        btn_frame = ttk.Frame(bottom_frame)
        btn_frame.pack()

        back_btn = tk.Button(
            btn_frame,
            text="Назад",
            command=self.show_team_count_screen,
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            width=13,
            height=1,
            relief="raised",
            bd=2
        )
        back_btn.pack(side="left", padx=20)

        next_btn = tk.Button(
            btn_frame,
            text="Далее → Ввод результатов",
            command=self.go_to_scores,
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            width=22,
            height=1,
            relief="raised",
            bd=3
        )
        next_btn.pack(side="left", padx=20)

        self.team_name_entry.bind('<Return>', lambda e: self.go_to_scores())
        next_btn.bind('<Return>', lambda e: self.go_to_scores())

    def go_to_scores(self, event=None):
        team_name = self.team_name_entry.get().strip()
        if not team_name:
            messagebox.showerror("Ошибка", "Введите название команды!")
            self.team_name_entry.focus_set()
            return

        existing_names = [team['name'].lower() for team in self.teams]
        if team_name.lower() in existing_names:
            messagebox.showerror("Ошибка", f"Команда '{team_name}' уже существует! Введите другое название.")
            self.team_name_entry.delete(0, tk.END)
            self.team_name_entry.focus_set()
            return

        self.current_team_name = team_name
        self.show_scores_screen()

    def show_scores_screen(self):
        self.current_screen = "scores"
        self.clear_main_frame()
        self.score_entries = []

        main_frame = ttk.Frame(self.main_frame)
        main_frame.pack(fill="both", expand=True, padx=40, pady=30)

        title = tk.Label(
            main_frame,
            text=f"Результаты: {self.current_team_name}",
            font=("Arial", 14, "bold")
        )
        title.pack(pady=15)

        tk.Label(
            main_frame,
            text="Введите 20 результатов (0-999):",
            font=("Arial", 11)
        ).pack(pady=10)

        scores_frame = ttk.Frame(main_frame)
        scores_frame.pack(pady=20, padx=50)

        for i in range(20):
            row = i // 5
            col = i % 5

            frame = ttk.Frame(scores_frame)
            frame.grid(row=row, column=col, padx=12, pady=10)

            tk.Label(frame, text=f"{i+1}:", font=("Arial", 9)).pack(side="left", padx=4)
            entry = tk.Entry(frame, width=8, justify="center", font=("Arial", 9))
            entry.pack(side="left")
            self.score_entries.append(entry)

            if i < 19:
                entry.bind('<Return>',
                           lambda e, next_idx=i+1: self.score_entries[next_idx].focus_set())
            else:
                entry.bind('<Return>', lambda e: self.save_team_scores())

        self.filled_label = tk.Label(
            main_frame,
            text="Заполнено: 0/20",
            font=("Arial", 10),
            fg="green"
        )
        self.filled_label.pack(pady=10)

        def update_filled_count():
            filled = sum(1 for entry in self.score_entries if entry.get().strip())
            self.filled_label.config(
                text=f"Заполнено: {filled}/20",
                fg="green" if filled == 20 else "orange" if filled >= 10 else "red"
            )

        for entry in self.score_entries:
            entry.bind('<KeyRelease>', lambda e: update_filled_count())

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=25)

        back_btn = tk.Button(
            btn_frame,
            text="Назад",
            command=self.show_team_name_screen,
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            width=13,
            height=1,
            relief="raised",
            bd=2
        )
        back_btn.pack(side="left", padx=20)

        save_btn = tk.Button(
            btn_frame,
            text="Сохранить команду",
            command=self.save_team_scores,
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            width=18,
            height=1,
            relief="raised",
            bd=3
        )
        save_btn.pack(side="left", padx=20)

        self.score_entries[0].focus_set()
        update_filled_count()

    def save_team_scores(self, event=None):
        scores = []

        for i, entry in enumerate(self.score_entries):
            value = entry.get().strip()
            if not value:
                messagebox.showerror("Ошибка", f"Поле {i+1} не заполнено!")
                entry.focus_set()
                return
            try:
                score = int(value)
                if 0 <= score <= 999:
                    scores.append(score)
                else:
                    messagebox.showerror("Ошибка", f"Результат {i+1} должен быть от 0 до 999!")
                    entry.focus_set()
                    return
            except ValueError:
                messagebox.showerror("Ошибка", f"Поле {i+1}: введите число!")
                entry.focus_set()
                return

        sorted_scores = sorted(scores, reverse=True)
        best_15 = sum(sorted_scores[:15])

        self.teams.append({
            'name': self.current_team_name,
            'scores': scores,
            'total': best_15,
            'position': 0
        })

        self.current_team += 1

        if self.current_team > self.team_count:
            self.calculate_final_results()
            self.show_final_results()
        else:
            self.show_team_name_screen()

    def calculate_final_results(self):
        self.teams.sort(key=lambda x: x['total'], reverse=True)

        position = 1
        for i, team in enumerate(self.teams):
            if i > 0 and team['total'] == self.teams[i-1]['total']:
                team['position'] = self.teams[i-1]['position']
            else:
                team['position'] = position
            position += 1

    def show_final_results(self):
        self.current_screen = "results"
        self.clear_main_frame()

        main_frame = ttk.Frame(self.main_frame)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill="x", padx=20, pady=5)

        title = tk.Label(
            title_frame,
            text="ИТОГОВЫЕ РЕЗУЛЬТАТЫ",
            font=("Arial", 16, "bold"),
            fg="#D32F2F"
        )
        title.pack()

        info_frame = ttk.LabelFrame(main_frame, text="Информация о соревнованиях", padding=8)
        info_frame.pack(fill="x", padx=20, pady=5)

        info_text = f"Место: {self.competition_info['city']}\n"
        info_text += f"Сроки: {self.competition_info['dates']}\n"
        info_text += f"Объект: {self.competition_info['venue']}\n"
        info_text += f"Бассейн: {self.competition_info['pool_length']}"

        tk.Label(info_frame, text=info_text, justify="left",
                 font=("Arial", 9)).pack(anchor="w")

        table_frame = ttk.LabelFrame(main_frame, text="Таблица результатов", padding=10)
        table_frame.pack(fill="both", expand=True, padx=20, pady=5)

        columns = ('position', 'name', 'total')
        self.results_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=5
        )

        self.results_tree.heading('position', text='Место')
        self.results_tree.heading('name', text='Команда')
        self.results_tree.heading('total', text='Сумма очков')

        self.results_tree.column('position', width=70, anchor='center')
        self.results_tree.column('name', width=350)
        self.results_tree.column('total', width=120, anchor='center')

        tree_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=tree_scrollbar.set)

        self.results_tree.pack(side="left", fill="both", expand=True)
        tree_scrollbar.pack(side="right", fill="y")

        for team in self.teams:
            self.results_tree.insert(
                '', 'end',
                values=(team['position'], team['name'], team['total'])
            )

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", padx=20, pady=15)

        pdf_btn = tk.Button(
            btn_frame,
            text="Сохранить в PDF",
            command=self.save_to_pdf,
            font=("Arial", 11, "bold"),
            bg="#2196F3",
            fg="white",
            width=18,
            height=1,
            relief="raised",
            bd=3
        )
        pdf_btn.pack(side="left", padx=20)

        exit_btn = tk.Button(
            btn_frame,
            text="Выход",
            command=self.root.quit,
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            width=18,
            height=1,
            relief="raised",
            bd=2
        )
        exit_btn.pack(side="right", padx=20)

    def save_to_pdf(self, event=None):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF файлы", "*.pdf")],
            initialfile="Кубок_ВС_РФ_по_плаванию_мужчины_итог.pdf",
            title="Сохранить результаты в PDF"
        )

        if not file_path:
            return

        try:
            doc = SimpleDocTemplate(
                file_path,
                pagesize=A4,
                topMargin=57,
                bottomMargin=43,
                leftMargin=40,
                rightMargin=40
            )
            elements = []

            styles = getSampleStyleSheet()

            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontName=self.font_name,
                fontSize=16,
                alignment=1,
                spaceAfter=10
            )

            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontName=self.font_name,
                fontSize=14,
                alignment=1,
                spaceAfter=15
            )

            info_style = ParagraphStyle(
                'CustomInfo',
                parent=styles['Normal'],
                fontName=self.font_name,
                fontSize=10,
                alignment=0,
                leftIndent=0,
                spaceAfter=5
            )

            elements.append(Paragraph("КУБОК ВС РФ ПО ПЛАВАНИЮ", title_style))
            elements.append(Paragraph("ИТОГОВЫЕ РЕЗУЛЬТАТЫ КОМАНДНОГО ПЕРВЕНСТВА СРЕДИ МУЖЧИН", subtitle_style))

            elements.append(Paragraph("Информация о соревнованиях:", info_style))
            elements.append(Paragraph(f"Место проведения: {self.competition_info['city']}", info_style))
            elements.append(Paragraph(f"Сроки проведения: {self.competition_info['dates']}", info_style))
            elements.append(Paragraph(f"Спортивный объект: {self.competition_info['venue']}", info_style))
            elements.append(Paragraph(f"Длина бассейна: {self.competition_info['pool_length']}", info_style))

            elements.append(Spacer(1, 15))

            table_data = [['Место', 'Команда', 'Сумма очков']]
            for team in self.teams:
                table_data.append([str(team['position']), team['name'], str(team['total'])])

            col_widths = [40, 350, 80]
            table = Table(table_data, colWidths=col_widths, hAlign='LEFT')

            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E75B6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), self.font_name),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F2F2F2')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F2F2F2'), colors.white])
            ])

            table.setStyle(table_style)
            elements.append(table)

            doc.build(elements)

            messagebox.showinfo("Успех", f"Файл успешно сохранен:\n{file_path}")

        except Exception as e:
            try:
                c = canvas.Canvas(file_path, pagesize=A4)
                width, height = A4

                c.setFont(self.font_name, 16)
                title1 = "КУБОК ВС РФ ПО ПЛАВАНИЮ"
                title1_width = c.stringWidth(title1, self.font_name, 16)
                c.drawString((width - title1_width) / 2, height - 57, title1)

                c.setFont(self.font_name, 14)
                title2 = "ИТОГОВЫЕ РЕЗУЛЬТАТЫ КОМАНДНОГО ПЕРВЕНСТВА СРЕДИ МУЖЧИН"
                title2_width = c.stringWidth(title2, self.font_name, 14)
                c.drawString((width - title2_width) / 2, height - 85, title2)

                c.setFont(self.font_name, 10)
                y = height - 120
                c.drawString(50, y, f"Место проведения: {self.competition_info['city']}")
                y -= 15
                c.drawString(50, y, f"Сроки проведения: {self.competition_info['dates']}")
                y -= 15
                c.drawString(50, y, f"Спортивный объект: {self.competition_info['venue']}")
                y -= 15
                c.drawString(50, y, f"Длина бассейна: {self.competition_info['pool_length']}")

                y -= 30
                c.setFont(self.font_name, 12)
                c.drawString(50, y, "Место")
                c.drawString(100, y, "Команда")
                c.drawString(450, y, "Сумма очков")

                c.line(50, y-5, 550, y-5)

                y -= 15
                c.setFont(self.font_name, 10)

                for team in self.teams:
                    if y < 43:
                        c.showPage()
                        c.setFont(self.font_name, 10)
                        y = height - 57

                    c.drawString(50, y, str(team['position']))
                    c.drawString(100, y, team['name'])
                    c.drawString(450, y, str(team['total']))
                    y -= 12

                c.save()

                messagebox.showinfo("Успех", f"Файл успешно сохранен:\n{file_path}")

            except Exception as e2:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e2)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SwimmingCupApp()
    app.run()