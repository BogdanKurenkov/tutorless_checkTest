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

themes = ['Правописание проверяемых непроверяемых, чередующихся гласных А/О в корне слова',
             'Правописание проверяемых непроверяемых, чередующихся гласных Е/И в корне слова',
             'Правописание двойных согласных', 'Правописание гласных после шипящих', 'Различение НЕ/НИ',
             'Правописание НЕ со словами разных частей речи',
             'Дефисные, слитные и раздельные написания существительных, прилагательных наречий',
             'Слитные и раздельные написания наречий, предлогов, союзов', 'Тире между подлежащим и сказуемым',
             'Знаки препинания в предложениях с обособленными членами предложения', 'Вводные слова и словосочетания',
             'Знаки препинания в предложениях с однородными членами предложения, в сложносочинённых предложениях',
             'Знаки препинания в сложносочиненных предложениях, сложноподчинённых предложениях',
             'Знаки препинания в предложениях с обобщающими словами при однородных членах предложениях, в бессоюзных сложных предложениях',
             'Знаки препинания при прямой речи. Знаки препинания при диалоге. Знаки препинания при цитировании.',
             'Знаки препинания в предложениях, содержащих конструкции с КАК', 'Определение подтем текста',
             'Стилистическая характеристика и задача речи', 'Лексическое значение слова, синонимы',
             'Лексическое значение слова, антонимы', 'Правописание глагольных форм', 'Правописание удвоенных согласных',
             'Фонетика', 'Состав слова', 'Разряды имен прилагательных',
             'Морфология местоимений и наречий (союзные слова), служебных частей речи. Строение сложноподчиненного предложения',
             'Синтаксис. Словосочетание.', 'Правописание И/Ы после Ц, гласных И/Ы после приставок',
             'Правописание суффиксов и окончаний существительных и прилагательных', 'Правописание согласных',
             'Знаки препинания в предложении с разными видами связи', 'Прямое и переносное значение слова',
             'Морфологические признаки глагола и причастия, образование причастий', 'Типы односоставных предложений',
             'Морфологические нормы', 'Синтаксические нормы', 'Речевые нормы', 'Сочетаемость слов',
             'Словообразовательные модели', 'Морфологические признаки имени существительного', 'Типы предложений']

@dataclass
class AllThemes:
    allThemes: list[str]


@dataclass
class Inner:
    test: str  # test name
    test_date: str
    username: str
    themes: str


# @dataclass
# class Answer:
#     text: list[str] | str
#     time: str


@dataclass
class Question:
    # questionId: str
    task: str
    type: str
    variants: list[str] | None
    # text: str | None
    answers: list[int] | str
    time: int
    # themes: list[str]
    # commentary: list[str]
    # answer: Answer


@dataclass
class Test:
    testId: str
    subjectId: str
    fulltime: str
    stage: str
    questions: list[Question]

    AllThemes:  list[str]


class JSONtoHTML:
    def __init__(self, json_filename, rules_filename, answers_filename):
        with open(json_filename, 'r', encoding="utf-8") as json_file:
            json_data = json.load(json_file)
        # self.usefulldata={}
        # self.usefulldata['test'] = 'Test'
        # self.usefulldata['themes'] = 'AllThemes'
        # self.usefulldata['test_date'] = json_data['date']
        # self.usefulldata['username'] = json_data['userFullname']
        # print(self.usefulldata)
        self.inner = Inner(
            test=json_data['subject'],
            themes='AllThemes',
            test_date=json_data['date'],
            username=json_data['userFullname']
        )
        # self.inner = Inner(**json_data.get("inner"))
        # self.test = Test(**json_data.get("test"))
        # self.test={}
        # self.test['testId'] = '1'
        # self.test['subjectId'] = 'RU'
        # # peredelat fulltime
        # self.test['fulltime'] = '12424'
        # self.test['stage'] = 'number'
        # self.test['questions'] = json_data['questions']

        self.test = Test(
            testId="1",
            subjectId='RU',
            fulltime='12424',
            stage=json_data['name'],
            AllThemes=themes,
            questions=json_data.get("questions")
        )

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

        with open(answers_filename, "r", encoding="utf8") as answers_file:
            answers_data = json.load(answers_file)
        self.answersData = answers_data['data']
        for i in range(len(self.answersData)):
            self.test.questions[i]['themes'] = self.answersData[i]['themes']
            self.test.questions[i]['commentary'] = self.answersData[i]['commentary'].split('\n')
            self.test.questions[i]['rightAnswers'] = self.answersData[i]['rightAnswers']
            self.test.questions[i]['acceptableTime'] = self.answersData[i]['acceptableTime']
        print(self.test.questions[0]['commentary'])

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

        # print(self.inner)

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
        # print(rendered_html)
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
            # print(question)
            ind += 1
            # получение инфы по тесту
            question_info = question
            answers = self.answersData[ind]['rightAnswers']
            themes = self.answersData[ind]['themes']
            time = int(self.answersData[ind]['acceptableTime'])
            user_answer = question_info['answers']
            user_time = question_info['time']
            commentary = self.answersData[ind]['commentary']
            # print(answers,user_answer)
            self.general_time += user_time

            # print(ind)
            if question_info["type"] == 'variants':  # если тип вопроса - выбрать правильные варианты ответа
                check_if_incorrect = 0
                check_if_correct = 0
                if answers == user_answer:
                    check_if_correct = len(answers)
                else:
                    # print(ind, answers, user_answer)
                    for i in range(len(answers)):
                        if i < len(user_answer):
                            # print('zashel v if',ind,user_answer,answers)
                            if answers[i] != user_answer[i]:
                                # print(answers[i], user_answer[i], i)
                                check_if_incorrect += 1
                                # print(user_answer)
                                # print(themes)
                                # print(user_answer)
                                if type(themes[answers[i] - 1]) == list:
                                    # print('vlojenniy if',ind,user_answer,answers)
                                    # print(themes[answers[i] - 1])
                                    for theme in themes[answers[i] - 1]:
                                        self.user_index[theme + '.'] += 1
                                        user_commentaries[theme + '.'] = commentary[answers[i] - 1]
                                else:
                                    self.user_index[themes[answers[i] - 1] + '.'] += 1
                                    user_commentaries[themes[answers[i] - 1] + '.'] = commentary[answers[i] - 1]
                        else:
                            # print('zashel v else',ind,user_answer,answers)
                            self.user_index[themes[answers[i] - 1] + '.'] += 1  # если разная длина у правильного
                            # ответа и
                            # ответа пользователя

                # print(check_if_incorrect,check_if_incorrect,check_if_correct,ind,answers,user_answer)
                check_if_not_equal = 0
                if len(user_answer) != len(answers):

                    check_if_not_equal += abs(len(answers) - len(user_answer))
                    # print(check_if_incorrect,check_if_not_equal,answers,user_answer,ind)

                if check_if_correct == len(answers):
                    # print('if equal',ind,user_answer,answers,'verno')
                    self.answer_results.append("Верно")
                    self.general_score += 2
                    self.num_of_correct_answers += 1
                elif check_if_incorrect == 0 and check_if_not_equal == 1:
                    # print('chastichno verno',ind,user_answer,answers)
                    self.general_score += 1
                    self.num_of_half_correct_answers = 0
                    self.answer_results.append("Частично верно")

                else:
                    # print('ne verno',ind,user_answer,answers)
                    self.answer_results.append("Неверно")
                    self.num_of_incorrect_answers += 1

            if question_info["type"] == 'textarea':  # если тип вопроса - найти подходящее слово
                if answers != user_answer:
                    # print('ne verno',ind,user_answer,answers)
                    self.num_of_incorrect_answers += 1
                    self.answer_results.append("Неверно")
                    for theme in themes:
                        if type(theme) == list:
                            for subtheme in theme:
                                self.user_index[subtheme + '.'] += 1
                        else:
                            self.user_index[theme + '.'] += 1

                else:
                    # print('verno', ind, user_answer, answers)
                    self.general_score += 2
                    self.num_of_correct_answers += 1
                    self.answer_results.append("Верно")

            if question_info["type"] == 'variants_with_textarea':  # если тип вопроса - выписать правильные ответы в
                # произвольном порядке
                check_if_correct = 0
                check_if_incorrect = 0
                right_answer = answers[0]
                for char_in_user_answer in user_answer:
                    check_char = 0
                    # print(char_in_user_answer,ind)
                    for char_in_right_answer in right_answer:
                        if char_in_user_answer == char_in_right_answer:
                            check_char += 1
                    if check_char == 0:
                        check_if_incorrect += 1
                        # print(themes,ind)
                        # print(answers, user_answer,ind)
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
                    # print('verno',ind,answers,user_answer)
                    self.answer_results.append("Верно")
                    self.general_score += 2
                    self.num_of_correct_answers += 1

                elif check_if_not_equal == 1 and check_if_incorrect == 0:
                    # print('chastichno', ind, user_answer, answers)
                    self.general_score += 1
                    self.num_of_half_correct_answers += 1
                    self.answer_results.append("Частично верно")
                else:
                    # print('ne verno', ind, user_answer, answers)
                    self.answer_results.append("Неверно")
                    self.num_of_incorrect_answers += 1

            if question_info["type"] == 'ratio':  # если тип вопроса - соотнести варианты из 2 колонок
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
                    # print('verno',ind,user_answer,answers)
                    self.answer_results.append("Верно")
                    self.general_score += 2
                    self.num_of_correct_answers += 1

                elif check_if_incorrect == 0 and check_if_correct < 4:
                    # print('chastichno', ind, user_answer, answers)
                    self.general_score += 1
                    self.answer_results.append("Частично верно")

                elif check_if_incorrect == 1:
                    # print('chactichno', ind, user_answer, answers)
                    self.answer_results.append("Частично верно")
                    self.general_score += 1
                    self.num_of_half_correct_answers += 1

                else:
                    # print('ne verno', ind, user_answer, answers)
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

            question['time'] = str(datetime.timedelta(seconds=question['time']))[-8:]

        self.test_points = TRANSFORM_POINTS[self.general_score]
        # print(self.general_score)
        self.general_test_points = list(TRANSFORM_POINTS.keys())[-1]
        # print(self.general_test_points)

        # print(self.num_of_incorrect_answers)

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
            # print(self.answer_results)


file = JSONtoHTML('example2.json', 'rules.txt', 'data.json')
file.render_html()