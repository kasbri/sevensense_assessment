import os

class SimulatedDevice:
    """
    Simulates a device that can perform software upgrades and downgrades.
    Includes logic for OTA upgrade steps, power loss, memory limits, and dual partitions.
    """

    STATES = ["Positioning", "Idle", "Downloading", "Upgrading"]

    def __init__(self):
        self.current_version = int(os.environ.get("INITIAL_VERSION", 1))
        self.state = "Idle"
        self.last_upgrade_status = None
        self.internet_available = True
        self.powered_on = True

        # Simulated memory
        self.memory_free = 100  # in MB
        self.update_size = 30   # size of update in MB

        self.active_partition = "A"
        self.inactive_partition = "B"
        self.image_on_B = None  # stores version being written

    def get_current_version(self):
        """Return the current active software version."""
        return self.current_version

    def get_last_upgrade_result(self):
        """Return the result of the last upgrade attempt."""
        return self.last_upgrade_status

    def is_upgrade_valid(self, new_version):
        """Check if the new version is different from the current one."""
        return new_version != self.current_version

    def set_state(self, new_state):
        """Set the device to a specific state if it's valid."""
        if new_state in self.STATES:
            self.state = new_state

    def request_upgrade(self, new_version, simulate_timeout=False):
        """
        Tries to upgrade the device to a new version.
        Has checks for state, internet, power, timeout, and memory.
        Simulates dual-partition logic with A/B switch.
        """
        if self.state != "Idle":
            self.last_upgrade_status = "failure"
            return False

        if not self.is_upgrade_valid(new_version):
            self.last_upgrade_status = "failure"
            return False

        self.state = "Downloading"

        if not self.internet_available:
            self.last_upgrade_status = "failure"
            self.state = "Idle"
            return False

        if self.memory_free < self.update_size:
            self.last_upgrade_status = "failure"
            self.state = "Idle"
            return False

        self.state = "Upgrading"

        if simulate_timeout:
            self.last_upgrade_status = "failure"
            self.state = "Idle"
            return False

        if not self.powered_on:
            self.last_upgrade_status = "failure"
            self.state = "Idle"
            return False

        # Write image to inactive partition
        self.image_on_B = new_version

        # Simulate successful switch
        self.active_partition = self.inactive_partition
        self.current_version = self.image_on_B
        self.image_on_B = None

        self.last_upgrade_status = "success"
        self.state = "Idle"
        return True
