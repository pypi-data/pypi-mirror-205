from dataclasses import dataclass
from enum import Enum
from time import sleep
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
import traceback
from zpy.app import zapp_context as ctx
class Emoji(Enum):
    GREEN_CIRCLE = "\U0001f7e2"
    BUILDING_CONSTRUCTION = "\U0001f3d7"
    ABACOUS = "\U0001f9ee"
    HIGH_VOLTAGE = "\U000026a1"
    PARTY_POPPER = "\U0001f389"
    CROSS_MARK = "\U0000274c"
    CHECK_MARK = "\U00002705"

    def __str__(self) -> str:
        return self.value


T = TypeVar("T")


@dataclass
class OutputStep:
    data: dict
    can_continue: bool = True
    is_ok: bool = True
    message: str = ""


class Step(ABC, Generic[T]):
    def __init__(self, name: str, init_data: dict = {}):
        self.name = name
        self.init_data = init_data
        self.global_data = {}
        self.verbose = False

    @abstractmethod
    def run(self, input_data: T=None, shared_data: dict = {}) -> OutputStep:
        return OutputStep(input_data)


class Stepexecutor:
    def __init__(
        self, scenario: str, steps: list[Step], global_data: dict = {}, verbose: bool = False
    ) -> dict:
        self.scenario = scenario
        self.steps = steps
        self.global_data = global_data
        self.verbose = verbose

    def execute(self, shared_data: dict = {}) -> dict:
        print(f"\n\t{Emoji.GREEN_CIRCLE} Scenario: {self.scenario}")
        print(f"\t\t{Emoji.ABACOUS} Summary:")
        print(f"\t\t   {Emoji.HIGH_VOLTAGE} Steps: {len(self.steps)}\n")
        transaction_data = {}
        for i, step in enumerate(self.steps):
            # print(f"\t\t \U000025b6 {step.name}")
            # sleep(0.7)
            step.global_data = self.global_data
            step.verbose = self.verbose
            try:
                result = step.run(transaction_data, shared_data)
            except Exception as e:
                ctx().logger.exception(e)
                result = OutputStep({}, is_ok=False, message=str(e))

            if result and result.is_ok:
                print(f"\t\t {Emoji.CHECK_MARK} S{i+1}: {step.name}\n")
                sleep(0.2)
            if result and not result.is_ok:
                print(f"\t\t {Emoji.CROSS_MARK} S{i+1}: {step.name}\n")
                sleep(0.2)
            transaction_data = result
            self.global_data = step.global_data
        sleep(0.5)
        print(f"\n\t{Emoji.PARTY_POPPER} Finished scenario...\n")
        return transaction_data
