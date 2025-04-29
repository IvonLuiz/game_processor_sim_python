from core.processor import Processor
from core.memory import Memory


def run_test(test_name, program, expected_registers=None, expected_memory=None):
    print(f"Running test: {test_name}")

    # Setup processor
    mem = Memory()
    mem.load_program(program)
    proc = Processor(mem)

    # Run program
    proc.run()

    # Check results
    success = True

    # Check registers if specified
    if expected_registers:
        for reg_num, expected_value in expected_registers.items():
            actual_value = proc.registers[reg_num]
            if actual_value != expected_value:
                print(f"  FAIL: R{reg_num} = {actual_value}, expected {expected_value}")
                success = False
            else:
                print(f"  PASS: R{reg_num} = {expected_value}")

    # Check memory if specified
    if expected_memory:
        for address, expected_value in expected_memory.items():
            actual_value = mem.load(address)
            if actual_value != expected_value:
                print(
                    f"  FAIL: MEM[{address}] = {actual_value}, expected {expected_value}"
                )
                success = False
            else:
                print(f"  PASS: MEM[{address}] = {expected_value}")

    print(f"Test {test_name}: {'PASSED' if success else 'FAILED'}")
    return success


# Example test cases
test_cases = [
    {
        "name": "Addition Test",
        "program": [
            "MOV R1 R0",  # Set R1 to 0
            "ADD R1 R2",  # R1 += R2
            "ADD R1 R3",  # R1 += R3
        ],
        "setup": lambda proc: setattr(proc, "registers", [0, 0, 5, 10] + [0] * 28),
        "expected_registers": {1: 15},
    },
    {
        "name": "Memory Store/Load Test",
        "program": [
            "MOV R1 R0",  # Set R1 to 0
            "SW R2 100(R0)",  # Store R2 to address 100
            "LW R1 100(R0)",  # Load from address 100 to R1
        ],
        "setup": lambda proc: setattr(proc, "registers", [0, 0, 42] + [0] * 29),
        "expected_registers": {1: 42},
        "expected_memory": {100: 42},
    },
]


# Run all tests
def run_all_tests():
    passed = 0
    failed = 0

    for test in test_cases:
        mem = Memory()
        mem.load_program(test["program"])
        proc = Processor(mem)

        # Setup initial state
        if "setup" in test:
            test["setup"](proc)

        # Run program
        proc.run()

        # Check results
        success = True
        expected_registers = test.get("expected_registers", {})
        for reg_num, expected_value in expected_registers.items():
            if proc.registers[reg_num] != expected_value:
                success = False
                break

        expected_memory = test.get("expected_memory", {})
        for addr, expected_value in expected_memory.items():
            if mem.load(addr) != expected_value:
                success = False
                break

        print(f"Test '{test['name']}': {'PASSED' if success else 'FAILED'}")
        if success:
            passed += 1
        else:
            failed += 1

    print(f"Summary: {passed} tests passed, {failed} tests failed")


if __name__ == "__main__":
    run_all_tests()
