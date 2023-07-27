/*Classes*/
class Inner{};
class Test{};
class Answer{};
class Question{};
class QuestionThemes{};
class AllThemes{};

/* То, что получает Саша */
const inner = {
  test: "Test",
  themes: "AllThemes",
}

const test = {
  testId: "number",
  subjectId: "number",
  fulltime: "number",
  stage: "number",
  questions: ["Question", "Question", "Question"],
}

const answer = {
  right: "boolean", //Необязательное свойство
  text: "string"
}

const question = {
  questionId: "number",
  task: "string",
  attachment: "string", //Необязательное свойство
  type: "string",
  answers: ["Answer", "Answer", "Answer"],
  time: "string",
  themes: "QuestionThemes",
}

const QuestionThemes = {
  themes: [
    {
      themeName: "string",
      index: "1"
    },
    {
      themeName: "string",
      index: "1.1"
    }
  ],
}

const AllThemes = {
  allThemes: ["QuestionThemes", "QuestionThemes", "QuestionTheme"]
}