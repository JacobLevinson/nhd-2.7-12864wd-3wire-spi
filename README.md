# nhd-2.7-12864wd-3wire-spi

## Overview

This repository contains the source code for the NHD-2.7-12864WD SSD1322 framebuffer driver, along with the device tree overlay (ssd1322-overlay.dts). The driver supports the NHD-2.7-12864WD series of OLED displays, which operate in 4-bit grayscale mode and interface with the system via a 3-wire SPI communication protocol.

The display has a resolution of 128x64 pixels, with each pixel represented by 4 bits. As a result, two pixels are packed into each byte. The driver provides basic framebuffer functionality, allowing the system to treat the SSD1322-based display as a framebuffer device. This enables users to write data to the display using the standard framebuffer interface.

To assist users in displaying images on the SSD1322-based framebuffer, a Python script is included that converts any input image (e.g., PNG, JPG) into the required 4-bit grayscale format for the display.

## Features

- **128x64 pixel resolution**.
- **4-bit grayscale support** (16 grayscale levels).
- **Framebuffer device**: exposes `/dev/fbX` for direct access.
- Designed for **NHD-2.7-12864WDXX** OLED displays.
- **3-wire SPI communication** for low pin count.

## Requirements

- **Raspberry Pi** or any other system with a **SPI interface**.
- SSD1322-based OLED display.

## Supported Display

- NHD-2.7-12864WDXX series (128x64 pixels, 4-bit grayscale).

## Pin Configuration

Connect the display to the Raspberry Pi's SPI pins as follows:

- **SPI_MOSI**: Connect to MOSI (Master Out Slave In).
- **SPI_SCLK**: Connect to SCLK (Serial Clock).
- **SPI_CS**: Connect to Chip Select (CS0 or CS1 depending on your configuration).

Make sure that the SPI interface is enabled in the system configuration.

## Driver Installation

To use this driver, follow these steps:

### 1. Clone the Repository

```
git clone https://github.com/JacobLevinson/nhd-2.7-12864wd-3wire-spi.git
cd nhd-2.7-12864wd-3wire-spi
```

### 2. Build the Driver

Ensure that you have the necessary kernel headers installed:

```
sudo apt-get install raspberrypi-kernel-headers build-essential
```

Then, build the driver using the `Makefile`:

```
make
```

### 3. Compile the Device Tree Overlay

The repository includes the `ssd1322-overlay.dts` file, which must be compiled into a `.dtbo` file (device tree binary overlay) for the Raspberry Pi.

Compile the overlay using the device tree compiler:

```
sudo dtc -@ -I dts -O dtb -o ssd1322-overlay.dtbo ssd1322-overlay.dts
```

### 4. Copy the Overlay to the Correct Directory

Once compiled, copy the `.dtbo` file to the appropriate directory so it can be loaded at boot:

```
sudo cp ssd1322-overlay.dtbo /boot/firmware/overlays/
```

### 5. Update the Configuration to Enable SPI and the Overlay

Open the `/boot/firmware/config.txt` and add the following lines to enable SPI and apply the SSD1322 overlay:

```
sudo nano /boot/firmware/config.txt
```

Add these lines:

```
dtparam=spi=on
dtoverlay=ssd1322-overlay
```

Save the file and reboot the system:

```
sudo reboot
```

### 6. Install the Driver

After rebooting, install the SSD1322 driver into the kernel using `insmod`:

```
sudo insmod ssd1322fb.ko
```

You should now see the framebuffer device created (e.g., `/dev/fb0`).

Verify the framebuffer device:

```
ls /dev/fb*
```

### 7. Using the Framebuffer

Once the driver is loaded, you can write directly to the framebuffer:

To clear the display, run the following command:

```
sudo dd if=/dev/zero of=/dev/fb0
```

### 8. Unload the Driver

To unload the driver, use the following command:

```
sudo rmmod ssd1322fb
```

## Wiring the Display

**Ensure that you wire the NHD-2.7-12864WD display according to the datasheet for the 3-wire SPI interface**. You can find the datasheet [here](https://newhavendisplay.com/content/specs/NHD-2.7-12864WDY3.pdf).

The following pins should be connected:

* **SPI_MOSI (DIN)**: Connect to the Master Out Slave In (MOSI) pin on your microcontroller or Raspberry Pi.
* **SPI_SCLK (CLK)**: Connect to the Serial Clock (SCLK) pin on your microcontroller or Raspberry Pi.
* **CS (Chip Select)**: Connect to the Chip Select (CS) pin, which should be tied to a GPIO pin on your microcontroller or Raspberry Pi.
* **RES (Reset)**: **Important**: The reset pin must be held high for normal operation. Ensure that the pin is tied to a high signal (3.3V or 5V).
* **VCC**: Connect to a 3.3V or 5V power source depending on your setup.
* **GND**: Connect to the ground pin of your microcontroller or Raspberry Pi.

Refer to the display's datasheet for more detailed wiring instructions specific to the NHD-2.7-12864WD for 3-wire SPI communication.


## Troubleshooting

1. **Driver Not Loading**: Ensure that SPI is enabled and the `dtoverlay` has been applied correctly. Check the logs using `dmesg` to see any error messages related to SPI or the framebuffer.
   
2. **No Framebuffer Device**: If `/dev/fbX` is not showing up, check the `dmesg` logs for errors during driver initialization.

3. **Display Not Updating**: Make sure your wiring is correct, especially the SPI, DC, and RST lines.

## License

This driver is licensed under the GNU General Public License (GPL). See the `LICENSE` file for more information.


## Python Script for Image Conversion

To make it easier to display images on the SSD1322-based framebuffer, a Python script is included in this repository. This script converts any input image into the proper 4-bit grayscale format required by the display.

### Requirements

- **Python 3**: You must have Python 3 installed on your system.
- **Pillow**: The Python Imaging Library (PIL) is required to handle the image conversion.

### Installing Python 3 and Pillow

On most systems, you can install Python 3 and the Pillow library using the following commands:

- For Ubuntu or Raspberry Pi OS:
```
sudo apt-get update
sudo apt-get install python3 python3-pip
pip3 install Pillow
```

Alternatively, if you already have `pip` installed, you can install Pillow with:
```
pip3 install Pillow
```

### Using the Script

The Python script, `convert_image_to_4bit_grayscale.py`, can be used to convert any image (e.g., PNG, JPG) into the 4-bit grayscale format required by the SSD1322 framebuffer.

To use the script, run the following command:

```
python3 convert_image_to_4bit_grayscale.py <input_image> [output_file]
```

- `<input_image>`: This is the path to the input image file. It can be in PNG, JPG, or other common image formats.
- `[output_file]`: (Optional) The path to the output file. If not provided, the output file will be named the same as the input file, with `-4bit.bin` appended.

#### Example

To convert an image called `logo.png` to the 4-bit format and save it as `logo-4bit.bin`, run:

```
python3 convert_image_to_4bit_grayscale.py logo.png
```

To specify a custom output file:

```
python3 convert_image_to_4bit_grayscale.py logo.png custom_output.bin
```

The resulting `.bin` file can then be written to the framebuffer device using:

```
sudo dd if=logo-4bit.bin of=/dev/fb0 bs=4096 count=1
```

This will display the image on the OLED screen via the framebuffer device.
