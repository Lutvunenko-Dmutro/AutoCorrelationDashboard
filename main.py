import sys
import io
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import logic 
import plotting 

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class EnergyAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Аналіз Часових Рядів Енергосистеми (з вкладками)")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2C3E50')
        
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#2C3E50')
        self.style.configure('TLabel', background='#2C3E50', foreground='white', font=('Arial', 10))
        self.style.configure('Title.TLabel', font=('Arial', 12, 'bold'), foreground='#3498DB')
        self.style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[10, 5])
        
        # --- Змінні для даних ---
        # Вкладка 1 (Завдання 1)
        self.dates_t1 = None
        self.power_t1 = None
        self.y_t_t1 = None
        self.y_t_plus_1_t1 = None
        self.rho_1_t1 = None
        self.acf_values_t1 = None
        self.mu_t1 = None
        self.sigma_t1 = None
        self.last_val_t1 = None

        # Вкладка 2 (Завдання 2 / CSV)
        self.dates_t2 = None
        self.power_t2 = None
        self.y_t_t2 = None
        self.y_t_plus_1_t2 = None
        self.rho_1_t2 = None
        self.acf_values_t2 = None
        self.mu_t2 = None
        self.sigma_t2 = None
        self.last_val_t2 = None

        self.setup_ui()
        self.load_task1_data() # Автоматично завантажуємо дані для 1-ї вкладки
        
    def setup_ui(self):
        # --- Заголовок ---
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=10)
        title_label = ttk.Label(title_frame, text="🔋 АНАЛІЗ ЧАСОВИХ РЯДІВ", style='Title.TLabel', font=('Arial', 14, 'bold'))
        title_label.pack()
        
        # --- Створення вкладок ---
        notebook = ttk.Notebook(self.root)
        
        self.tab1 = ttk.Frame(notebook, style='TFrame')
        self.tab2 = ttk.Frame(notebook, style='TFrame')
        
        notebook.add(self.tab1, text=" Завдання 1: Аналіз 16 точок ")
        notebook.add(self.tab2, text=" Завдання 2: Модель Блукання (CSV) ")
        
        notebook.pack(pady=10, padx=20, fill="both", expand=True)

        # --- Наповнення Вкладки 1 ---
        self.setup_tab1()
        
        # --- Наповнення Вкладки 2 ---
        self.setup_tab2()

        # --- Статус бар ---
        self.status_var = tk.StringVar()
        self.status_var.set("Готово. Дані для Завдання 1 завантажено.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # ===================================================================
    # 						ВКЛАДКА 1 (ЗАВДАННЯ 1)
    # ===================================================================
    
    def setup_tab1(self):
        # --- Фрейм для кнопок ---
        button_frame_t1 = ttk.Frame(self.tab1)
        button_frame_t1.pack(pady=10)
        
        btn_t1_series = ttk.Button(button_frame_t1, text="📊 Графік ряду (1a)", command=self.show_timeseries_t1)
        btn_t1_series.pack(side=tk.LEFT, padx=8)
        
        btn_t1_scatter = ttk.Button(button_frame_t1, text="📈 Діаграма розсіюв. (1в)", command=self.show_scatter_t1)
        btn_t1_scatter.pack(side=tk.LEFT, padx=8)
        
        btn_t1_acf = ttk.Button(button_frame_t1, text="🔄 Автокореляція (1в)", command=self.show_autocorrelation_t1)
        btn_t1_acf.pack(side=tk.LEFT, padx=8)
        
        btn_t1_stats = ttk.Button(button_frame_t1, text="📋 Статистика (1в)", command=self.show_statistics_t1)
        btn_t1_stats.pack(side=tk.LEFT, padx=8)
        
        # --- Фрейм для графіка ---
        self.graph_frame_t1 = ttk.Frame(self.tab1)
        self.graph_frame_t1.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_task1_data(self):
        """Автоматично завантажує та обробляє дані для Завдання 1."""
        try:
            self.dates_t1, self.power_t1 = logic.load_test_data()
            (self.y_t_t1, self.y_t_plus_1_t1, 
             self.rho_1_t1, self.acf_values_t1) = logic.calculate_autocorrelation(self.power_t1)
            (self.mu_t1, self.sigma_t1, 
             self.last_val_t1) = logic.calculate_forecast_parameters(self.power_t1)
            self.show_timeseries_t1()
        except Exception as e:
            messagebox.showerror("Помилка Завдання 1", f"Не вдалося завантажити/обробити тестові дані: {e}")

    def show_timeseries_t1(self):
        self.status_var.set("Вкладка 1: Побудова графіка часового ряду...")
        fig = plotting.create_timeseries_plot(self.dates_t1, self.power_t1)
        self.display_figure(fig, self.graph_frame_t1)
        self.status_var.set("Вкладка 1: Графік часового ряду готовий")

    def show_scatter_t1(self):
        self.status_var.set("Вкладка 1: Побудова діаграми розсіювання...")
        fig = plotting.create_scatter_plot(self.y_t_t1, self.y_t_plus_1_t1, self.rho_1_t1)
        self.display_figure(fig, self.graph_frame_t1)
        self.status_var.set("Вкладка 1: Діаграма розсіювання готова")

    def show_autocorrelation_t1(self):
        self.status_var.set("Вкладка 1: Побудова графіків автокореляції...")
        fig = plotting.create_autocorrelation_plot(self.dates_t1, self.y_t_t1, self.y_t_plus_1_t1, 
                                                 self.acf_values_t1, self.rho_1_t1, self.power_t1)
        self.display_figure(fig, self.graph_frame_t1)
        self.status_var.set("Вкладка 1: Графіки автокореляції готові")

    def show_statistics_t1(self):
        self.status_var.set("Вкладка 1: Генерація статистичного звіту...")
        # Оновлений виклик
        self.display_statistics_ui(
            graph_frame=self.graph_frame_t1,
            title="ЗАВДАННЯ 1: АНАЛІЗ 16 ТОЧОК",
            dates=self.dates_t1,
            power_load=self.power_t1,
            rho_1=self.rho_1_t1,
            mu=self.mu_t1,
            sigma=self.sigma_t1,
            last_val=self.last_val_t1,
            is_task1=True
        )
        self.status_var.set("Вкладка 1: Статистичний звіт готовий")

    # ===================================================================
    # 						ВКЛАДКА 2 (ЗАВДАННЯ 2 / CSV)
    # ===================================================================

    def setup_tab2(self):
        # --- Фрейм для завантаження ---
        data_frame_t2 = ttk.Frame(self.tab2)
        data_frame_t2.pack(pady=10)
        
        load_csv_btn = ttk.Button(data_frame_t2, text="📥 Завантажити CSV для Завдання 2", 
                                  command=self.load_csv_data_t2, width=35)
        load_csv_btn.pack(side=tk.LEFT, padx=10)

        # --- Фрейм для кнопок ---
        button_frame_t2 = ttk.Frame(self.tab2)
        button_frame_t2.pack(pady=10)
        
        self.analysis_buttons_t2 = [] # Список для (де)активації
        
        btn_t2_series = ttk.Button(button_frame_t2, text="📊 Часовий ряд (CSV)", 
                                   command=self.show_timeseries_t2, state=tk.DISABLED)
        btn_t2_series.pack(side=tk.LEFT, padx=8)
        self.analysis_buttons_t2.append(btn_t2_series)
        
        btn_t2_acf = ttk.Button(button_frame_t2, text="🔄 Автокореляція (CSV)", 
                                command=self.show_autocorrelation_t2, state=tk.DISABLED)
        btn_t2_acf.pack(side=tk.LEFT, padx=8)
        self.analysis_buttons_t2.append(btn_t2_acf)
        
        btn_t2_forecast = ttk.Button(button_frame_t2, text="🔮 Прогноз (2а)", 
                                     command=self.show_forecast_t2, state=tk.DISABLED)
        btn_t2_forecast.pack(side=tk.LEFT, padx=8)
        self.analysis_buttons_t2.append(btn_t2_forecast)
        
        btn_t2_stats = ttk.Button(button_frame_t2, text="📋 Статистика (2б)", 
                                  command=self.show_statistics_t2, state=tk.DISABLED)
        btn_t2_stats.pack(side=tk.LEFT, padx=8)
        self.analysis_buttons_t2.append(btn_t2_stats)
        
        # --- Фрейм для графіка ---
        self.graph_frame_t2 = ttk.Frame(self.tab2)
        self.graph_frame_t2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_csv_data_t2(self):
        filepath = filedialog.askopenfilename(
            title="Оберіть CSV файл",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not filepath:
            return 
            
        try:
            self.status_var.set(f"Вкладка 2: Завантаження {filepath}...")
            self.root.update_idletasks()
            
            self.dates_t2, self.power_t2 = logic.load_data_from_csv(filepath)
            
            # Розрахунки
            (self.y_t_t2, self.y_t_plus_1_t2, 
             self.rho_1_t2, self.acf_values_t2) = logic.calculate_autocorrelation(self.power_t2)
            (self.mu_t2, self.sigma_t2, 
             self.last_val_t2) = logic.calculate_forecast_parameters(self.power_t2)

            # Активуємо кнопки
            for btn in self.analysis_buttons_t2:
                btn.config(state=tk.NORMAL)
            
            self.status_var.set(f"Вкладка 2: Дані CSV ({len(self.power_t2)} точок) завантажено.")
            # Автоматично показуємо прогноз (головне для Задачі 2)
            self.show_forecast_t2()
            
        except Exception as e:
            messagebox.showerror("Помилка завантаження CSV", f"Не вдалося прочитати файл:\n{e}")
            self.status_var.set("Помилка завантаження. Спробуйте ще раз.")

    def show_timeseries_t2(self):
        self.status_var.set("Вкладка 2: Побудова графіка часового ряду...")
        fig = plotting.create_timeseries_plot(self.dates_t2, self.power_t2)
        self.display_figure(fig, self.graph_frame_t2)
        self.status_var.set("Вкладка 2: Графік часового ряду готовий")

    def show_autocorrelation_t2(self):
        self.status_var.set("Вкладка 2: Побудова графіків автокореляції...")
        fig = plotting.create_autocorrelation_plot(self.dates_t2, self.y_t_t2, self.y_t_plus_1_t2, 
                                                 self.acf_values_t2, self.rho_1_t2, self.power_t2)
        self.display_figure(fig, self.graph_frame_t2)
        self.status_var.set("Вкладка 2: Графіки автокореляції готові")

    def show_forecast_t2(self):
        self.status_var.set("Вкладка 2: Побудова графіка прогнозу (Завдання 2a)...")
        forecast_dates, forecast_values, forecast_rmse = logic.generate_forecast_data(
            self.dates_t2[-1], self.last_val_t2, self.mu_t2, self.sigma_t2)
        
        fig = plotting.create_forecast_plot(self.dates_t2, self.power_t2, forecast_dates, 
                                          forecast_values, forecast_rmse, self.mu_t2, 
                                          self.sigma_t2, self.last_val_t2)
        self.display_figure(fig, self.graph_frame_t2)
        self.status_var.set("Вкладка 2: Графік прогнозування (2а) готовий")

    def show_statistics_t2(self):
        self.status_var.set("Вкладка 2: Генерація статистичного звіту (Завдання 2б)...")
        # Оновлений виклик
        self.display_statistics_ui(
            graph_frame=self.graph_frame_t2,
            title="ЗАВДАННЯ 2: АНАЛІЗ МОДЕЛІ БЛУКАННЯ (CSV)",
            dates=self.dates_t2,
            power_load=self.power_t2,
            rho_1=self.rho_1_t2,
            mu=self.mu_t2,
            sigma=self.sigma_t2,
            last_val=self.last_val_t2,
            is_task1=False
        )
        self.status_var.set("Вкладка 2: Статистичний звіт (2б) готовий")

    # ===================================================================
    # 						ЗАГАЛЬНІ ФУНКЦІЇ
    # ===================================================================

    def clear_graph_frame(self, graph_frame):
        for widget in graph_frame.winfo_children():
            widget.destroy()
    
    def display_figure(self, fig, graph_frame):
        self.clear_graph_frame(graph_frame)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def display_statistics_ui(self, graph_frame, title, dates, power_load, rho_1, mu, sigma, last_val, is_task1=False):
        """
        Створює "професійний" звіт про статистику замість консольного виводу.
        """
        self.clear_graph_frame(graph_frame)
        
        graph_frame.configure(style='TFrame')
        
        # --- Створюємо прокручувану область ---
        canvas = tk.Canvas(graph_frame, bg='#2C3E50', borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(graph_frame, orient="vertical", command=canvas.yview)
        
        scrollable_frame = ttk.Frame(canvas, style='TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        # --- Допоміжні функції для побудови UI ---
        def add_header(parent, text):
            """Додає заголовок розділу з лініями"""
            ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=10, padx=10)
            ttk.Label(parent, text=text, style='Title.TLabel').pack(anchor='w', padx=10)
            ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=(2, 5), padx=10)

        def add_stat(parent, label, value):
            """Додає рядок "Мітка: Значення" """
            frame = ttk.Frame(parent, style='TFrame')
            frame.pack(fill='x', padx=20, pady=2, anchor='w')
            
            # Мітка (жирна)
            ttk.Label(frame, text=f"{label}:", font=('Arial', 10, 'bold'), background='#2C3E50', foreground='white').pack(side='left', anchor='w')
            
            # Значення (з правого боку)
            ttk.Label(frame, text=value, font=('Arial', 10), background='#2C3E50', foreground='#ECF0F1', wraplength=400, justify=tk.LEFT).pack(side='right', anchor='e', expand=True, padx=10)

        # --- 1. Заповнюємо фрейм даними ---
        
        # Головний заголовок
        ttk.Label(scrollable_frame, text=title, style='Title.TLabel', font=('Arial', 14, 'bold')).pack(pady=(5, 10), anchor='center')

        # Визначаємо одиниці виміру
        units = "" if is_task1 else " МВт"
        units_mu = "/год" if is_task1 else " МВт/год"
        units_sigma = "" if is_task1 else " МВт"

        # --- 2. Блок "Характеристики даних" ---
        add_header(scrollable_frame, "ОСНОВНІ ХАРАКТЕРИСТИКИ ДАНИХ")
        try:
            start_date_str = dates[0].strftime('%Y-%m-%d %H:%M')
            end_date_str = dates[-1].strftime('%Y-%m-%d %H:%M')
        except Exception: # Про всяк випадок
            start_date_str = str(dates[0])
            end_date_str = str(dates[-1])
            
        add_stat(scrollable_frame, "Кількість спостережень", f"{len(power_load)}")
        add_stat(scrollable_frame, "Період (початок)", start_date_str)
        add_stat(scrollable_frame, "Період (кінець)", end_date_str)

        # --- 3. Блок "Статистика ряду" ---
        add_header(scrollable_frame, "СТАТИСТИКА РЯДУ")
        add_stat(scrollable_frame, "Середнє значення", f"{power_load.mean():.2f}{units}")
        add_stat(scrollable_frame, "Мінімум", f"{power_load.min():.2f}{units}")
        add_stat(scrollable_frame, "Максимум", f"{power_load.max():.2f}{units}")
        add_stat(scrollable_frame, "Стандартне відхилення", f"{power_load.std():.2f}{units}")
        add_stat(scrollable_frame, "Медіана", f"{np.median(power_load):.2f}{units}")
        
        # --- 4. Блок "Автокореляція" (Завдання 1в) ---
        add_header(scrollable_frame, "АНАЛІЗ АВТОКОРЕЛЯЦІЇ (Завдання 1в)")
        add_stat(scrollable_frame, "Коефіцієнт (ρ₁)", f"{rho_1:.4f}")
        interpretation = "Сильна позитивна" if abs(rho_1) > 0.7 else ("Помірна" if abs(rho_1) > 0.3 else "Слабка")
        add_stat(scrollable_frame, "Інтерпретація", interpretation)
        
        # --- 5. Блок "Параметри моделі / Прогноз" (Завдання 2б) ---
        forecast_block_title = "ПРОГНОЗ (Завдання 2б)" if not is_task1 else "ПАРАМЕТРИ МОДЕЛІ (для 16 точок)"
        add_header(scrollable_frame, forecast_block_title)
        
        add_stat(scrollable_frame, "Тренд (μ)", f"{mu:.4f} {units_mu}")
        add_stat(scrollable_frame, "Відхилення шуму (σ)", f"{sigma:.4f} {units_sigma}")
        add_stat(scrollable_frame, "Останнє спостереження", f"{last_val:.2f}{units}")
        
        # --- 6. Блок "Прогнозні горизонти" ---
        ttk.Label(scrollable_frame, text="Прогноз на різні горизонти (Y(t+τ) = Y(t) + μ·τ):",
                  font=('Arial', 10, 'bold'), background='#2C3E50', foreground='white').pack(anchor='w', padx=20, pady=(15, 5))
        
        forecast_horizons = [1, 2, 3, 4, 5] if is_task1 else [1, 6, 12, 24, 48]
        # Внутрішній фрейм для відступу
        forecast_frame = ttk.Frame(scrollable_frame, style='TFrame')
        forecast_frame.pack(fill='x', padx=30, pady=0, anchor='w')
        
        for tau in forecast_horizons:
            forecast = last_val + mu * tau
            rmse = sigma * np.sqrt(tau)
            ci_lower = forecast - 1.96 * rmse
            ci_upper = forecast + 1.96 * rmse
            
            # Форматуємо рядки
            tau_str = f"• {tau:2d} год:"
            val_str = f"{forecast:7.2f} ± {rmse:.2f}{units}"
            ci_str = f"[{ci_lower:.2f}, {ci_upper:.2f}]"
            
            # Фрейм для одного рядка прогнозу
            row_frame = ttk.Frame(forecast_frame, style='TFrame')
            row_frame.pack(fill='x', anchor='w')
            
            # Використовуємо 'Courier New' для табличного, вирівняного вигляду
            ttk.Label(row_frame, text=tau_str, font=('Courier New', 10, 'bold'), background='#2C3E50', foreground='white').pack(side='left', anchor='w')
            ttk.Label(row_frame, text=val_str, font=('Courier New', 10, 'bold'), background='#2C3E50', foreground='white', width=25, anchor='w').pack(side='left', anchor='w', padx=10)
            ttk.Label(row_frame, text=ci_str, font=('Courier New', 10), background='#2C3E50', foreground='#95A5A6').pack(side='left', anchor='w', expand=True)


def main():
    root = tk.Tk()
    app = EnergyAnalysisApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()