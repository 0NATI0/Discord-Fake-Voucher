import requests
import re

def buildnum():
        res = requests.get("https://discord.com/login").text
        file_with_build_num = 'https://discord.com/assets/' + re.compile(r'assets/+([a-z0-9]+)\.js').findall(res)[-2]+'.js'
        req_file_build = requests.get(file_with_build_num).text
        index_of_build_num = req_file_build.find('buildNumber')+24
        return int(req_file_build[index_of_build_num:index_of_build_num+6])