from src.instruction_processing import MachineGenerator

with open("./examples/example.txt", "r") as machine:
    text = machine.read()
    generator = MachineGenerator(text)
    tm = generator.process_turing_machine()
    tm.start()
