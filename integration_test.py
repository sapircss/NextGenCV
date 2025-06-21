# integration_test.py
import requests

def test_upload():
    url = "http://10.100.102.4/api/upload"
    file = {'file': open('/home/asher/Desktop/2030/AsherResume.pdf', 'rb')}
    response = requests.post(url, files=file)
    print("Upload:", response.status_code, response.json())

# def test_parse():
#     url = "http://localhost:8002/parse_resume/"
#     data = {"file_path": "uploads/sample_resume.pdf"}
#     response = requests.post(url, json=data)
#     print("Parse:", response.status_code, response.json())

# def test_enhance():
#     url = "http://localhost:8003/enhance_resume/"
#     data = {"text": "I am a Software Developer skilled in Python."}
#     response = requests.post(url, json=data)
#     print("Enhance:", response.status_code, response.json())

if __name__ == "__main__":
    test_upload()
    # test_parse()
    # test_enhance()
