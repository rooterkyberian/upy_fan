# Makefile based on https://github.com/XenGi/washingremote/blob/70391c62e47ffa8d93671036645f6eb8b6181432/Makefile

#PORT=/dev/tty.SLAB_USBtoUART
PORT=/dev/ttyUSB0

BAUDRATE=115200
FLASH_BAUDRATE=460800
FIRMWARE=esp8266-20180511-v1.9.4.bin

ESPTOOL=esptool.py
AMPY=ampy

SOURCEDIR=src/
SOURCES := $(shell find $(SOURCEDIR) -name '*.py')

upload:
	for file in src/*py; do \
		echo $$file ; \
		$(AMPY) -p $(PORT) -b $(BAUDRATE) put $$file; \
	done

$(PORT):
	@echo " ESP at $(PORT) not found"
	@false

$(FIRMWARE):
	wget http://micropython.org/resources/firmware/$(FIRMWARE)

webrepl:
	xdg-open http://micropython.org/webrepl/

repl:
	miniterm.py $(PORT) $(BAUDRATE)

erase:
	$(ESPTOOL) --port $(PORT) erase_flash

flash: $(FIRMWARE)
	$(ESPTOOL) --port $(PORT) --baud $(FLASH_BAUDRATE) write_flash --flash_size=detect --verify 0 $(FIRMWARE)


everything:
	make erase
	sleep 1
	make flash
	sleep 3
	make upload

.PHONY: repl erase firmware everything
