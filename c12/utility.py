import psutil

from c12.constant import Color, ExecutionMode


def print_colored_text(text: str, color: Color = Color.WHITE, start='', end='\n'):
    print(start + '\033[' + color.value + 'm' + text + '\033[0m', end=end)


class ComputerStructure:

    def __init__(self):
        self.cpu_core_count = psutil.cpu_count()
        self.total_memory_amount = psutil.virtual_memory().total * 1e-9
        self.available_memory_amount = psutil.virtual_memory().available * 1e-9

    def decide_mode(self) -> ExecutionMode:
        cpu_core_count = self.cpu_core_count
        total_memory_amount = self.total_memory_amount
        available_memory_amount = self.available_memory_amount
        available_very_high = cpu_core_count >= 8 and total_memory_amount >= 16 and available_memory_amount >= 8
        available_high = cpu_core_count >= 6 and total_memory_amount >= 16 and available_memory_amount >= 8
        available_middle = cpu_core_count >= 4 and total_memory_amount >= 12 and available_memory_amount >= 6
        available_low = cpu_core_count >= 4 and total_memory_amount >= 8 and available_memory_amount >= 4
        if available_very_high:
            return ExecutionMode.VERY_HIGH
        elif available_high:
            return ExecutionMode.HIGH
        elif available_middle:
            return ExecutionMode.MIDDLE
        elif available_low:
            return ExecutionMode.LOW
        else:
            return ExecutionMode.NO_RECOMMENDED


class TrainSetting:

    def __init__(self, scan: bool):
        execution_mode = ExecutionMode.DEBUG
        if scan:
            computer_structure = ComputerStructure()
            execution_mode = computer_structure.decide_mode()
        if execution_mode == ExecutionMode.VERY_HIGH:
            self.extraction_count = 12000
            self.epochs = 30
        elif execution_mode == ExecutionMode.HIGH:
            self.extraction_count = 6000
            self.epochs = 60
        elif execution_mode == ExecutionMode.MIDDLE:
            self.extraction_count = 6000
            self.epochs = 30
        elif execution_mode == ExecutionMode.LOW:
            self.extraction_count = 3000
            self.epochs = 30
        elif execution_mode == ExecutionMode.NO_RECOMMENDED:
            self.extraction_count = 1500
            self.epochs = 30
        elif execution_mode == ExecutionMode.DEBUG:
            self.extraction_count = 20
            self.epochs = 1
        print('{}(data count: {}, epochs: {})'.format(execution_mode, self.extraction_count, self.epochs))


if __name__ == '__main__':
    print('Total Memory:\t', psutil.virtual_memory().total * 1e-9, 'GB')
    print('Available Memory:\t', psutil.virtual_memory().available * 1e-9, 'GB')
    print('Free Memory:\t', psutil.virtual_memory().free * 1e-9, 'GB')
    print('Used Memory:\t', psutil.virtual_memory().used * 1e-9, 'GB')
