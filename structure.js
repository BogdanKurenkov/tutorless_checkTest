/*Classes*/
class Test{};
class User{};
class Question{};

/* То, что получает Саша. Объект класса Test */

const test = {
  userFullname: "string",
  date: "string",
  name: "string",
  subject: "string",
  fullTime: "string",
  questions: "Question[]",
}

const question = {
  id: "number",
  name: "string",
  type: "string",
  addition: "string", //Необязательное свойство
  task: "string",
  image: "string", //Необязательное свойство
  variants: "string[]", //Необязательное свойство
  answers: "string[]",
}