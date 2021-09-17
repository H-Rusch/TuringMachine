from src.exceptions import ArgumentToSmallException


class TuringMachine:
    def __init__(self, states: list, initial_state: str, accepting_states: list, transitions: dict, initial_input: list,
                 tapes: int = 1):
        if tapes <= 0:
            raise ArgumentToSmallException("You have to have at least 1 tape in your machine")

        self.tapes = [Tape() for _ in range(tapes)]
        self.tapes[0] = Tape(initial_input)
        self.initial_input = "".join(initial_input)
        self.states = states
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.transitions = transitions

    def start(self):
        """The main calculation of the Turing Machine. The fitting transition is used, until the machine stops.
        Print current state of the machine in each iteration.
        """
        steps = 0
        state = self.initial_state
        while True:
            print()
            print("State:\t" + state)
            for i in range(len(self.tapes)):
                print(f"Tape {i + 1}:\t" + str(self.tapes[i]))
            print("Steps:\t" + str(steps))

            # current values on the tape
            values = tuple(t.current.value for t in self.tapes)

            # if a transition is possible, execute it by changing the state, chaning the value of the tapes
            # and doing the movement on the tape
            if state in self.transitions.keys() and values in self.transitions[state].keys():
                transition = self.transitions[state][values]

                state = transition[0]
                for i in range(len(self.tapes)):
                    # change the value of tape #i
                    self.tapes[i].current.value = transition[1 + i]

                    # movement for tape # i
                    if transition[len(self.tapes) + 1 + i] == "r":
                        self.tapes[i].go_right()
                    elif transition[len(self.tapes) + 1 + i] == "l":
                        self.tapes[i].go_left()
                steps += 1

            else:
                break

        if state in self.accepting_states:
            print("Accepting the input: " + self.initial_input)
        else:
            print("Rejecting the input: " + self.initial_input)


class Tape:
    """"Using a double-linked-list as the tape."""

    def __init__(self, init: list = None):
        """Initialize the Tape. If no input was given, a blank is active, but if an input was given, the first element
        of the input is active."""
        self.start = Field("_")
        self.current = self.start

        if init is not None and len(init) > 0:
            # generate fields with the values given. Link adjacent fields with each other.
            for value in init:
                generating = Field(value)
                self.current.next = generating
                generating.previous = self.current
                self.current = generating

            # remove leading blank
            self.start = self.start.next
            self.start.previous = None
            self.current = self.start

    def go_right(self):
        """Go to the Field following the current Field.
        If the right edge of the Tape is reached, a blank will be generated.
        If going right on blanks at the left edge, those blanks will be removed.
        """
        # only one blank
        if self.current.value == "_" and self.current.next is None and self.current.previous is None:
            pass

        # left edge
        elif self.current.previous is None and self.current.value == "_":
            self.current = self.current.next
            self.start = self.current
            self.current.previous = None

        # right edge
        elif self.current.next is None:
            generated = Field("_")
            generated.previous = self.current
            self.current.next = generated
            self.current = self.current.next

        else:
            self.current = self.current.next

    def go_left(self):
        """Go to the Field preceding the current Field.
        If going left on blanks at the left edge, those blanks will be removed.
        if the left edge of the Tape is reached, a blank will be generated.
        """
        # only one blank
        if self.current.value == "_" and self.current.next is None and self.current.previous is None:
            pass

        # right edge
        elif self.current.next is None and self.current.value == "_":
            self.current = self.current.previous
            self.current.next = None

        # left edge
        elif self.current.previous is None:
            generated = Field("_")
            generated.next = self.current
            self.current.previous = generated
            self.start = generated
            self.current = self.current.previous

        else:
            self.current = self.current.previous

    def __str__(self):
        """String representation of the Tape. All of the values are combined and the active value is highlighted.
        """
        current = self.start
        values = []
        while True:
            if current == self.current:
                values.append("." + current.value + ".")
            else:
                values.append(" " + current.value + " ")
            current = current.next
            if current is None:
                break
        return " ".join(values)


class Field:
    """A Field on the tape. Every Field has a value and a blank has the value '_'.
    """

    def __init__(self, value: str):
        self.value = value
        self.previous = None
        self.next = None
