import argparse
import json
import re
from tqdm import tqdm


def createParser():
    """Create parser"""

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='32.txt')
    parser.add_argument('--output', default='output.txt')
    return parser


class Validator:
    """Validator class to get count_valid_records / count_invalid_records / count_invalid_arguments"""
    value: list

    def __init__(self, array) -> None:
        """Constructor: gets copy them to local list"""
        self.value = array.copy()

    def validation(self, index) -> dict:
        """Function: Get valid / invalid writes"""

        result = {"telephone": self.check_telephone(index),
                  "height": self.check_height(index),
                  "inn": self.check_inn(index),
                  "passport_number": self.check_passport_number(index),
                  "occupation": self.check_occupation(index),
                  "age": self.check_age(index),
                  "academic_degree": self.check_academic_degree(index),
                  "worldview": self.check_worldview(index),
                  "adress": self.check_address(index)}
        return result.copy()

    def count_valid_records(self) -> int:
        """Function: Get count valid writes"""

        count_correct = 0
        for i in tqdm(range(len(self.value)),
                      desc="Подсчёт корректных записей"):
            if not (False in self.validation(i).values()):
                count_correct += 1
        return count_correct

    def count_invalid_records(self) -> int:
        """Function: Get count invalid writes"""

        count_incorrect = 0
        for i in tqdm(range(len(self.value)),
                      desc="Подсчёт некорректных записей"):
            if False in self.validation(i).values():
                count_incorrect += 1
        return count_incorrect

    def count_invalid_arguments(self) -> list:
        """Function: Get valid writes"""

        count_inv = [0] * 9
        for i in tqdm(range(len(self.value)),
                      desc="Подсчёт некорректных записей  данных"):
            if not self.check_telephone(i):
                count_inv[0] += 1
            if not self.check_height(i):
                count_inv[1] += 1
            if not self.check_inn(i):
                count_inv[2] += 1
            if not self.check_passport_number(i):
                count_inv[3] += 1
            if not self.check_occupation(i):
                count_inv[4] += 1
            if not self.check_age(i):
                count_inv[5] += 1
            if not self.check_academic_degree(i):
                count_inv[6] += 1
            if not self.check_worldview(i):
                count_inv[7] += 1
            if not self.check_address(i):
                count_inv[8] += 1
        return count_inv

    def check_telephone(self, num) -> bool:
        """Function: check telephone"""

        pattern = "\\+(7)\\-\\(\\d{3}\\)\\-\\d{3}\\-\\d{2}\\-\\d{2}$"
        if re.match(pattern, self.value[num]["telephone"]):
            return True
        return False

    def check_height(self, num) -> bool:
        """Function: check height"""
        try:
            float_height = float(self.value[num]["height"])
            return 2.2 > float_height > 1.2
        except ValueError:
            return False

    def check_inn(self, num) -> bool:
        """Function: check IIN"""

        pattern = "^\\d{12}$"
        if re.match(pattern, self.value[num]["inn"]):
            return True
        return False

    def check_passport_number(self, num) -> bool:
        """Function: check passport number"""

        if isinstance(self.value[num]["passport_number"], int):
            if 100000 <= self.value[num]["passport_number"] < 1000000:
                return True
        return False

    def check_occupation(self, num) -> bool:
        """Function: check occupation"""

        pattern = "^([а-яА-Я]|[a-zA-Z]|-| ){3,}$"
        if re.match(pattern, self.value[num]["occupation"]):
            return True
        return False

    def check_age(self, num) -> bool:
        """Function: check age"""

        if isinstance(self.value[num]["age"], int):
            if 0 <= self.value[num]["age"] < 120:
                return True
        return False

    def check_academic_degree(self, num) -> bool:
        """Function: check academic degree"""

        pattern = "[a-zA-Zа-яА-Я]+"
        if re.match(pattern, self.value[num]["academic_degree"]):
            return True
        return False

    def check_worldview(self, num) -> bool:
        """Function: check worldview"""

        pattern = "[a-zA-Zа-яА-Я]+"
        if re.match(pattern, self.value[num]["worldview"]):
            return True
        return False

    def check_address(self, num) -> bool:
        """Function: check address"""

        pattern = ".+[0-9]+"
        if re.match(pattern, self.value[num]["address"]):
            return True
        return False


class fileReader:
    """Reads file data by path name"""

    def __init__(self, file_path) -> None:
        """Contstructor: writes path"""
        self.path = file_path

    def read_file(self) -> list:
        """Function: writes data to class self"""

        array: list = []
        data = json.load(open(self.path, encoding="windows-1251"))
        for i in data:
            array.append(dict(i.copy()))
        return array


class fileWriter:
    """Write file data by path name"""

    def __init__(self, file_path) -> None:
        """Contstructor: writes path"""

        self.path = file_path

    def write_file(self, array) -> None:
        """Function: reads data from file"""

        tmp = []
        for i in tqdm(range(len(array.value)),
                      desc="Запись результата валидации в файл"):
            if not (False in array.validation(i).values()):
                tmp.append(array.value[i].copy())
        json.dump(
            tmp,
            open(self.path, "w", encoding="windows-1251"))


parser = createParser()
namespace = parser.parse_args()

array = Validator(fileReader(namespace.input).read_file())
valid = array.count_valid_records()
invalid = array.count_invalid_records()
result = array.count_invalid_arguments()
fileWriter(namespace.output).write_file(array)

print("Count valid records " + str(valid))
print("Count invalid records " + str(invalid))
print(result)
