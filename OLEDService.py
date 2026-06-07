import subprocess
import logging
from PIL import ImageDraw, ImageFont
from luma.oled.device import sh1106
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.core.error import DeviceNotFoundError

class OLEDService:
    def __init__(self):
        self.devices = {}

    def set_mux_channel(self, channel):
        mask = 1 << channel
        subprocess.run(["i2cset", "-y", "1", "0x70", f"0x{mask:02x}"])

    def get_device(self, channel):
        if channel not in self.devices:
            try:
                self.set_mux_channel(channel)
                serial = i2c(port=1, address=0x3C)
                self.devices[channel] = sh1106(serial)
                logging.info(f"OLED initialized on channel {channel}")
            except (DeviceNotFoundError, OSError) as e:
                logging.error(f"Failed to initialize OLED on channel {channel}: {e}")
                self.devices[channel] = None
        return self.devices[channel]

    def draw_text(self, channel, text):
        dev = self.get_device(channel)
        if dev is None:
            logging.error(f"Cannot draw on channel {channel}: Device not available")
            return False
        
        try:
            self.set_mux_channel(channel)
            with canvas(dev) as draw:
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 40)
                except IOError:
                    font = ImageFont.load_default()
                
                bbox = draw.textbbox((0, 0), text, font=font)
                x = (128 - (bbox[2] - bbox[0])) // 2
                y = (64 - (bbox[3] - bbox[1])) // 2 - bbox[1]
                draw.text((x, y), text, font=font, fill="white")
            return True
        except (DeviceNotFoundError, OSError) as e:
            logging.error(f"Error drawing on channel {channel}: {e}")
            self.devices[channel] = None # Reset
            return False

    def clear_all(self):
        for channel in range(4):
            dev = self.get_device(channel)
            if dev:
                try:
                    self.set_mux_channel(channel)
                    dev.clear()
                    logging.info(f"Cleared OLED on channel {channel}")
                except Exception as e:
                    logging.error(f"Error clearing OLED on channel {channel}: {e}")
