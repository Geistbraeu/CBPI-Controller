import time
import subprocess
import requests
from PIL import Image, ImageDraw, ImageFont
from luma.oled.device import sh1106
from luma.core.interface.serial import i2c
from luma.core.render import canvas

# --- НАСТРОЙКИ ---
SENSOR_ID = "MjirdhbTQNi7DX9MTFqVJF"
URL = f"http://localhost:8000/sensor/{SENSOR_ID}"
INTERVAL = 0.5  # Полсекунды

# Функция быстрого переключения каналов TCA9548A через i2cset
def set_mux_channel(channel):
    mask = 1 << channel
    subprocess.run(["i2cset", "-y", "1", "0x70", f"0x{mask:02x}"])

print("Инициализация экрана на канале 3...")

# Инициализируем Экран на Канале 3
set_mux_channel(3)
serial_mux3 = i2c(port=1, address=0x3C)
oled1 = sh1106(serial_mux3)

def get_temperature():
    """Запрос данных из cbpi4"""
    try:
        # Небольшой таймаут, чтобы скрипт не зависал, если cbpi4 занят
        response = requests.get(URL, timeout=0.4)
        if response.status_code == 200:
            data = response.json()
            value = data.get("value")
            if value is not None:
                return f"{round(float(value), 1)} °C"
        else:
            print(f"Ошибка сервера cbpi4: {response.status_code}")
    except Exception as e:
        print(f"Ошибка сети/запроса: {e}")
    return None

def draw_huge_number(device, text_str):
    """Отрисовка текста по центру экрана"""
    with canvas(device) as draw:
        try:
            # Используем ваш проверенный крупный шрифт
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 36)
        except IOError:
            font = ImageFont.load_default()
            
        # Расчет центрирования
        bbox = draw.textbbox((0, 0), text_str, font=font)
        x = (128 - (bbox[2] - bbox[0])) // 2
        y = (64 - (bbox[3] - bbox[1])) // 2 - bbox[1]
        
        draw.text((x, y), text_str, font=font, fill="white")

def main():
    print(f"Запущен мониторинг датчика {SENSOR_ID}. Вывод на OLED (Mux Ch 3)...")
    
    last_text = None
    
    try:
        while True:
            current_text = get_temperature()
            
            if current_text is not None:
                # Обновляем экран только если значение изменилось
                if current_text != last_text:
                    last_text = current_text
                    
                    # Переключаем мультиплексор на нужный канал перед выводом
                    set_mux_channel(3)
                    draw_huge_number(oled1, current_text)
            else:
                # Если датчик недоступен, выводим ошибку
                if last_text != "ERR":
                    last_text = "ERR"
                    set_mux_channel(3)
                    draw_huge_number(oled1, "Ошибка")
            
            time.sleep(INTERVAL)
            
    except KeyboardInterrupt:
        print("\nМониторинг остановлен.")
        # При выходе аккуратно гасим экран
        set_mux_channel(3)
        with canvas(oled1) as draw:
            pass 

if __name__ == "__main__":
    main()