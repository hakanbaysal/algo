# This is the second question of the algorithm assignment
class AlgoQ2:

    def __init__(self, input1: list, input2: list):
        self.input1 = input1
        self.input2 = input2
        self.merged_list = self.merge_lists(input1, input2)
        self.output = self.calculate_median(self.merged_list)

    # This method merges two lists into one
    @staticmethod
    def merge_lists(input1: list, input2: list) -> list:
        return sorted(input1 + input2)

    # This method calculates the median of a list
    @staticmethod
    def calculate_median(merged_list: list) -> float:
        list_length = len(merged_list)
        find_middle_index = int(list_length / 2)
        if len(merged_list) % 2 == 0:
            return (merged_list[find_middle_index] + merged_list[find_middle_index - 1]) / 2
        else:
            return merged_list[find_middle_index]


# This is the main method
if __name__ == '__main__':
    # This is the first list
    input1 = [float(x) for x in input("input1: ").split()]
    # This is the second list
    input2 = [float(x) for x in input("input2: ").split()]
    # This is the object of the class AlgoQ2
    algo = AlgoQ2(input1, input2)
    # This is the output
    print("output:", algo.output)
