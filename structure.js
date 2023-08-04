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
  type: "string", //(типы вопросов: variants, textarea, variants_with_textarea, variants_with_picture, textarea_with_picture, variants_addition, textarea_with_addition, ratio)
  addition: "string", //Необязательное свойство
  task: "string",
  image: "string", //Необязательное свойство
  variants: "string[]", //Необязательное свойство
  letterVariants: "string[]", //Необязательное свойство
  numericVariants: "string[]", //Необязательное свойство
  answers: "string[]",
}