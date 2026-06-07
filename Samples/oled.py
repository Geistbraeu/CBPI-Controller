import time
import subprocess
import logging
from PIL import Image, ImageDraw, ImageFont
from luma.oled.device import sh1106
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.core.error import DeviceNotFoundError

# Быстрое переключение каналов
def set_mux_channel(channel):
    mask = 1 << channel
    subprocess.run(["i2cset", "-y", "1", "0x70", f"0x{mask:02x}"])

print("Инициализация экранов...")
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def create_oled(channel):
    """Попытаться создать устройство на указанном канале MUX. Возвращает устройство или None."""
    try:
        set_mux_channel(channel)
        serial = i2c(port=1, address=0x3C)
        dev = sh1106(serial)
        logging.info("OLED initialized on channel %d", channel)
        return dev
    except (DeviceNotFoundError, OSError) as e:
        logging.warning("OLED on channel %d not available: %s", channel, e)
        return None


# динамический список дисплеев: индекс 0..3 соответствуют каналам 0..3
oleds = [create_oled(ch) for ch in range(4)]


def draw_huge_number(device, number_str):
    with canvas(device) as draw:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 40)
        except IOError:
            font = ImageFont.load_default()
            
        bbox = draw.textbbox((0, 0), number_str, font=font)
        x = (128 - (bbox[2] - bbox[0])) // 2
        y = (64 - (bbox[3] - bbox[1])) // 2 - bbox[1]
        draw.text((x, y), number_str, font=font, fill="white")

# Выводим цифры один раз (попытка, с переинициализацией при необходимости)
initial_texts = ["11.1 °C", "22.2 °C", "33.3 °C", "44.4 °C"]
for idx, txt in enumerate(initial_texts):
    if oleds[idx] is None:
        oleds[idx] = create_oled(idx)
    if oleds[idx] is not None:
        try:
            set_mux_channel(idx)
            draw_huge_number(oleds[idx], txt)
        except (DeviceNotFoundError, OSError) as e:
            logging.warning("Error drawing on channel %d: %s", idx, e)
            oleds[idx] = None
    else:
        logging.info("Skipping initial draw for channel %d (no device)", idx)

print("Запуск одновременного линейного демо (5 секунд). Нажмите Ctrl+C...")

STEPS = 100
# Суммарное время на шаг (с учетом вызова i2cset) должно быть около 0.05 сек
DELAY = 0.05 

try:
    while True:
        # === ПЕРВАЯ ПОЛОВИНА ЦИКЛА (2.5 сек) ===
        # Экран 1: 0 -> 255 | Экран 2: 255 -> 0
        for step in range(STEPS):
            val_up = int((step / (STEPS - 1)) * 255)
            val_down = 255 - val_up
            
            # Быстро отправляем контраст на Экраны (проверяем и переинициализируем при необходимости)
            # Экран 1
            if oleds[0] is None:
                oleds[0] = create_oled(0)
            if oleds[0] is not None:
                try:
                    set_mux_channel(0)
                    oleds[0].contrast(val_up)
                except (DeviceNotFoundError, OSError) as e:
                    logging.warning("OLED 0 lost during contrast(): %s", e)
                    oleds[0] = None

            # Экран 3 (индекс 2)
            if oleds[2] is None:
                oleds[2] = create_oled(2)
            if oleds[2] is not None:
                try:
                    set_mux_channel(2)
                    oleds[2].contrast(val_up)
                except (DeviceNotFoundError, OSError) as e:
                    logging.warning("OLED 2 lost during contrast(): %s", e)
                    oleds[2] = None

            # Экран 2 (индекс 1)
            if oleds[1] is None:
                oleds[1] = create_oled(1)
            if oleds[1] is not None:
                try:
                    set_mux_channel(1)
                    oleds[1].contrast(val_down)
                except (DeviceNotFoundError, OSError) as e:
                    logging.warning("OLED 1 lost during contrast(): %s", e)
                    oleds[1] = None

            # Экран 4 (индекс 3)
            if oleds[3] is None:
                oleds[3] = create_oled(3)
            if oleds[3] is not None:
                try:
                    set_mux_channel(3)
                    oleds[3].contrast(val_down)
                except (DeviceNotFoundError, OSError) as e:
                    logging.warning("OLED 3 lost during contrast(): %s", e)
                    oleds[3] = None
            
            time.sleep(DELAY)

        # === ВТОРАЯ ПОЛОВИНА ЦИКЛА (2.5 сек) ===
        # Экран 1: 255 -> 0 | Экран 2: 0 -> 255
        for step in range(STEPS):
            val_down = int((1 - (step / (STEPS - 1))) * 255)
            val_up = 255 - val_down
            
            # Вторая половина: зеркально (переинициализация при необходимости)
            if oleds[0] is None:
                oleds[0] = create_oled(0)
            if oleds[0] is not None:
                try:
                    set_mux_channel(0)
                    oleds[0].contrast(val_down)
                except (DeviceNotFoundError, OSError) as e:
                    logging.warning("OLED 0 lost during contrast(): %s", e)
                    oleds[0] = None

            if oleds[2] is None:
                oleds[2] = create_oled(2)
            if oleds[2] is not None:
                try:
                    set_mux_channel(2)
                    oleds[2].contrast(val_down)
                except (DeviceNotFoundError, OSError) as e:
                    logging.warning("OLED 2 lost during contrast(): %s", e)
                    oleds[2] = None

            if oleds[1] is None:
                oleds[1] = create_oled(1)
            if oleds[1] is not None:
                try:
                    set_mux_channel(1)
                    oleds[1].contrast(val_up)
                except (DeviceNotFoundError, OSError) as e:
                    logging.warning("OLED 1 lost during contrast(): %s", e)
                    oleds[1] = None

            if oleds[3] is None:
                oleds[3] = create_oled(3)
            if oleds[3] is not None:
                try:
                    set_mux_channel(3)
                    oleds[3].contrast(val_up)
                except (DeviceNotFoundError, OSError) as e:
                    logging.warning("OLED 3 lost during contrast(): %s", e)
                    oleds[3] = None
            
            time.sleep(DELAY)

except KeyboardInterrupt:
    print("\nВозврат к стандартной яркости.")
    for idx in range(4):
        if oleds[idx] is None:
            oleds[idx] = create_oled(idx)
        if oleds[idx] is not None:
            try:
                set_mux_channel(idx)
                oleds[idx].contrast(255)
            except (DeviceNotFoundError, OSError) as e:
                logging.warning("OLED %d lost during cleanup(): %s", idx, e)
                oleds[idx] = None
    set_mux_channel(4)
    
