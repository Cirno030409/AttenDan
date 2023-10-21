import binascii

import nfc


class CardReader:
    def connect_reader(self):
        try:
            self.clf = nfc.ContactlessFrontend("usb")
        except IOError:
            print("[NFC] reader not found.")
            return -1
        print("[NFC] reader connected.")

    def wait_for_card_touched(
        self,
    ):  # This func blocks called thread until card is touched.
        tag = self.clf.connect(rdwr={"on-connect": lambda tag: False})
        return binascii.hexlify(tag.identifier).decode()

    def disconnect_reader(self):
        print("[NFC] reader disconnected.")
        self.clf.close()
