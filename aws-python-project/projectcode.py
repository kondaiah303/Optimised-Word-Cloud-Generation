import json
from nltk.tokenize import word_tokenize
import boto3
client = boto3.client('s3')
BUCKET_NAME = "mybucket3034"
BUCKET_OBJECT_KEY_NAME = "WordFrequencyFile1.json"
LOCAL_FILE_PATH = r'/Users/entropik/PycharmProjects/pythonproject/aws-python-project/WordFrequencyFile.json'
MAX_FREQUENCY_NUMBER = 25


def get_s3_objects():
    try:
        s3bucket_object = client.get_object(Bucket=BUCKET_NAME, Key=BUCKET_OBJECT_KEY_NAME)
    except Exception as e:
        print("S3 File not found"+str(e))
        return {}
    data1 = s3bucket_object['Body'].read()
    py_objects = json.loads(data1)
    return py_objects


def list_of_words_count(payload):
    tokenized_text = word_tokenize(payload)
    words_list = []
    for words in tokenized_text:
        if words.isalpha():
            words_list.append(words)
    py_objects = get_s3_objects()
    for word in words_list:
        if word in py_objects:
            py_objects[word] = py_objects.get(word) + 1
        elif word not in py_objects:
            py_objects[word] = 1
    sorted_dict = dict(sorted(py_objects.items(), key=lambda item: item[1], reverse=True))
    update_file = open(LOCAL_FILE_PATH, 'w')
    json.dump(sorted_dict, update_file, indent=3)
    update_file.close()
    upload_files()
    py_objects_max_frequency_number = {}
    frequency = 1
    for i, j in py_objects.items():
        if frequency <= MAX_FREQUENCY_NUMBER:
            py_objects_max_frequency_number.update({i: j})
        frequency += 1
    print(py_objects_max_frequency_number)
    return {"statusCode": 200, "body": json.dumps(py_objects_max_frequency_number)}


def upload_files():
    client.upload_file(LOCAL_FILE_PATH, BUCKET_NAME, BUCKET_OBJECT_KEY_NAME)
