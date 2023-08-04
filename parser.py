from __future__ import annotations

import json
from dataclasses import dataclass
import datetime

import jinja2


TRANSFORM_POINTS = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 9,
    9: 10,
    10: 12,
    11: 14,
    12: 16,
    13: 18,
    14: 20,
    15: 22,
    16: 23,
    17: 25,
    18: 27,
    19: 28,
    20: 29,
    21: 31,
    22: 32,
    23: 34,
    24: 35,
    25: 36,
    26: 37,
    27: 38,
    28: 39,
    29: 41,
    30: 42,
    31: 43,
    32: 44,
    33: 45,
    34: 46,
    35: 47,
    36: 48,
    37: 49,
    38: 50,
    39: 51,
    40: 52,
    41: 53,
    42: 54,
    43: 55,
    44: 56,
    45: 57,
    46: 58,
    47: 59,
    48: 60,
    49: 61,
    50: 62,
    51: 63,
    52: 64,
    53: 65,
    54: 66,
    55: 67,
    56: 68,
    57: 69,
    58: 70,
    59: 71,
    60: 72,
    61: 73,
    62: 74,
    63: 75,
    64: 76,
    65: 77,
    66: 78,
    67: 79,
    68: 80,
    69: 81,
    70: 82,
    71: 83,
    72: 84,
    73: 85,
    74: 87,
    75: 89,
    76: 90,
    77: 92,
    78: 96,
    79: 98,
    80: 100
}

THEMES = ["Орфография", "Пунктуация", "Лексика", "Культура речи", "Фонетика", "Состав слова. Образование слов",
          "Морфология", "Синтаксис", "Текст, стили речи"]


@dataclass
class AllThemes:
    allThemes: list[str]


@dataclass
class Inner:
    test: str  # test name
    test_date: str
    username: str
    themes: str


@dataclass
class Answer:
    text: list[int] | str
    time: str


@dataclass
class Question:
    questionId: str  # A1, B12
    task: str
    type: str
    variants: list[str] | None
    text: str | None
    answers: list[int] | str
    time: str
    themes: list[str]
    commentary: list[str]
    answer: Answer


@dataclass
class Test:
    testId: int
    subjectId: int
    fulltime: int
    stage: str
    questions: list[Question]

    AllThemes: AllThemes


class JSONtoHTML:
    def __init__(self, json_filename, rules_filename):
        with open(json_filename, 'r', encoding="utf-8") as json_file:
            json_data = json.load(json_file)
        self.inner = Inner(**json_data.get("inner"))
        self.test = Test(**json_data.get("test"))
        self.general_time = 0  # in secs
        self.user_score = 0
        self.rules = {}
        self.incorrect_answers_for_theme = {}
        self.num_of_incorrect_answers = 0
        self.general_score = 0
        self.general_time = 0
        self.time_recommendation = ""
        self.strings = ["" for i in range(9)]

        with open(rules_filename, 'r', encoding="utf8") as rules_data_file:
            rules_data_file = rules_data_file.read()

        rules_data_file = rules_data_file.replace('\xad', '')
        rules_data_file = rules_data_file.replace('\t', '')
        splitted_rules = rules_data_file.split('\n')
        splitted_rules = [item for item in splitted_rules if item.strip()]

        for i in splitted_rules:
            key, value = i.split(" ", 1)
            self.rules[key] = value
        self.user_commentaries = {}
        self.num_of_correct_answers = 0
        self.num_of_half_correct_answers = 0
        self.num_of_incorrect_answers = 0
        self.problem_themes = {}
        self.rules_list = {}
        self.recommendations_index = {
            "general_score": self.general_score,
            "time_recommendation": self.time_recommendation,
            "rules": []
        }
        
    def render_html(self):
        self.make_recommendations()
        self.make_html_file()
        html = open('1111111111.html', encoding='utf8').read()
        template_ = jinja2.Template(html)
        self.test.questions
        rendered_html = (template_.render(
            inner=self.inner,
            test=self.test,
            answer_results=self.answer_results,
            time_recommendation=self.time_recommendation,
            problem_themes=self.problem_themes,
            general_test_points=self.general_test_points,
            first_points=self.general_score,
            test_points=self.test_points,
            time_of_solving=str(datetime.timedelta(seconds=self.general_time))[-8:],
            num_of_correct_answers=self.num_of_correct_answers,
            num_of_incorrect_answers=self.num_of_incorrect_answers
        ))
        print(rendered_html)
        with open('jinja2.html', 'w', encoding='utf8') as f:
            f.write(rendered_html)

    def make_user_score(self) -> list:

        self.user_index = {}
        self.answer_results = []
        user_commentaries = {}
        for i in self.rules.keys():
            self.user_index[i] = 0
        ind = -1
        for question in self.test.questions:
            ind += 1
            # получение инфы по тесту
            question_info = question['question']
            answers = question_info['answers']
            themes = question_info['themes']
            time = int(question_info['time'])
            user_answer = question['answer']['text']
            user_time = question['answer']['time']
            commentary = question_info['commentary']
            self.general_time += user_time

            if question_info["type"] == 'string':  # если тип вопроса - выбрать правильные варианты ответа

                check_if_incorrect = 0
                check_if_correct = 0
                if answers == user_answer:
                    check_if_correct = len(answers)
                else:
                    for i in range(len(answers)):
                        if i < len(user_answer):

                            if answers[i] != user_answer[i]:
                                check_if_incorrect += 1

                                if type(themes[answers[i] - 1]) == list:
                                    for theme in themes[answers[i] - 1]:
                                        self.user_index[theme + '.'] += 1
                                        user_commentaries[theme + '.'] = commentary[answers[i] - 1]
                                else:
                                    self.user_index[themes[answers[i] - 1] + '.'] += 1
                                    user_commentaries[themes[answers[i] - 1] + '.'] = commentary[answers[i] - 1]
                        else:
                            self.user_index[themes[answers[i] - 1] + '.'] += 1  # если разная длина у правильного
                            # ответа и
                            # ответа пользователя

                check_if_not_equal = 0
                if len(user_answer) != len(answers):
                    check_if_not_equal += abs(len(answers) - len(user_answer))

                if check_if_correct == len(answers):
                    self.answer_results.append("Верно")
                    self.general_score += 2
                    self.num_of_correct_answers += 1

                elif check_if_incorrect == 0 and check_if_not_equal == 1:
                    self.general_score += 1
                    self.num_of_half_correct_answers = 0
                    self.answer_results.append("Частично верно")

                else:
                    self.answer_results.append("Неверно")
                    self.num_of_incorrect_answers += 1

            if question_info["type"] == 'word':  # если тип вопроса - найти подходящее слово
                if answers != user_answer:
                    self.num_of_incorrect_answers += 1
                    self.answer_results.append("Неверно")
                    for theme in themes:
                        if type(theme) == list:
                            for subtheme in theme:
                                self.user_index[subtheme + '.'] += 1
                        else:
                            self.user_index[theme + '.'] += 1

                else:
                    self.general_score += 2
                    self.num_of_correct_answers += 1
                    self.answer_results.append("Верно")

            if question_info["type"] == 'list_word':  # если тип вопроса - выписать правильные ответы в
                # произвольном порядке
                check_if_correct = 0
                check_if_incorrect = 0
                right_answer = answers[0]
                for char_in_user_answer in user_answer:
                    check_char = 0
                    for char_in_right_answer in right_answer:
                        if char_in_user_answer == char_in_right_answer:
                            check_char += 1
                    if check_char == 0:
                        check_if_incorrect += 1
                        if type(themes[int(char_in_user_answer) - 1]) == list:
                            for subtheme in themes[int(char_in_user_answer) - 1]:
                                self.user_index[subtheme + '.'] += 1
                        else:
                            self.user_index[themes[int(char_in_user_answer) - 1] + '.'] += 1
                    else:
                        check_if_correct += check_char

                check_if_not_equal = 0
                if len(user_answer) != len(right_answer):
                    check_if_not_equal = abs(len(user_answer) - len(right_answer))

                if check_if_correct == len(right_answer):
                    self.answer_results.append("Верно")
                    self.general_score += 2
                    self.num_of_correct_answers += 1

                elif check_if_not_equal == 1 and check_if_incorrect == 0:
                    self.general_score += 1
                    self.num_of_half_correct_answers += 1
                    self.answer_results.append("Частично верно")
                else:
                    self.answer_results.append("Неверно")
                    self.num_of_incorrect_answers += 1

            if question_info["type"] == 'АБВГ_string':  # если тип вопроса - соотнести варианты из 2 колонок

                check_if_incorrect = 0
                check_if_correct = 0

                for i in range(len(user_answer)):
                    if i % 2 != 0:

                        if user_answer[i] != answers[i]:
                            check_if_incorrect += 1
                            if type(themes[(i // 2)]) == list:
                                for couple_of_themes in themes[i // 2]:
                                    if couple_of_themes is list:
                                        for subtheme in couple_of_themes:
                                            self.user_index[subtheme + '.'] += 1
                            else:
                                self.user_index[themes[(i // 2)] + '.'] += 1
                        else:
                            check_if_correct += 1

                if check_if_incorrect == 0:
                    self.answer_results.append("Верно")
                    self.general_score += 2
                    self.num_of_correct_answers += 1

                elif check_if_incorrect == 0 and check_if_correct < 4:
                    self.general_score += 1
                    self.answer_results.append("Частично верно")

                elif check_if_incorrect == 1:
                    self.answer_results.append("Частично верно")
                    self.general_score += 1
                    self.num_of_half_correct_answers += 1

                else:
                    self.answer_results.append("Неверно")
                    self.num_of_incorrect_answers += 1

            if time < user_time <= 1.4 * time:

                for i in themes:
                    self.user_index[i + '.'] += 0.2

            if 1.4 * time < user_time <= 1.8 * time:

                for i in themes:
                    self.user_index[i + '.'] += 0.4

            if 1.8 * time < user_time <= 2.3 * time:

                for i in themes:
                    self.user_index[i + '.'] += 0.6

            question['answer']['time'] = str(datetime.timedelta(seconds=question['answer']['time']))[-8:]

        self.test_points = TRANSFORM_POINTS[self.general_score]
        self.general_test_points = list(TRANSFORM_POINTS.keys())[-1]

        if self.general_time < 1200:
            self.time_recommendation = "Вы справились довольно быстро!"

        if 1200 <= self.general_time < 1600:
            self.time_recommendation = "У вас почти закончилось время! Нужно стараться выполнять тест быстрее"

        if self.general_time > 1600:
            self.time_recommendation = "У вас закочилось время! Нужно стараться выполнять тест быстрее"

        sorted_by_index = dict(sorted(self.user_index.items(), key=lambda item: item[1], reverse=True))
        sorted_by_theme = {k: v for k, v in self.user_index.items() if v != 0}
        return [sorted_by_index, sorted_by_theme]

    def make_recommendations(self) -> list:
        sorted_index_dict, sorted_theme_dict = self.make_user_score()
        top_related_index = list(sorted_index_dict.keys())
        top_related_theme = list(sorted_theme_dict.keys())
        for rec in top_related_index:
            self.recommendations_index["rules"].append(
                f"Rule : {self.rules[rec]}" + f" number : {rec} " + f"index : {sorted_index_dict[rec]}")
        for rec in top_related_theme:
            self.rules_list[rec] = self.rules[rec]
        return [self.recommendations_index, self.rules_list]

    def complete_rules_list(self):
        complete_rules = []
        for key, value in self.rules_list.items():
            key_list = key.split(".")[:-1]
            temp_list = []
            new_key = key_list[0] + '.' + key_list[1] + '.'
            if self.strings[int(key_list[0]) - 1] == "":
                self.strings[int(key_list[0]) - 1] = THEMES[int(key_list[0]) - 1]
            if self.rules[new_key] not in self.rules_list:
                temp_list.insert(0, self.rules[new_key])
            if len(key_list) > 2:
                for i in range(2, len(key_list)):
                    new_key += key_list[i] + '.'
                    temp_list.append(self.rules[new_key])
            complete_rules.append(temp_list)
        return complete_rules

    def make_html_file(self):
        complete_rules = self.complete_rules_list()
        for i in range(len(complete_rules)):
            string_to_insert = []
            for j in range(len(complete_rules[i])):
                if complete_rules[i][j] not in self.rules_list.values():
                    if j == 0:
                        string_to_insert.append(complete_rules[i][j])
                    else:
                        string_to_insert.append(complete_rules[i][j])
                else:
                    string_to_insert.append(complete_rules[i][j])
                    ierarchy = 0
                    for k in self.rules_list.keys():
                        if self.rules_list[k] == complete_rules[i][j]:
                            ierarchy = k[0]
                    self.problem_themes.setdefault(self.strings[int(ierarchy) - 1], []).extend(string_to_insert)
        for key in self.problem_themes.keys():
            self.problem_themes[key] = list(set(self.problem_themes[key]))


file = JSONtoHTML('old.json', 'rules.txt')
file.render_html()