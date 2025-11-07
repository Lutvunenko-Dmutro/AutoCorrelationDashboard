import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def load_test_data():
    """
    Завантажує тестові дані з Задачі 1.
    """
    power_load_list = [1.6, 0.8, 1.2, 0.5, 0.9, 1.1, 1.1, 0.6, 1.5, 0.8, 0.9, 1.2, 0.5, 1.3, 0.8, 1.2]
    power_load = np.array(power_load_list)
    
    n_hours = len(power_load_list)
    start_date = datetime(2024, 11, 1, 0, 0)
    
    # Генеруємо список об'єктів datetime
    dates = _generate_dates_recursive(start_date, n_hours, 0, [])
    
    return dates, power_load

def load_data_from_csv(filepath):
    """
    Завантажує та обробляє дані з CSV файлу.
    Очікує стовпці: 'мітка_часу' та 'навантаження_мвт'
    """
    try:
        df = pd.read_csv(filepath)
        
        # --- Перевірка необхідних стовпців ---
        if 'мітка_часу' not in df.columns:
            raise ValueError("CSV файл повинен мати стовпець 'мітка_часу'")
        if 'навантаження_мвт' not in df.columns:
            raise ValueError("CSV файл повинен мати стовпець 'навантаження_мвт'")

        # --- Обробка даних ---
        # 1. Перетворюємо стовпець з датами у формат datetime
        df['мітка_часу'] = pd.to_datetime(df['мітка_часу'])
        
        # 2. Сортуємо дані про всяк випадок
        df = df.sort_values(by='мітка_часу')
        
        # 3. Витягуємо дані у форматі, який очікує програма
        # plotting.py очікує список/масив дат та масив значень
        dates = df['мітка_часу'].tolist() # Список об'єктів datetime
        power_load = df['навантаження_мвт'].values # Масив numpy
        
        return dates, power_load
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не знайдено: {filepath}")
    except Exception as e:
        raise Exception(f"Помилка читання або обробки CSV: {e}")


def _generate_dates_recursive(start_date, total_hours, current_hour, dates_list):
    """
    Допоміжна рекурсивна функція для генерації списку дат.
    """
    if current_hour >= total_hours:
        return dates_list
    dates_list.append(start_date + timedelta(hours=current_hour))
    return _generate_dates_recursive(start_date, total_hours, current_hour + 1, dates_list)

def calculate_autocorrelation(power_load, max_lag=None):
    """
    Розраховує параметри автокореляції.
    """
    n = len(power_load)
    
    # Робимо max_lag динамічним
    if max_lag is None:
        # Гарне значення за замовчуванням для ACF-графіка
        max_lag = min(48, n // 2) 
        
    if max_lag >= n:
        max_lag = n - 1 # Не може бути більше за кількість даних

    y_t = power_load[:-1]
    y_t_plus_1 = power_load[1:]
    rho_1 = np.corrcoef(y_t, y_t_plus_1)[0, 1]
    
    acf_values = []
    lag = 0
    while lag <= max_lag:
        if lag == 0:
            acf_values.append(1.0)
        else:
            y1 = power_load[:-lag]
            y2 = power_load[lag:]
            correlation = np.corrcoef(y1, y2)[0, 1]
            acf_values.append(correlation)
        lag += 1
    
    return y_t, y_t_plus_1, rho_1, acf_values

def calculate_forecast_parameters(power_load):
    """
    Розраховує параметри для моделі випадкового блукання з трендом.
    """
    n_hours = len(power_load)
    if n_hours < 2:
        return 0, 0, power_load[-1] # Недостатньо даних
        
    mu_estimate = (power_load[-1] - power_load[0]) / (n_hours - 1)
    sigma_estimate = np.std(np.diff(power_load))
    last_value = power_load[-1]
    
    return mu_estimate, sigma_estimate, last_value

def generate_forecast_data(last_date, last_value, mu_estimate, sigma_estimate, forecast_hours=48):
    """
    Генерує дані для прогнозу (модель випадкового блукання).
    """
    # Повертаємо 48 годин за замовчуванням
    forecast_dates = _generate_forecast_dates(last_date, forecast_hours, 1, [])
    forecast_values = _generate_forecast_values(last_value, mu_estimate, forecast_hours, 1, [])
    forecast_rmse = _generate_forecast_rmse(sigma_estimate, forecast_hours, 1, [])
    
    return forecast_dates, forecast_values, forecast_rmse

def _generate_forecast_dates(last_date, total_hours, current_hour, dates_list):
    if current_hour > total_hours:
        return dates_list
    # Переконуємось, що last_date є datetime об'єктом
    if not isinstance(last_date, datetime):
        # Якщо це numpy.datetime64 або щось інше, конвертуємо
        last_date = pd.to_datetime(last_date).to_pydatetime()
        
    dates_list.append(last_date + timedelta(hours=current_hour))
    return _generate_forecast_dates(last_date, total_hours, current_hour + 1, dates_list)

def _generate_forecast_values(last_value, mu_estimate, total_hours, current_hour, values_list):
    if current_hour > total_hours:
        return values_list
    values_list.append(last_value + mu_estimate * current_hour)
    return _generate_forecast_values(last_value, mu_estimate, total_hours, current_hour + 1, values_list)

def _generate_forecast_rmse(sigma_estimate, total_hours, current_hour, rmse_list):
    if current_hour > total_hours:
        return rmse_list
    rmse_list.append(sigma_estimate * np.sqrt(current_hour))
    return _generate_forecast_rmse(sigma_estimate, total_hours, current_hour + 1, rmse_list)
