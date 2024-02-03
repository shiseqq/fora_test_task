import json
import pandas as pd
from datetime import datetime
from prettytable import PrettyTable


class Table:
    def __init__(self, bib_number, name, surname, result):
        self.place = -1
        self.bib_number = bib_number
        self.name = surname           # In the test example, names and surnames were mixed up
        self.surname = name
        self.result = result

    def __str__(self):
        return (f'{self.place}, {self.bib_number}, {self.name}, {self.surname}, '
                f'{str(self.result)[2:].replace('.', ',')}')

    def get_list(self):
        return [self.place, self.bib_number, self.name, self.surname, str(self.result)[2:].replace('.', ',')]

    def get_place(self):
        return self.place

    def get_info(self):
        return {"Нагрудный номер": str(self.bib_number),
                "Имя": self.name,
                "Фамилия": self.surname,
                "Результат": str(self.result)[2:].replace('.', ',')}


def PrintTable(table_data):
    table = PrettyTable()
    table.field_names = ["Занятое место", "Нагрудный номер", "Имя", "Фамилия", "Результат"]
    table.align = 'l'
    for i in table_data:
        table.add_row(i.get_list())
    print(table)


def main():
    with (open('competitors2.json', encoding='utf-8-sig') as json_file):
        competitors_dict = json.load(json_file)

    dataFrame = pd.read_csv('results_RUN.txt', header=None, delimiter=' ')

    results_table = []
    for i in range(0, len(dataFrame), 2):
        m_time = datetime.strptime(dataFrame.values[i][2], "%H:%M:%S,%f")
        m_time1 = datetime.strptime(dataFrame.values[i + 1][2], "%H:%M:%S,%f")
        key = str(dataFrame.values[i][0])
        results_table.append(Table(key, competitors_dict[key]['Name'], competitors_dict[key]['Surname'],
                                   m_time1 - m_time))

    results_table = sorted(results_table, key=lambda x: x.result)

    for i in range(len(results_table)):
        results_table[i].place = i + 1

    final_results = {}
    for i in results_table:
        final_results[i.get_place()] = i.get_info()

    json_object = json.dumps(final_results, indent=4, sort_keys=False,ensure_ascii=False)
    with open('final_results.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)

    PrintTable(results_table)


if __name__ == "__main__":
    main()
