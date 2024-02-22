from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure
from six import string_types
import time
import random

class TestBigFive(BaseCase):

    id_test = 689835470004879361                    # не понял, только один вариант теста?
    post_url = '/dating/user-analitics/tags/'

    answers = []
    results = []

    @allure.description("This main test, collect data")
    def test_get_big_five(self):

        ############################### 1 получаем вопросы
        res = MyRequests.get(f"/dating/public-interview/{self.id_test}/questions/")
        #print(res.content)

        Assertions.assert_code_status(res, 200)

        #json ли ?
        self.answers = Assertions.assert_json(res)
#        print(f" 1 :  {self.answers}")
        TestBigFive.answers = self.answers      # проверить в других тестах

        #собираем запрос для post    {"questionId":"696039351758290945","answer":1}
        answers_p = []
        for answer in self.answers:
            answer_post = {
                'questionId': answer['id'],
                'answer': 1
            }
            #print(answer_post)
            answers_p.append(answer_post)

        answers_for_post = { "answers": answers_p }
        #print(answers_for_post)

        ################################## 2 отправляем ответы
        res2 = MyRequests.post_j(self.post_url, data=answers_for_post)

        Assertions.assert_code_status(res2, 200)
        self.results = Assertions.assert_json(res2)

        TestBigFive.results = self.results
        # print(self.results)

    # проверяем ответы
    @allure.description("This test checks correction of answers")
    def test_check_answers(self):

        answers = TestBigFive.answers
        keys = ['id', 'text', 'interview']

        # print(f" 2 :  {answers} type {type(answers)}")

        assert type(answers) is list,  f"Wrong type answers: {answers}"
        assert len(answers) > 0,  f"Wrong count answers: {answers} count: {len(answers)}"

        for answer in self.answers:
            assert type(answer) is dict, f"Wrong type answer: {answers}"
            assert len(list(answer.keys())) == len(keys), f"Wrong count keys answer: {answers}"
            Assertions.assert_dict_has_keys(answer, keys)
            assert int(answer['id']) > 0, f"Wrong answer id: {answer['id']}"
            assert isinstance(answer['text'], string_types), f"Wrong answer text: {answer['text']}"
            assert int(answer['interview']) > 0, f"Wrong answer interview: {answer['interview']}"

    # проверяем базовый результат анкетирования
    @allure.description("This test checks final results")
    def test_check_results(self):

        results = TestBigFive.results

        self.check_results(results)

    def check_results(self, results: list):

        keys = ['name', 'description', 'percent']

        assert type(results) is list,  f"Wrong type results: {results}"
        assert len(results) > 0 ,  f"Wrong count results: {len(results)}"

        # print(results)
        for desc in results:
            assert type(desc) is dict, f"Wrong type results: {desc}"
            assert len(list(desc.keys())) == len(keys), f"Wrong count keys results: {desc}"
            Assertions.assert_dict_has_keys(desc, keys)
            assert isinstance(desc['name'], string_types), f"Wrong results text: {desc['name']}"
            assert isinstance(desc['description'], string_types), f"Wrong results description: {desc['description']}"
            assert int(desc['percent']) > 0, f"Wrong result percent: {desc['percent']}"

    # позитивные
    @allure.description("This pozitive test, checks all answers")
    def test_pozitive_answers_all(self):

        answers = TestBigFive.answers # возьмем за основу

        assert type(answers) is list,  f"Wrong type answers: {answers}"
        assert len(answers) > 0,  f"Wrong count answers: {answers}"

        # только такие ответы могут быть
        l_answrs = [1,2,3,4,5,6,7]

        #прогоним по всем вариантам ответа
        for new_answer in l_answrs:
            answers_p = []
            for answer in answers:
                answer_post = {
                    'questionId': answer['id'],
                    'answer': new_answer
                }
                answers_p.append(answer_post)

            answers_for_post = {"answers": answers_p}
            print(answers_for_post)
            res = MyRequests.post_j(self.post_url, data=answers_for_post)
            Assertions.assert_code_status(res, 200)

            # чтоб не ддосить
            time.sleep(.2)

            results = Assertions.assert_json(res)
            self.check_results(results)

    #ну и несколько с рандомными
    @allure.description("This pozitive test, checks random answers")
    def test_pozitive_answers_random(self):

        answers = TestBigFive.answers  # возьмем за основу

        assert type(answers) is list, f"Wrong type answers: {answers}"
        assert len(answers) > 0, f"Wrong count answers: {answers}"

        for i in range(6):
            answers_p = []
            for answer in answers:
                answer_post = {
                    'questionId': answer['id'],
                    'answer': random.randrange(1,7)
                }
                answers_p.append(answer_post)

            answers_for_post = {"answers": answers_p}
            print(answers_for_post)
            res = MyRequests.post_j(self.post_url, data=answers_for_post)
            Assertions.assert_code_status(res, 200)

            # чтоб не ддосить
            time.sleep(.2)

            results = Assertions.assert_json(res)
            self.check_results(results)


    # негативные
    @allure.description("This negative test, checks few answers")
    def test_negative_answers_few(self):

        answers = TestBigFive.answers # возьмем за основу
        assert type(answers) is list,  f"Wrong type answers: {answers}"
        assert len(answers) > 0,  f"Wrong count answers: {answers}"

        # мало ответов
        answers_p = []
        for i in range(3):
            answer_post = {
                'questionId': answers[i]['id'],
                'answer': 1
            }
            answers_p.append(answer_post)

        answers_for_post = {"answers": answers_p}
        print(answers_for_post)
        res = MyRequests.post_j(self.post_url, data=answers_for_post)
        Assertions.assert_code_status(res, 500)     #тут отдал 200, наверное правильно

    @allure.description("This negative test, checks many answers")
    # много ответов
    def test_negative_answers_many(self):

        answers = TestBigFive.answers  # возьмем за основу
        assert type(answers) is list, f"Wrong type answers: {answers}"
        assert len(answers) > 0, f"Wrong count answers: {answers}"

        answers_p = []
        for answer in answers:
            answer_post = {
                'questionId': answer['id'],
                'answer': 1
            }
            answers_p.append(answer_post)
        for answer in answers:
            answer_post = {
                'questionId': answer['id'],
                'answer': 2
            }
            answers_p.append(answer_post)

        answers_for_post = {"answers": answers_p}
        print(answers_for_post)
        res = MyRequests.post_j(self.post_url, data=answers_for_post)
        Assertions.assert_code_status(res, 200)         #тут отдал 200, наверное правильно

    @allure.description("This negative test, checks bad answer")
    def test_negative_answers_bad_id(self):

        answers = TestBigFive.answers  # возьмем за основу
        assert type(answers) is list, f"Wrong type answers: {answers}"
        assert len(answers) > 0, f"Wrong count answers: {answers}"

        answers_p = []
        for answer in answers:
            answer_post = {
                'questionId': answer['id'],
                'answer': 'proverka'
            }
            answers_p.append(answer_post)

        answers_for_post = {"answers": answers_p}
        print(answers_for_post)
        res = MyRequests.post_j(self.post_url, data=answers_for_post)
        Assertions.assert_code_status(res, 500)

    @allure.description("This negative test, checks bad questionId")
    def test_negative_answers_bad_id(self):

        answers = TestBigFive.answers  # возьмем за основу
        assert type(answers) is list, f"Wrong type answers: {answers}"
        assert len(answers) > 0, f"Wrong count answers: {answers}"

        answers_p = []
        for answer in answers:
            answer_post = {
                'questionId': 'proverka',
                'answer': 1
            }
            answers_p.append(answer_post)

        answers_for_post = {"answers": answers_p}
        print(answers_for_post)
        res = MyRequests.post_j(self.post_url, data=answers_for_post)
        Assertions.assert_code_status(res, 500)


