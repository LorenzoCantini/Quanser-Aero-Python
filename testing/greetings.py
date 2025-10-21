from quanser.hardware import HIL, HILError, StringProperty

try:
    card = HIL()
    card.open("quanser_aero_usb", "0")

    try:
        manufacturer = card.get_string_property(StringProperty.MANUFACTURER, 64)
        product_name = card.get_string_property(StringProperty.PRODUCT_NAME, 64)
        model_name = card.get_string_property(StringProperty.MODEL_NAME, 64)
        serial_number = card.get_string_property(StringProperty.SERIAL_NUMBER, 64)
        firmware_version = card.get_string_property(StringProperty.FIRMWARE_VERSION, 64)

        print(f"{manufacturer} {product_name} {model_name}")
        print(f"Serial number: {serial_number}")
        print(f"Firmware version: {firmware_version}")

    except HILError as ex:
        print("Unable to get serial number. %s" % ex.get_error_message())

    finally:
        card.close()

except HILError as ex:
    print("Unable to open board. %s" % ex.get_error_message())
