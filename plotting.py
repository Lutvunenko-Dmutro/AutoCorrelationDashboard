import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

def create_timeseries_plot(dates, power_load):
    fig = Figure(figsize=(10, 6), facecolor='#ECF0F1')
    ax = fig.add_subplot(111)
    
    plot_kwargs = {
        'linewidth': 2,
        'color': '#2E86AB'
    }
    if len(dates) < 500: 
        plot_kwargs['marker'] = 'o'
        plot_kwargs['markersize'] = 2
        plot_kwargs['markerfacecolor'] = '#A23B72'
        
    ax.plot(dates, power_load, **plot_kwargs)
    
    ax.set_facecolor('#F8F9FA')
    ax.set_xlabel('Час', fontsize=12, fontweight='bold', color='#2C3E50')
    ax.set_ylabel('Потужність навантаження (МВт)', fontsize=12, fontweight='bold', color='#2C3E50')
    
    # Динамічний заголовок
    title_suffix = f"({len(dates)} спостережень)" if len(dates) > 50 else ""
    ax.set_title(f'Часовий ряд потужності навантаження {title_suffix}', 
                fontsize=14, fontweight='bold', pad=20, color='#2C3E50')
    ax.grid(True, alpha=0.3, linestyle='--', color='#7F8C8D')
    
    stats_text = f"Середнє: {power_load.mean():.1f}\nМакс: {power_load.max():.1f}\nМін: {power_load.min():.1f}"
    # Адаптуємо одиниці виміру для малих значень (Завдання 1)
    if power_load.mean() < 10: 
        stats_text = stats_text.replace("МВт", "")
        ax.set_ylabel('Значення', fontsize=12, fontweight='bold', color='#2C3E50')

    ax.annotate(stats_text, xy=(0.02, 0.98), xycoords='axes fraction', 
               bbox=dict(boxstyle="round,pad=0.3", facecolor='#3498DB', alpha=0.8),
               fontsize=10, color='white', verticalalignment='top')
    
    fig.tight_layout()
    return fig

def create_autocorrelation_plot(dates, y_t, y_t_plus_1, acf_values, rho_1, power_load):
    fig = Figure(figsize=(12, 6), facecolor='#ECF0F1')
    fig.suptitle('Аналіз Автокореляції', fontsize=16, fontweight='bold', color='#2C3E50')
    
    ax1 = fig.add_subplot(121)
    
    n_show = 500 # Макс. точок для цього графіка

    # Готуємо дані для y(t)
    # y_t має на 1 елемент менше, ніж dates. Треба брати dates[:-1]
    dates_for_yt = dates[:-1]
    y_t_data = y_t
    
    # Готуємо дані для y(t+1)
    # y_t_plus_1 має на 1 елемент менше, ніж dates. Треба брати dates[1:]
    dates_for_yt1 = dates[1:]
    y_t_plus_1_data = y_t_plus_1
    
    # Застосовуємо зріз n_show, якщо даних забагато
    # Тепер ми ріжемо і X, і Y, тож їх довжина завжди збігається
    if len(dates_for_yt) > n_show:
        dates_for_yt = dates_for_yt[:n_show]
        y_t_data = y_t_data[:n_show]
        
    if len(dates_for_yt1) > n_show:
        dates_for_yt1 = dates_for_yt1[:n_show]
        y_t_plus_1_data = y_t_plus_1_data[:n_show]

    ax1.plot(dates_for_yt, y_t_data, label='y(t)', linewidth=2, color='#2E86AB', alpha=0.8)
    ax1.plot(dates_for_yt1, y_t_plus_1_data, label='y(t+1)', linewidth=2, 
            color='#E74C3C', alpha=0.8, linestyle='--')
    
    ax1.set_facecolor('#F8F9FA')
    ax1.set_xlabel('Час (або перші 500 точок)', fontsize=11, fontweight='bold', color='#2C3E50')
    
    # Адаптуємо підпис осі
    y_label = 'Потужність (МВт)' if y_t.mean() > 10 else 'Значення'
    ax1.set_ylabel(y_label, fontsize=11, fontweight='bold', color='#2C3E50')
    
    ax1.set_title('Порівняння y(t) та y(t+1)', fontsize=12, fontweight='bold', color='#2C3E50')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3, linestyle='--', color='#7F8C8D')
    
    ax2 = fig.add_subplot(122)
    markers, stemlines, baseline = ax2.stem(range(len(acf_values)), acf_values, 
                                           linefmt='#2E86AB', markerfmt='o', basefmt='gray')
    plt.setp(stemlines, linewidth=2)
    plt.setp(markers, markersize=4, color='#E74C3C')
    
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    # Довірчий інтервал має сенс лише якщо точок достатньо (напр. > 10)
    if len(power_load) > 10:
        ax2.axhline(y=1.96/np.sqrt(len(power_load)), color='red', linestyle='--', 
                   linewidth=1, label='95% довірчий інтервал')
        ax2.axhline(y=-1.96/np.sqrt(len(power_load)), color='red', linestyle='--', linewidth=1)
        ax2.legend(fontsize=9)

    ax2.set_facecolor('#F8F9FA')
    ax2.set_xlabel(f'Лаг (години, макс. {len(acf_values)-1})', fontsize=11, fontweight='bold', color='#2C3E50')
    ax2.set_ylabel('Автокореляція', fontsize=11, fontweight='bold', color='#2C3E50')
    ax2.set_title(f'Автокореляційна функція (ACF)\nρ₁ = {rho_1:.4f}', 
                 fontsize=12, fontweight='bold', color='#2C3E50')
    ax2.grid(True, alpha=0.3, linestyle='--', color='#7F8C8D')
    
    fig.tight_layout()
    return fig

def create_scatter_plot(y_t, y_t_plus_1, rho_1):
    fig = Figure(figsize=(10, 6), facecolor='#ECF0F1')
    ax = fig.add_subplot(111)
    
    # --- ОНОВЛЕНА ЛОГІКА ---
    # Якщо точок забагато, обираємо випадкову вибірку, щоб графік не "завис"
    n_points = len(y_t)
    if n_points > 2000:
        indices = np.random.choice(n_points, 2000, replace=False)
        y_t_sample = y_t[indices]
        y_t_plus_1_sample = y_t_plus_1[indices]
        title_suffix = f'\n(на базі 2000 випадкових точок)'
        point_size = 20
        point_alpha = 0.5
    else:
        y_t_sample = y_t
        y_t_plus_1_sample = y_t_plus_1
        title_suffix = ''
        point_size = 50
        point_alpha = 0.7
    # --- КІНЕЦЬ ОНОВЛЕННЯ ---
    
    scatter = ax.scatter(y_t_sample, y_t_plus_1_sample, alpha=point_alpha, s=point_size, c=range(len(y_t_sample)), 
                       cmap='viridis', edgecolors='black', linewidth=0.1)
    ax.set_facecolor('#F8F9FA')
    
    # Адаптуємо підписи
    x_label = 'y(t) - Потужність в момент t (МВт)' if y_t.mean() > 10 else 'y(t) - Значення в момент t'
    y_label = 'y(t+1) - Потужність в момент t+1 (МВт)' if y_t.mean() > 10 else 'y(t+1) - Значення в момент t+1'
    
    ax.set_xlabel(x_label, fontsize=12, fontweight='bold', color='#2C3E50')
    ax.set_ylabel(y_label, fontsize=12, fontweight='bold', color='#2C3E50')
    ax.set_title(f'Діаграма розсіювання: y(t+1) від y(t)\nКоефіцієнт кореляції: {rho_1:.4f}{title_suffix}', 
                fontsize=14, fontweight='bold', pad=20, color='#2C3E50')
    
    # Розраховуємо регресію на повних даних, щоб була точна
    z = np.polyfit(y_t, y_t_plus_1, 1)
    p = np.poly1d(z)
    x_line = np.linspace(y_t.min(), y_t.max(), 100)
    ax.plot(x_line, p(x_line), "r--", linewidth=2, 
           label=f'Лінія регресії: y={z[0]:.3f}x+{z[1]:.1f}')
    
    ax.plot([y_t.min(), y_t.max()], [y_t.min(), y_t.max()], 'k:', 
           linewidth=1.5, label='y(t+1) = y(t)', alpha=0.5)
    
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--', color='#7F8C8D')
    
    interpretation = "Сильна позитивна кореляція" if abs(rho_1) > 0.7 else ("Помірна кореляція" if abs(rho_1) > 0.3 else "Слабка кореляція")
    ax.annotate(f'Інтерпретація: {interpretation}', 
               xy=(0.02, 0.98), xycoords='axes fraction',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='#27AE60', alpha=0.8),
               fontsize=10, color='white', verticalalignment='top')
    
    fig.tight_layout()
    return fig

def create_forecast_plot(dates, power_load, forecast_dates, forecast_values, forecast_rmse, mu_estimate, sigma_estimate, last_value):
    fig = Figure(figsize=(10, 6), facecolor='#ECF0F1')
    ax = fig.add_subplot(111)
    
    # Визначаємо, скільки останніх годин історії показати
    # Для Завдання 1 (16 точок) покажемо всі 16.
    # Для CSV покажемо 168.
    lookback_hours = 168 
    if len(dates) < lookback_hours:
        lookback_hours = len(dates)
    
    # Обрізаємо історичні дані, щоб показати лише останню частину
    historical_dates_slice = dates[-lookback_hours:]
    historical_power_slice = power_load[-lookback_hours:]
    
    # Малюємо лише "зріз" даних
    label_text = 'Історичні дані'
    if len(dates) > lookback_hours:
        label_text = f'Історичні дані (останні {lookback_hours} год.)'
        
    ax.plot(historical_dates_slice, historical_power_slice, linewidth=2, color='#2E86AB', 
           label=label_text, marker='o', markersize=3)
    
    ax.plot(forecast_dates, forecast_values, linewidth=2, color='#E67E22', 
           label='Прогноз', linestyle='--', marker='s', markersize=3)
    
    ci_lower = []
    ci_upper = []
    i = 0
    while i < len(forecast_values):
        ci_lower.append(forecast_values[i] - 1.96 * forecast_rmse[i])
        ci_upper.append(forecast_values[i] + 1.96 * forecast_rmse[i])
        i += 1
    
    ax.fill_between(forecast_dates, ci_lower, ci_upper, alpha=0.3, 
                   color='#E67E22', label='95% довірчий інтервал')
    
    ax.axvline(x=dates[-1], color='red', linestyle=':', linewidth=2, 
              label='Момент прогнозування')
    
    ax.set_facecolor('#F8F9FA')
    ax.set_xlabel('Час', fontsize=12, fontweight='bold', color='#2C3E50')
    
    # Адаптуємо підпис осі
    y_label = 'Потужність навантаження (МВт)' if power_load.mean() > 10 else 'Значення'
    ax.set_ylabel(y_label, fontsize=12, fontweight='bold', color='#2C3E50')

    ax.set_title('Прогнозування випадкового блукання з трендом', 
                fontsize=14, fontweight='bold', pad=20, color='#2C3E50')
    ax.legend(fontsize=10, loc='best')
    ax.grid(True, alpha=0.3, linestyle='--', color='#7F8C8D')
    
    # Адаптуємо одиниці виміру
    units = "МВт/год" if power_load.mean() > 10 else "/год"
    sigma_units = "МВт" if power_load.mean() > 10 else ""
    
    model_info = f"Модель: Y(t+τ) = Y(t) + μ·τ\nμ = {mu_estimate:.3f} {units}\nσ = {sigma_estimate:.2f} {sigma_units}"
    ax.annotate(model_info, xy=(0.02, 0.02), xycoords='axes fraction',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='#8E44AD', alpha=0.8),
               fontsize=9, color='white', verticalalignment='bottom')
    
    fig.tight_layout()
    return fig