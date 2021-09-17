from src.exceptions import AlreadyDefinedException, TransitionError, MachineNotFullyDefined
from src.turing_machine import TuringMachine


class MachineGenerator:
    def __init__(self, text):
        self.tapes = None
        self.machine_input = None
        self.state_list = []
        self.initial_state = None
        self.accepting_states = None
        self.transitions = dict()

        self.text = text

    def process_turing_machine(self):
        lines = self.text.splitlines()

        transition_condition = None
        i = 0
        while i < len(lines):
            line = lines[i].replace(" ", "")
            # ignore comments and empty lines
            if not (line.startswith("#") or len(line) == 0):
                # input
                if line.startswith("input:"):
                    if self.machine_input is None:
                        self.machine_input = line[line.find(":") + 1:]
                    else:
                        raise AlreadyDefinedException("The input was defined before. Error in line " + str(i + 1))

                # state list
                elif line.startswith("states:"):
                    if not self.state_list:
                        self.state_list = line[line.find(":") + 1:].split(",")
                    else:
                        raise AlreadyDefinedException("The state list was defined before. Error in line " + str(i + 1))

                # initial state
                elif line.startswith("initial:"):
                    if self.initial_state is None:
                        self.initial_state = line[line.find(":") + 1:]
                    else:
                        raise AlreadyDefinedException(
                            "The initial state was defined before. Error in line " + str(i + 1))

                # final states
                elif line.startswith("accept:"):
                    if self.accepting_states is None:
                        self.accepting_states = line[line.find(":") + 1:].split(",")
                    else:
                        raise AlreadyDefinedException(
                            "The accepting states were defined before. Error in line " + str(i + 1))

                # transitions
                else:
                    if transition_condition is None:
                        transition_condition = line.split(",")
                    else:
                        transition_result = line.split(",")

                        if self.validate_transition(transition_condition, transition_result):
                            self.create_transition(transition_condition, transition_result)
                            transition_condition = None
                        else:
                            raise TransitionError("Error with transition in line " + str(i + 1) + "\n"
                                                  + "Check if it has the correct amount of tapes and that the "
                                                  + "symbols are single characters")

            i += 1

        self.check_values()

        return TuringMachine(self.state_list, self.initial_state, self.accepting_states, self.transitions,
                             list(self.machine_input), self.tapes)

    def check_values(self):
        """Check the given values in the machine description. If the state list is not given, or there is no initial
        state given, this will raise an Exception.
        If there is no number of tapes or no accepting states given, the fitting value is set to a default value.
        """
        if self.tapes is None:
            self.tapes = 1
        if len(self.state_list) == 1:
            raise MachineNotFullyDefined("The state-list has to be defined.")
        if self.initial_state is None or self.initial_state == "":
            raise MachineNotFullyDefined("The initial state has to be given.")
        if self.accepting_states is None:
            self.accepting_states = []

    def validate_transition(self, condition, result):
        # set the number of tapes from the first transition encountered
        if self.tapes is None:
            self.tapes = len(condition) - 1

        # check condition
        if not (len(condition) - 1 == self.tapes and condition[0] in self.state_list and all(
                len(element) == 1 for element in condition[1:])):
            return False

        # check result
        if not (len(result) - 1 == 2 * self.tapes and result[0] in self.state_list and
                all(len(element) == 1 for element in result[1:]) and
                all(direction in ["l", "s", "r"] for direction in result[self.tapes + 1:])):
            return False

        return True

    def create_transition(self, condition, result):
        state = condition[0]
        tapes = tuple(tape for tape in condition[1:])

        if state not in self.transitions.keys():
            self.transitions[state] = dict()
        if tapes not in self.transitions.keys():
            self.transitions[state][tapes] = result
        else:
            raise AlreadyDefinedException("This transition has already been defined: " + condition + "->" + result)
