import os
import pytest
from my_package.module1 import SimulatedDevice

def setup_function():
    """Reset the initial version to 1 before each test."""
    os.environ["INITIAL_VERSION"] = "1"

def test_upgrade_not_allowed_for_same_version():
    """ Upgrade should fail if the new version is the same as current."""
    device = SimulatedDevice()
    device.set_state("Idle")
    result = device.request_upgrade(1)
    assert result is False
    assert device.get_last_upgrade_result() == "failure"

def test_upgrade_successful():
    """Upgrade should succeed if all conditions are met."""
    device = SimulatedDevice()
    device.set_state("Idle")
    result = device.request_upgrade(2)
    assert result is True
    assert device.get_current_version() == 2
    assert device.get_last_upgrade_result() == "success"

def test_upgrade_fails_if_not_idle():
    """Upgrade should fail if the device is not in Idle state."""
    device = SimulatedDevice()
    device.set_state("Positioning")
    result = device.request_upgrade(2)
    assert result is False
    assert device.get_last_upgrade_result() == "failure"

def test_upgrade_fails_if_no_internet():
    """ Upgrade should fail if internet is not available."""
    device = SimulatedDevice()
    device.set_state("Idle")
    device.internet_available = False
    result = device.request_upgrade(2)
    assert result is False
    assert device.get_last_upgrade_result() == "failure"
    assert device.state == "Idle"

def test_upgrade_fails_if_power_lost():
    """Upgrade should fail if the device loses power during upgrade."""
    device = SimulatedDevice()
    device.set_state("Idle")
    device.powered_on = False
    result = device.request_upgrade(2)
    assert result is False
    assert device.get_last_upgrade_result() == "failure"
    assert device.state == "Idle"

def test_downgrade_is_allowed():
    """Downgrade should be allowed if the version is lower. """
    os.environ["INITIAL_VERSION"] = "3"
    device = SimulatedDevice()
    device.set_state("Idle")
    result = device.request_upgrade(2)
    assert result is True
    assert device.get_current_version() == 2
    assert device.get_last_upgrade_result() == "success"

def test_upgrade_fails_due_to_timeout():
    """Upgrade should fail if a timeout is simulated."""
    device = SimulatedDevice()
    device.set_state("Idle")
    result = device.request_upgrade(2, simulate_timeout=True)
    assert result is False
    assert device.get_last_upgrade_result() == "failure"
    assert device.state == "Idle"

def test_upgrade_fails_if_already_downloading():
    """ Upgrade should not be allowed if already in Downloading state."""
    device = SimulatedDevice()
    device.set_state("Downloading")
    result = device.request_upgrade(2)
    assert result is False
    assert device.get_last_upgrade_result() == "failure"

def test_upgrade_fails_if_not_enough_memory():
    """Upgrade should fail if there's not enough memory available."""
    device = SimulatedDevice()
    device.set_state("Idle")
    device.memory_free = 10  # less than update_size
    result = device.request_upgrade(2)
    assert result is False
    assert device.get_last_upgrade_result() == "failure"
    assert device.state == "Idle"
