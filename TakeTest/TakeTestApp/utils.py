import datetime, os, json
from . import forms
from . import models
from TakeTest import settings

class BackendOperations():
    def __init__(self):
        pass

    def upload_test(self, request):
        form = forms.UploadTestForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            new_entry = form.save(commit=False)
            new_entry.test_name = request.POST.get('test_name')
            new_entry.author_id = request.user.id
            new_entry.save()
            return new_entry
        return None

    def calculate_score(self, answer_dump, test_obj):
        file_path = os.path.join(settings.MEDIA_ROOT, str(test_obj.test_file))
        with open(file_path) as test_file:
            ques_dump =  json.loads(test_file.read())
        ques_and_ans_list = ques_dump['questions']
        total_ques = len(ques_and_ans_list)
        score = 0
        for ans in answer_dump:
            ques_num = ans['question_number']
            actual_ans_list = ans['answers_list']
            expected_ans_list = [item['answers_list'] for item in ques_and_ans_list if ques_num == item['question_number']]
            expected_ans_list[0].sort()
            actual_ans_list.sort()
            if expected_ans_list[0] == actual_ans_list:
                score = score + 1
        return (score/total_ques)*100
