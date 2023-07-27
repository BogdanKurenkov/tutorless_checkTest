import json
import re

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


def convert_time(time):  
    mins = 0
    secs = time
    while secs - 60 >= 0:
        mins += 1
        secs -= 60
    converted = ""
    if mins < 10:
        if secs < 10:
            converted = f"0{mins}:0{secs}"
        else:
            converted = f"0{mins}:{secs}"
    else:
        if secs < 10:
            converted = f"{mins}:0{secs}"
        else:
            converted = f"{mins}:{secs}"
    return converted


class Test:

    def __init__(self, filename_test, filename_rules):
        with open(filename_test, 'r', encoding="utf-8") as test_data_file:
            general_data = json.load(test_data_file)
            self.user_name = general_data['inner']['username']
            self.test_date = general_data['inner']['test_date']
            self.test_name = general_data['test']['testId']
            self.test_subject = general_data['test']["subjectId"],
            self.test_fulltime = general_data['test']["fulltime"],
            self.test_stage = general_data['test']["stage"],
            self.test_questions_answers = general_data['test']['questions']
            self.general_score = 0
            self.general_time = 0
            self.time_recommendation = ""
            self.strings = ["" for i in range(9)]
        with open(filename_rules, 'r', encoding="utf8") as rules_data_file:
            rules_data_file = rules_data_file.read()

        rules_data_file = rules_data_file.replace('\xad', '')
        rules_data_file = rules_data_file.replace('\t', '')


        splitted_rules = rules_data_file.split('\n')
        print(splitted_rules)
        self.rules = {}
        self.rules_list = {}
        self.recommendations_index = {"general_score": self.general_score, "time_recommendation":
            self.time_recommendation,
                                      "rules": []}
        print(len(splitted_rules))
        k = 0
        for i in splitted_rules:
            try:
                k += 1
                print(k, '-я итерация запустилась')
                print(i)
                key, value = i.split(" ", 1)
                self.rules[key] = value
                print(k, '-я прошла успешно')
            except:
                continue
        self.num_of_correct_answers = 0
        self.num_of_half_correct_answers = 0
        self.num_of_incorrect_answers = 0

    def make_user_score(self) -> list:

        self.user_index = {}
        user_commentaries = {}
        for i in self.rules.keys():
            self.user_index[i] = 0

        for question in self.test_questions_answers:

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
                                self.num_of_incorrect_answers += 1

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
                    self.general_score += 2
                    self.num_of_correct_answers += 1

                elif check_if_incorrect == 0 and check_if_not_equal == 1:
                    self.general_score += 1
                    self.num_of_half_correct_answers = 0

                else:
                    self.num_of_incorrect_answers += 1

            if question_info["type"] == 'word':  # если тип вопроса - найти подходящее слово
                if answers != user_answer:
                    self.num_of_incorrect_answers += 1
                    for theme in themes:
                        if type(theme) == list:
                            for subtheme in theme:
                                self.user_index[subtheme + '.'] += 1
                        else:
                            self.user_index[theme + '.'] += 1

                else:
                    self.general_score += 2
                    self.num_of_correct_answers += 1

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
                        self.num_of_incorrect_answers += 1
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
                    self.general_score += 2

                elif check_if_not_equal == 1 and check_if_incorrect == 0:
                    self.general_score += 1
                    self.num_of_half_correct_answers += 1

                else:
                    self.num_of_incorrect_answers += 1

            if question_info["type"] == 'АБВГ_string':  # если тип вопроса - соотнести варианты из 2 колонок

                check_if_incorrect = 0
                check_if_correct = 0

                for i in range(len(user_answer)):
                    if i % 2 != 0:

                        if user_answer[i] != answers[i]:
                            check_if_incorrect += 1
                            self.num_of_incorrect_answers += 1
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
                    self.general_score += 2

                if check_if_incorrect == 0 and check_if_correct < 4:
                    self.general_score += 1

                elif check_if_incorrect == 1:
                    self.general_score += 1
                    self.num_of_half_correct_answers += 1

                else:
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

        self.test_points = TRANSFORM_POINTS[self.general_score]

        if self.general_time < 1200:
            self.time_recommendation = "that's the right way to do!"

        if 1200 <= self.general_time < 1600:
            self.time_recommendation = "you're close to run out of time!"

        if self.general_time > 1600:
            self.time_recommendation = "you have to do it faster!"

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
        # print(self.recommendations_index)
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
                self.strings[int(key_list[
                                     0]) - 1] = f"<p class =\"normal0\" style=\"text-indent:36pt; line-height:115%; font-size:10pt\" > <span " \
                                                f"style = \"font-family:Montserrat; font-style:italic; color:#1c4587\" > {THEMES[int(key_list[0]) - 1]} </span></p> "
            if self.rules[new_key] not in self.rules_list:
                temp_list.insert(0, self.rules[new_key])
            if len(key_list) > 2:
                for i in range(2, len(key_list)):
                    new_key += key_list[i] + '.'
                    temp_list.append(self.rules[new_key])
            complete_rules.append(temp_list)
        return complete_rules

    def add_consultation(self):
        string_to_insert = f"<p class=\"normal0\"" \
                           f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                           f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>" \
                           f"<p class=\"normal0\" "
        string_to_insert += " <p class=\"normal0\" style=\"margin-right:4.1pt; line-height:normal; widows:0; orphans:0; font-size:12pt\"><span " \
                            "style=\"font-family:Montserrat; font-weight:bold\">Консультация по вопросам</span> " \
                            "</p> <p class=\"normal0\" style=\"margin-right:4.1pt; line-height:normal; widows:0; orphans:0\"><span " \
                            "style=\"-aw-import:ignore\">&#xa0;</span></p>"
        counter = 0
        for question_answer in self.test_questions_answers:
            counter += 1
            question = question_answer["question"]
            answer = question_answer["answer"]
            task = question["task"]
            time = convert_time(int(question["time"]))
            commentary = question["commentary"]

            to_insert = f"<p class=\"normal0\"" \
                        f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                        f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>"
            if question["questionId"] == "A1":
                to_insert += f" <ol style=\"margin:0pt; padding-left:0pt\">" \
                             f"<li class=\"normal0\" " \
                             f"style=\"margin-right:5.7pt; margin-left:7.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-family:Montserrat; font-size:12pt; font-weight:bold; list-style-position:inside; -aw-list-padding-sml:9.05pt\">" \
                             f" <span style=\"width:9.05pt; font:7pt 'Times New Roman'; display:inline-block; -aw-import:ignore\">&#xa0;&#xa0;&#xa0;&#xa0;&#xa0; </span><span>{task} </span>" \
                             f"</li>"
            else:
                to_insert += f"<li class=\"normal0\" " \
                             f"style=\"margin-right:5.7pt; margin-left:7.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-family:Montserrat; font-size:12pt; font-weight:bold; list-style-position:inside; -aw-list-padding-sml:9.05pt\">" \
                             f" <span style=\"width:9.05pt; font:7pt 'Times New Roman'; display:inline-block; -aw-import:ignore\">&#xa0;&#xa0;&#xa0;&#xa0;&#xa0; </span><span>{task}</span>" \
                             f" </li>"
            if question["type"] == "string":
                if question["questionId"] in ["A17", "A18", "A19"]:
                    text = question["text"]
                    to_insert += f"<p class=\"normal0\" " \
                                 f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p> " \
                                 f"<p class=\"normal0\" " \
                                 f" style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"width:36pt; font-family:Montserrat; display:inline-block\">&#xa0;</span><span " \
                                 f"style=\"font-family:Montserrat\">{text}</span></span> " \
                                 f"</p>"
                variants = question["variants"]
                if len(variants) > 1:
                    for var in range(len(variants)):
                        if (var + 1) in answer["text"]:
                            to_insert += f" <p class=\"normal0\" " \
                                         f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                         f"<span style=\"font-family:Montserrat\">{var + 1} {variants[var]} ☑</span></p> "
                        else:
                            to_insert += f"<p class=\"normal0\" " \
                                         f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                         f"<span style=\"font-family:Montserrat\">{var + 1} {variants[var]} ☐</span></p> "
                else:
                    to_insert += f" <p class=\"normal0\"" \
                                 f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\">" \
                                 f"<span style=\"font-family:Montserrat\">{variants[0]}</span></p>"

                to_insert += f"<p class=\"normal0\"" \
                             f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                             f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>" \
                             f"<p class=\"normal0\" " \
                             f" style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                             f"<span style=\"width:36pt; font-family:Montserrat; display:inline-block\">&#xa0;</span><span " \
                             f"style=\"font-family:Montserrat; color:#1c4587\">Затраченное время:</span><span style=\"font-family:Montserrat\"> {time}.</span> " \
                             f"</p>"

                for i in range(len(commentary)):
                    if i == 0:
                        to_insert += f"<p class=\"normal0\" " \
                                     f"style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                     f"<span style=\"font-family:Montserrat; font-style:italic; -aw-import:ignore\">&#xa0;</span></p>" \
                                     f"<table cellspacing=\"0\" cellpadding=\"0\" class=\"Table2\"" \
                                     f"style=\"width:451.75pt; border:1pt solid #000000; -aw-border-insideh:1pt single #000000; -aw-border-insidev:1pt single #000000; border-collapse:collapse\">" \
                                     f" <tr>" \
                                     f"<td style=\"padding:16.35pt 15.85pt; vertical-align:top\"><p class=\"normal0\"" \
                                     f"style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\">" \
                                     f"<span style=\"font-family:Montserrat; font-style:italic\">{i + 1}) {commentary[i]}</span>" \
                                     f"</p>"
                    else:
                        to_insert += f"<p class=\"normal0\"" \
                                     f"style=\"margin-right:5.7pt; text-align:justify; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\">" \
                                     f"<span style=\"font-family:Montserrat; font-style:italic\">{i + 1}) {commentary[i]}</span>" \
                                     f"</p> "
                        if i == len(commentary) - 1:
                            to_insert += "</td> " \
                                         "</tr> " \
                                         "</table>"
            if question["type"] == "word":
                text = question["text"]
                right_word = answer["text"]
                to_insert += f"<p class=\"normal0\"" \
                             f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                             f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>" \
                             f"<p class=\"normal0\" " \
                             f" style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                             f"<span style=\"width:36pt; font-family:Montserrat; display:inline-block\">&#xa0;</span><span " \
                             f"style=\"font-family:Montserrat\">{text}</span></span>" \
                             f"</p>"
                to_insert += f"<p class=\"normal0\"" \
                             f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                             f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>" \
                             f"<p class=\"normal0\" " \
                             f" style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                             f"<span style=\"width:36pt; font-family:Montserrat; display:inline-block\">&#xa0;</span><span " \
                             f"style=\"font-family:Montserrat; color:#1c4587\">Затраченное время:</span><span style=\"font-family:Montserrat\"> {time}.</span> " \
                             f"</p>"
                to_insert += f"<p class=\"normal0\"" \
                             f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                             f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>" \
                             f"<p class=\"normal0\" " \
                             f" style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                             f"<span style=\"width:36pt; font-family:Montserrat; display:inline-block\">&#xa0;</span><span " \
                             f"style=\"font-family:Montserrat\">Правильный ответ: {right_word}</span></span>" \
                             f"</p>"
                to_insert += f"<p class=\"normal0\"" \
                             f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                             f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>" \
                             f"<p class=\"normal0\" " \
                             f" style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                             f"<span style=\"width:36pt; font-family:Montserrat; display:inline-block\">&#xa0;</span><span " \
                             f"style=\"font-family:Montserrat\">{commentary[0]}</span></span>\"" \
                             f"</p>"

            if question["type"] == "list_word":
                if question["questionId"] == "B13" or question["questionId"] == "B8":
                    text = question["text"]
                    right_word = answer["text"]
                    to_insert += f"<p class=\"normal0\"" \
                                 f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>" \
                                 f"<p class=\"normal0\" " \
                                 f" style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"width:36pt; font-family:Montserrat; display:inline-block\">&#xa0;</span><span " \
                                 f"style=\"font-family:Montserrat\">{text}</span></span>" \
                                 f"</p>"
                    to_insert += f"<p class=\"normal0\"" \
                                 f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>" \
                                 f"<p class=\"normal0\" " \
                                 f" style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"width:36pt; font-family:Montserrat; display:inline-block\">&#xa0;</span><span " \
                                 f"style=\"font-family:Montserrat; color:#1c4587\">Затраченное время:</span><span style=\"font-family:Montserrat\"> {time}.</span> " \
                                 f"</p>"
                    to_insert += f"<p class=\"normal0\"" \
                                 f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>" \
                                 f"<p class=\"normal0\" " \
                                 f" style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"width:36pt; font-family:Montserrat; display:inline-block\">&#xa0;</span><span " \
                                 f"style=\"font-family:Montserrat\">Правильный ответ: {right_word}</span></span>" \
                                 f"</p>"
                    to_insert += f"<p class=\"normal0\"" \
                                 f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>" \
                                 f"<p class=\"normal0\" " \
                                 f" style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"width:36pt; font-family:Montserrat; display:inline-block\">&#xa0;</span><span " \
                                 f"style=\"font-family:Montserrat\">{commentary[0]}</span></span>" \
                                 f"</p>"
                else:
                    print(question["questionId"])
                    variants = question["variants"]
                    for var in range(len(variants)):
                        if str(var + 1) in answer["text"]:
                            to_insert += f" <p class=\"normal0\"" \
                                         f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\">" \
                                         f"<span style=\"font-family:Montserrat\">{var + 1} {variants[var]} ☑</span></p>"
                        else:
                            to_insert += f"<p class=\"normal0\"" \
                                         f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\">" \
                                         f"<span style=\"font-family:Montserrat\">{var + 1} {variants[var]} ☐</span></p>"

                    to_insert += f"<p class=\"normal0\"" \
                                 f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>" \
                                 f"<p class=\"normal0\" " \
                                 f" style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"width:36pt; font-family:Montserrat; display:inline-block\">&#xa0;</span><span " \
                                 f"style=\"font-family:Montserrat; color:#1c4587\">Затраченное время:</span><span style=\"font-family:Montserrat\"> {time}.</span> " \
                                 f"</p>"

                    if len(commentary) > 1:

                        for i in range(len(commentary)):
                            if i == 0:
                                to_insert += f"<p class=\"normal0\" " \
                                             f"style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                             f"<span style=\"font-family:Montserrat; font-style:italic; -aw-import:ignore\">&#xa0;</span></p>" \
                                             f"<table cellspacing=\"0\" cellpadding=\"0\" class=\"Table2\"" \
                                             f"style=\"width:451.75pt; border:1pt solid #000000; -aw-border-insideh:1pt single #000000; -aw-border-insidev:1pt single #000000; border-collapse:collapse\">" \
                                             f" <tr>" \
                                             f"<td style=\"padding:16.35pt 15.85pt; vertical-align:top\"><p class=\"normal0\"" \
                                             f"style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\">" \
                                             f"<span style=\"font-family:Montserrat; font-style:italic\">{i + 1}) {commentary[i]}</span>" \
                                             f"</p>"
                            else:
                                to_insert += f"<p class=\"normal0\"" \
                                             f"style=\"margin-right:5.7pt; text-align:justify; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\">" \
                                             f"<span style=\"font-family:Montserrat; font-style:italic\">{i + 1}) {commentary[i]}</span>" \
                                             f"</p> "
                                if i == (len(commentary) - 1):
                                    to_insert += "</td> " \
                                                 "</tr> " \
                                                 "</table>"
                    else:
                        to_insert += f"<p class=\"normal0\"" \
                                     f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                     f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>" \
                                     f"<p class=\"normal0\" " \
                                     f" style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                     f"<span style=\"width:36pt; font-family:Montserrat; display:inline-block\">&#xa0;</span><span " \
                                     f"style=\"font-family:Montserrat\">{commentary[0]}</span></span>\"" \
                                     f"</p>"

            if question["type"] == "АБВГ_string":
                num_variants = question["num_variants"]
                A_variants = question["A_variants"]
                right_word = answer["text"]
                a_markers = "АБВГ"
                for var in range(len(A_variants)):
                    to_insert += f"<p class=\"normal0\" " \
                                 f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"font-family:Montserrat\">{a_markers[var]}. {A_variants[var]}</span></p> "
                to_insert += f"<p class=\"normal0\" " \
                             f"style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                             f"<span style=\"font-family:Montserrat; font-style:italic; -aw-import:ignore\">&#xa0;</span></p>"

                for var in range(len(num_variants)):
                    to_insert += f"<p class=\"normal0\" " \
                                 f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"font-family:Montserrat\">{var + 1} {num_variants[var]}</span></p> "

                to_insert += f"<p class=\"normal0\"" \
                             f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                             f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>" \
                             f"<p class=\"normal0\" " \
                             f" style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                             f"<span style=\"width:36pt; font-family:Montserrat; display:inline-block\">&#xa0;</span><span " \
                             f"style=\"font-family:Montserrat; color:#1c4587\">Затраченное время:</span><span style=\"font-family:Montserrat\"> {time}.</span> " \
                             f"</p>"

                to_insert += f"<p class=\"normal0\"" \
                             f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                             f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>" \
                             f"<p class=\"normal0\" " \
                             f" style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                             f"<span style=\"width:36pt; font-family:Montserrat; display:inline-block\">&#xa0;</span><span " \
                             f"style=\"font-family:Montserrat\">Правильный ответ: {right_word}</span></span>" \
                             f"</p>"

                if len(commentary) > 1:
                    for i in range(len(commentary)):
                        if i == 0:
                            to_insert += f"<p class=\"normal0\" " \
                                         f"style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                         f"<span style=\"font-family:Montserrat; font-style:italic; -aw-import:ignore\">&#xa0;</span></p>" \
                                         f"<table cellspacing=\"0\" cellpadding=\"0\" class=\"Table2\"" \
                                         f"style=\"width:451.75pt; border:1pt solid #000000; -aw-border-insideh:1pt single #000000; -aw-border-insidev:1pt single #000000; border-collapse:collapse\">" \
                                         f" <tr>" \
                                         f"<td style=\"padding:16.35pt 15.85pt; vertical-align:top\"><p class=\"normal0\"" \
                                         f"style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\">" \
                                         f"<span style=\"font-family:Montserrat; font-style:italic\">{i + 1}) {commentary[i]}</span>" \
                                         f"</p>"
                        else:
                            to_insert += f"<p class=\"normal0\"" \
                                         f"style=\"margin-right:5.7pt; text-align:justify; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\">" \
                                         f"<span style=\"font-family:Montserrat; font-style:italic\">{i + 1}) {commentary[i]}</span>" \
                                         f"</p> "
                            if i == (len(commentary) - 1):
                                to_insert += "</td> " \
                                             "</tr> " \
                                             "</table>"
                else:
                    to_insert += f"<p class=\"normal0\"" \
                                 f"style=\"margin-right:5.7pt; margin-left:43.05pt; text-indent:7.05pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"font-family:Montserrat; -aw-import:ignore\">&#xa0;</span></p>" \
                                 f"<p class=\"normal0\" " \
                                 f" style=\"margin-right:5.7pt; line-height:normal; widows:0; orphans:0; font-size:12pt; background-color:#ffffff\"> " \
                                 f"<span style=\"width:36pt; font-family:Montserrat; display:inline-block\">&#xa0;</span><span " \
                                 f"style=\"font-family:Montserrat\">{commentary[0]}</span></span>" \
                                 f"</p>"
            string_to_insert += to_insert
            if question["questionId"] == "B22":
                string_to_insert += " </ol>"

        return string_to_insert

    def make_html_file(self):
        data = ''
        with open("analytics.html", 'r+', encoding='utf-8') as output_file:
            data = output_file.read()
        with open("new_table.html", 'w', encoding='utf-8') as output_file1:
            data = data.replace("schoolboy_name", self.user_name)
            data = data.replace("test_date", self.test_date)
            data = data.replace("test_name", self.test_name)
            data = data.replace("schoolboy_name", self.user_name)
            data = data.replace("first_points", str(self.general_score))
            data = data.replace("test_points", str(self.test_points))
            data = data.replace("time_of_solving", str(self.general_time))
            data = data.replace("num_of_correct_answers", str(self.num_of_correct_answers))
            data = data.replace("num_of_incorrect_answers", str(self.num_of_incorrect_answers))
            output_file1.write(data)
            complete_rules = self.complete_rules_list()
            for i in range(len(complete_rules)):
                string_to_insert = ""
                for j in range(len(complete_rules[i])):
                    if complete_rules[i][j] not in self.rules_list.values():
                        if j == 0:
                            string_to_insert += f"<p class=\"normal0\" style=\"margin-left:{36 * (j + 1)}pt; text-indent:-18pt;" \
                                                f"line-height:115%; font-size:12pt; -aw-import:list-item; " \
                                                f"-aw-list-level-number:{j}; " \
                                                f"-aw-list-number-format:\'●\'; -aw-list-number-styles:\'bullet\';" \
                                                f"-aw-list-padding-sml:10.96pt\">" \
                                                f"<span style=\"-aw-import:ignore\"><span " \
                                                f"style=\"font-family:Montserrat\"><span>●</span></span><span " \
                                                f"style=\"width:10.96pt; font:7pt 'Times New Roman'; display:inline-block; " \
                                                f"-aw-import:spaces\">&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;" \
                                                f" </span></span><span style=\"font-family:Montserrat\">{complete_rules[i][j]}</span></p> "
                        else:
                            string_to_insert += f"<p class=\"normal0\" style=\"margin-left:{36 * (j + 1)}pt; text-indent:-18pt;" \
                                                f"line-height:115%; font-size:12pt; -aw-import:list-item; " \
                                                f"-aw-list-level-number:{j};" \
                                                f"-aw-list-number-format:\'○\'; -aw-list-number-styles:\'bullet\';" \
                                                f"-aw-list-padding-sml:10.96pt\">" \
                                                f"<span style=\"-aw-import:ignore\"><span " \
                                                f"style=\"font-family:Montserrat\"><span>○</span></span><span " \
                                                f"style=\"width:10.96pt; font:7pt 'Times New Roman'; display:inline-block;  " \
                                                f"-aw-import:spaces\">&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;" \
                                                f" </span></span><span style=\"font-family:Montserrat\">{complete_rules[i][j]}</span></p> "
                    else:
                        string_to_insert += f"<p class=\"normal0\" style=\"margin-left:{36 * (j + 1)}pt; text-indent:-18pt;" \
                                            f"line-height:normal; widows:0; orphans:0; font-size:12pt; -aw-import:list-item; " \
                                            f"-aw-list-level-number:{j};" \
                                            f"-aw-list-number-format:\'■\'; -aw-list-number-styles:\'bullet\';" \
                                            f"-aw-list-padding-sml:10.8pt\">" \
                                            f"<span style=\"-aw-import:ignore\"><span " \
                                            f"style=\"font-family:Montserrat; font-weight:bold\"><span style=\"font-weight:normal\">■</span></span><span " \
                                            f"style=\"width:10.8pt; font:7pt 'Times New Roman'; display:inline-block;  " \
                                            f"-aw-import:spaces\">&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;" \
                                            f" </span></span><span style=\"font-family:Montserrat; font-weight:bold\">{complete_rules[i][j]}</span></p> "
                        ierarchy = 0
                        for k in self.rules_list.keys():
                            if self.rules_list[k] == complete_rules[i][j]:
                                ierarchy = k[0]
                        self.strings[int(ierarchy) - 1] += string_to_insert

            string_for_html_file = ""
            for i in self.strings:
                if i != "":
                    string_for_html_file += i

            string_for_html_file += self.add_consultation()
            output_file1.write(string_for_html_file)


good_test = Test("test.json", "rules.txt")

good_recs_index, rules_list = good_test.make_recommendations()
good_test.make_html_file()
