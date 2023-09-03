from __future__ import annotations
from dataclasses import dataclass
import json
import copy

RUSSIAN_LANGUAGE_MAX_PRIMARY_SCORE = 80

RUSSIAN_LANGUAGE_TRANSFORM_POINTS = {
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


@dataclass
class Test:
    id: int
    userFullname: str
    date: str
    fullTime: int
    answers: list[Answer]


@dataclass
class DataFromServer:
    id: int
    name: str
    subject: str
    timeCommentaries: str
    questions: list[Question]


@dataclass
class Question:
    id: int
    name: str
    type: str
    task: str
    commentary: str
    acceptableTime: int
    themesIndexes: list[str]
    addition: str = None
    image: str = None
    variants: list[Variant] = None
    letterRatioVariants: list[str] = None
    numericRatioVariants: list[str] = None
    time: int = None
    status: str = None


@dataclass
class Variant:
    id: int
    accuracy: True | False
    text: str = None
    themes: list[str] = None
    isChosen: True | False = None


@dataclass
class Answer:
    id: int
    time: int
    answers: list[str]


@dataclass
class Analytics:
    userFullname: Test.userFullname
    date: Test.date
    subject: DataFromServer.subject
    testName: DataFromServer.name
    primaryScore: int
    testScore: int
    scorePercentage: int
    rightAnswersAmount: int
    partiallyCorrectAnswersAmount: int
    wrongAnswersAmount: int
    themes: list[Theme]
    questions: list[Question]


@dataclass
class Theme:
    index: str
    level: int
    themesList: list[str]
    misunderstandingIndex: int = None


def getData(client, server):
    with open(client, encoding='utf-8') as f:
        data = json.load(f)
        answers: list[Answer] = []
        for answer in data['answers']:
            answers.append(Answer(
                id=answer['id'],
                time=answer['time'],
                answers=answer['answers']
            ))
        test = Test(
            id=data['id'],
            userFullname=data['userFullname'],
            date=data['date'],
            fullTime=data['fullTime'],
            answers=answers
        )

    with open(server, encoding='utf-8') as f:
        data = json.load(f)
        questions: list[Question] = []
        for question in data['questions']:
            if question['type'] == 'variants':
                variants: list[Variant] = []
                for variant in question['variants']:
                    variants.append(Variant(
                        id=variant['id'],
                        text=variant['text'],
                        accuracy=variant['accuracy'],
                        themes=variant['themes']
                    ))
                questions.append(Question(
                    id=question['id'],
                    name=question['name'],
                    type=question['type'],
                    task=question['task'],
                    variants=variants,
                    commentary=question['commentary'],
                    acceptableTime=question['acceptableTime'],
                    themesIndexes=question['themesIndexes']
                ))
            if question['type'] == 'variants_with_addition':
                variants: list[Variant] = []
                for variant in question['variants']:
                    variants.append(Variant(
                        id=variant['id'],
                        accuracy=variant['accuracy'],
                        themes=variant['themes']
                    ))
                questions.append(Question(
                    id=question['id'],
                    name=question['name'],
                    type=question['type'],
                    task=question['task'],
                    addition=question['addition'],
                    variants=variants,
                    commentary=question['commentary'],
                    acceptableTime=question['acceptableTime'],
                    themesIndexes=question['themesIndexes']
                ))
        serverData = DataFromServer(
            id=data['id'],
            name=data['name'],
            subject=data['subject'],
            timeCommentaries=data['timeCommentaries'],
            questions=questions
        )
    return {'test': test, 'serverData': serverData}


class TestHandler:

    def __init__(self, test: Test, serverData: DataFromServer):
        self.test = test
        self.serverData = serverData

    def getThemeLevel(self, themeIndex):
        level = 0
        for symbol in themeIndex:
            if (symbol == '.'):
                level += 1
        return level + 1

    def getThemesList(self, themeIndex: str):
        themesList: list[str] = []
        themesListCopy = themeIndex.split('.')
        for i in range(0, len(themesListCopy)):
            themesList.append(themesListCopy[i])
        return themesList

    def getThemesStr(self, themesList: list):
        return '.'.join(themesList)

    def themeHierarchyCounter(self, themes: list, theme: Theme):
        topThemeThemesList = copy.deepcopy(theme.themesList)
        while len(topThemeThemesList) > 1:
            topThemeThemesList.pop(-1)
            topThemeIndex = self.getThemesStr(topThemeThemesList)
            topTheme = Theme(
                index=topThemeIndex,
                level=self.getThemeLevel(topThemeIndex),
                themesList=self.getThemesList(topThemeIndex),
                misunderstandingIndex=1
            )
            counter = 0
            for theme in themes:
                if theme.index == topThemeIndex:
                    theme.misunderstandingIndex += 1
                else:
                    counter += 1
            if counter == len(themes):
                themes.append(topTheme)

        return themes

    def addThemes(self, themes, indexes):
        for themeIndex in indexes:
            themesCounter = 0
            if len(themes) > 0:
                for theme in themes:
                    if theme.index == themeIndex:
                        theme.misunderstandingIndex += 1
                        themes = self.themeHierarchyCounter(themes, theme)
                    else:
                        themesCounter += 1
            else:
                newTheme = Theme(
                    index=themeIndex,
                    level=self.getThemeLevel(themeIndex),
                    themesList=self.getThemesList(themeIndex),
                    misunderstandingIndex=1
                )
                themes.append(newTheme)
                themes = self.themeHierarchyCounter(themes, newTheme)
            if themesCounter == len(themes):
                newTheme = Theme(
                    index=themeIndex,
                    level=self.getThemeLevel(themeIndex),
                    themesList=self.getThemesList(themeIndex),
                    misunderstandingIndex=1
                )
                themes.append(newTheme)
                themes = self.themeHierarchyCounter(themes, newTheme)

        return themes

    def checkThemesEntry(self, themeThemesList: list[str], topThemeThemesList: list[str]):
        if not len(topThemeThemesList):
            return True
        counter = 0
        if len(topThemeThemesList) <= len(themeThemesList):
            for i in range(0, len(topThemeThemesList)):
                if themeThemesList[i] == topThemeThemesList[i]:
                    counter += 1
            if counter == len(topThemeThemesList):
                return True
            else:
                return False
        else:
            return False

    def themesSort(self, themes: list[Theme]):
        sortedThemes: list[Theme] = []
        level = 1
        topTheme = Theme(
                    index="0",
                    level=1,
                    misunderstandingIndex=0,
                    themesList=[]
                )
        while True:
            if not len(themes):
                break
            else:
                maxMisunderstandingIndex = 0
                newTheme = Theme(
                    index="0",
                    level=1,
                    misunderstandingIndex=0,
                    themesList=[]
                )
                for theme in themes:
                    if theme.level == level and theme.misunderstandingIndex > maxMisunderstandingIndex and self.checkThemesEntry(theme.themesList, topTheme.themesList):
                        newTheme = copy.deepcopy(theme)
                        maxMisunderstandingIndex = theme.misunderstandingIndex
                if newTheme.index != "0":
                    sortedThemes.append(newTheme)
                for theme in themes:
                    if newTheme.index == theme.index:
                        themes.remove(theme)
                if newTheme.index != "0":
                    topTheme = copy.deepcopy(newTheme)
                counter = 0
                for theme in themes:
                    if self.checkThemesEntry(theme.themesList, topTheme.themesList):
                        counter += 1
                if counter:
                    level += 1
                else:
                    if level - 1 == topTheme.level:
                        level -= 1
                    for theme in reversed(sortedThemes):
                        if theme.level == level - 1:
                            topTheme = copy.deepcopy(theme)
                            level = topTheme.level + 1
                            break

        return sortedThemes

    def makeAnalytics(self):
        primaryScore = 0
        rightAnswersAmount = 0
        partiallyCorrectAnswersAmount = 0
        wrongAnswersAmount = 0
        themes: list[Theme] = []
        statuses: list[str] = []
        counters: list[int] = []
        rightAnswersAmounts: list[int] = []
        for question in self.serverData.questions:
            questionRightAnswersAmount = 0
            for variant in question.variants:
                if variant.accuracy:
                    questionRightAnswersAmount += 1
            rightAnswersAmounts.append(questionRightAnswersAmount)
        for userAnswer in self.test.answers:
            counter = 0
            for answer in userAnswer.answers:
                if not self.serverData.questions[userAnswer.id].variants[int(answer) - 1].accuracy:
                    counter += 1
                    themes = self.addThemes(themes,
                                            self.serverData.questions[userAnswer.id].variants[int(answer) - 1].themes)
            for variant in self.serverData.questions[userAnswer.id].variants:
                if not userAnswer.answers.__contains__(str(variant.id + 1)) and variant.accuracy:
                    themes = self.addThemes(themes,
                                            self.serverData.questions[userAnswer.id].variants[variant.id].themes)

            counters.append(counter)
            if counter == 0 and len(userAnswer.answers) == rightAnswersAmounts[userAnswer.id]:
                statuses.append("Верно")
                primaryScore += 2
                rightAnswersAmount += 1
            elif ((counter == 0 and rightAnswersAmounts[userAnswer.id] == len(userAnswer.answers) + 1) or (
                    counter == 1 and rightAnswersAmounts[userAnswer.id] == len(userAnswer.answers) - 1) or (
                          counter == 1 and rightAnswersAmounts[userAnswer.id] == len(userAnswer.answers)
                  )):
                statuses.append("Частично верно")
                primaryScore += 1
                partiallyCorrectAnswersAmount += 1
            else:
                statuses.append("Неверно")
                wrongAnswersAmount += 1
                if counter > 0:
                    themes = self.addThemes(themes, self.serverData.questions[userAnswer.id].themesIndexes)
        scorePercentage = (primaryScore / RUSSIAN_LANGUAGE_MAX_PRIMARY_SCORE) * 100
        testScore = RUSSIAN_LANGUAGE_TRANSFORM_POINTS.get(primaryScore)

        questions: list[Question] = []

        for question in self.serverData.questions:
            variants: list[Variant] = []
            for variant in question.variants:
                if self.test.answers[question.id].answers.__contains__(str(variant.id + 1)):
                    variants.append(Variant(
                        id=variant.id,
                        text=variant.text,
                        accuracy=variant.accuracy,
                        themes=variant.themes,
                        isChosen=True
                    ))
                else:
                    variants.append(Variant(
                        id=variant.id,
                        text=variant.text,
                        accuracy=variant.accuracy,
                        themes=variant.themes,
                        isChosen=False
                    ))
            questions.append(Question(
                id=self.serverData.questions[question.id].id,
                name=self.serverData.questions[question.id].name,
                type=self.serverData.questions[question.id].type,
                task=self.serverData.questions[question.id].task,
                commentary=self.serverData.questions[question.id].commentary,
                acceptableTime=self.serverData.questions[question.id].acceptableTime,
                themesIndexes=self.serverData.questions[question.id].themesIndexes,
                addition=self.serverData.questions[question.id].addition,
                image=self.serverData.questions[question.id].image,
                variants=variants,
                letterRatioVariants=self.serverData.questions[question.id].letterRatioVariants,
                numericRatioVariants=self.serverData.questions[question.id].numericRatioVariants,
                time=self.test.answers[question.id].time,
                status=statuses[question.id]
            ))

        analytics = Analytics(
            userFullname=self.test.userFullname,
            date=self.test.date,
            subject=self.serverData.subject,
            testName=self.serverData.name,
            primaryScore=primaryScore,
            testScore=testScore,
            scorePercentage=int(scorePercentage),
            rightAnswersAmount=rightAnswersAmount,
            partiallyCorrectAnswersAmount=partiallyCorrectAnswersAmount,
            wrongAnswersAmount=wrongAnswersAmount,
            themes=self.themesSort(themes),
            questions=questions
        )

        return analytics

    def getAnalytics(self):
        return self.makeAnalytics()


def main(client, server):
    data = getData(client, server)
    testHandler = TestHandler(data['test'], data['serverData'])
    analytics = testHandler.getAnalytics()
    print(analytics)


main("client.json", "server.json")
