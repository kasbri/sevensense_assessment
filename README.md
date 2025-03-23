# OTA Upgrade Simulation

This is a simple simulation of an over-the-air (OTA) upgrade system for a robot device.  
The project includes a Python class that simulates the device and a set of tests that check if the upgrade process works.

---

## Project Structure

```
my_package/
├── python/
│   └── my_package/
│       ├── __init__.py
│       └── module1.py            # Simulated device
├── tests/
│   └── test_module1.py           # Test cases using pytest
└── README.md                     # This file
```

---

## What It Does

- Simulates a device with software that can be upgraded or downgraded.
- The upgrade process has two steps: Downloading and Upgrading.
- The upgrade only works if:
  - The device is in the "Idle" state
  - There is internet
  - The device has power
  - The version is different (upgrade or downgrade)
- It also simulates timeout and failure cases.

---

## Assumptions

- No real-time simulation is used. I did not use time.sleep() or any actual waiting. Instead, I simulate timing-based behavior (like timeouts) using flags such as simulate_timeout = True.
- The device upgrade process is represented as two logical steps (Downloading and Upgrading) by changing the state attribute inside the SimulatedDevice class.
- Upgrade failures are handled based on simple condition checks: internet status, power status, wrong state, and timeouts.
- The simulated device doesn’t persist any data or logs — it only keeps the current version and the result of the last upgrade (as "success" or "failure").
- If the upgrade or downgrade version is the same as the current version, the request is rejected.
- Downgrades are allowed as long as the new version is different from the current one.
- The initial version is passed via an environment variable INITIAL_VERSION. If not provided, it defaults to 1.
- I assume the device starts in the "Idle" state by default, and the test manually sets it to other states as needed.
- The power loss and timeout are treated similarly: both cause the upgrade to fail if they happen after the "Downloading" step.
- There is no retry logic or resume mechanism implemented for failed upgrades, since this wasn't explicitly required.

---

## Notes

While working on this task, I followed the instructions closely and implemented all the required logic and tests. I used a single class to simulate the device behavior, and a set of pytest tests to verify functionality.

I also added a few realistic improvements inspired by how OTA upgrades work in real embedded systems:

### Enhancements I Added

- Memory Limit Simulation
  I added a memory_free attribute and an update_size. The upgrade fails if there isn't enough memory available to hold the new image. This simulates limited flash storage on embedded systems.

- Dual Partition Upgrade Logic (A/B system)  
  Real OTA systems often write updates to an inactive partition (e.g., "B") and switch over only if the upgrade succeeds. I simulated this by storing the new version in "mage_on_B", then switching "active_partition" and applying the new version on success.

These enhancements are not required by the assignment, but I wanted to simulate behavior that’s closer to a real-world OTA system.

### Challenges:

- Implementing timeout simulation without using real delay. It required adding custom parameters and designing testable logic that could mimic this behavior correctly without breaking the method flow.
- Making sure each failure point triggered at the right stage. For example, ensuring that a power failure during the "Upgrading" stage would not be confused with failures in the "Downloading" stage.
- Creating meaningful tests for negative scenarios while avoiding redundancy. It took a few tries to structure the tests so they cover the requirements without repeating too much logic.
- I tried to keep everything clear and beginner-friendly.

Overall, this project helped me improve my Python testing skills and understand how to simulate behavior logically.

---
