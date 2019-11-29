import requests

def read_from_file(filepath):
  """

  (string) -> list or None

  Function read text list from text file

  """

  try:
    with open(filepath, encoding='utf8') as file:
      text_list = [str.strip() for str in file]
    return text_list
  except FileNotFoundError:
    print(f"Файл {filepath} не найден.")

def write_to_file(filepath, lines):
  """

  (string, string) -> int or None

  Function writes text list from text file

  """
  try:
    with open(filepath, 'w', encoding='utf8') as file:
      file.writelines(lines)
    return 0
  except PermissionError:
    print(f"Нет прав для создания файла {filepath}.")

def translate_file(filepath_from, filepath_to, lang_from, lang_to = "ru"):
  """

  (string, string, string, string) -> None

  Function executes translating file from one language to another

  """

  # all what we need to ask Yandex Translate
  api_key = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
  url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

  # Read source textfile
  texts = read_from_file(filepath_from)
  if texts == None:
    return

  params = {
    "key": api_key,
    "text": "",
    "lang": f"{lang_from}-{lang_to}",
  }

  # Get tranlated strings
  lines = ""
  for text in texts:
    if len(text) <= 0:
      continue
    params["text"] = text
    response = requests.get(url, params=params)
    json_ = response.json()
    lines = lines + "".join(json_["text"]) + "\n\n"

  if write_to_file(filepath_to, lines):
    print(f"Файл \"{filepath_from}\" переведен. Результат в файле \"{filepath_to}\".")

def upload_file_to_yandexdisk(filename):
  """

  (string, string, string, string) -> None

  Function upload file to Yandex Disk

  """

  # This token was get on the site YANDEX DISK
  token = "AgAAAAAB684qAADLW6F61GPlN0Pshb69CRBaQ3Y"
  url = r"https://cloud-api.yandex.net/v1/disk/resources/upload"

  params = {
    "path": filename,
    "overwrite": "true"
  }

  headers = {"Authorization": f"OAuth {token}"}

  try:
    response = requests.get(url, headers=headers, params=params)
    json_ = response.json()
    link_for_upload = json_["href"]
    # print(fr"{link_for_upload}")

    with open(filename, encoding='utf8') as file:
      mdata = file.read().encode()
      res = requests.put(fr"{link_for_upload}", data=mdata)

    if res.status_code == 201:
      print(f"Файл {filename} успешно загружен на Яндекс Диск.")
  except FileNotFoundError:
    print(f"Файл {filename} не найден.")

def main():
  """

  (None) -> None

  Main function describe main functionality

  """
  filenemes = ("DE", "ES", "FR")

  # Translate files
  for filename in filenemes:
    translate_file(f"{filename}1.txt", f"{filename}_to_RU.txt", filename.lower())

  # Upload result files to Yandex Disk
  for filename in filenemes:
    upload_file_to_yandexdisk(f"{filename}_to_RU.txt")

main()
