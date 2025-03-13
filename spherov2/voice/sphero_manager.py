# sphero_manager.py

from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.scanner import ToyNotFoundError  # Import the exception

class SpheroManager:
    def __init__(self):
        self.toy = None
        self.api = None

    def connect(self):
        """Scan for a Sphero Mini and manually enter its context."""
        if self.api:
            print("Sphero is already connected; skipping re-scan.")
            return
        # else proceed with scanning
        
        try:
            self.toy = scanner.find_Mini(timeout=5.0)
        except ToyNotFoundError as e:
            print("No Sphero found. Please ensure the device is powered on and in range.")
            self.toy = None
            self.api = None
            return
        if self.toy:
            self.api = SpheroEduAPI(self.toy)
            self.api.__enter__()  # Manually call __enter__
            print("Sphero connected in a persistent context!")
        else:
            print("No Sphero found during scanning.")

    def disconnect(self):
        """Exit the context manager if connected."""
        if self.api:
            self.api.__exit__(None, None, None)  # Manually call __exit__
            self.api = None
            print("Sphero disconnected (context closed).")

    def roll(self, angle, speed, duration):
        """Roll the Sphero, if connected."""
        if self.api:
            self.api.roll(angle, speed, duration)
        else:
            print("No Sphero connection available to roll.")