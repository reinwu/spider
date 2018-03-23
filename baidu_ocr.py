#coding:UTF-8

from aip import AipOcr
import json
import os
import filetype

#定义 Baidu OCR 常量 
APP_ID = '10711685'
API_KEY = 'G9hXCS1MrxTadpPGuQHCvNtz'
SECRET_KEY = 'RP06XYIzokPwv7Ye2KMX6CQeGX37Iksg'

#初始化AipFace对象
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 定义参数变量  
options = {  
    'detect_direction': 'true',  
    'language_type': 'CHN_ENG',  
}  

#读取图片目录所有文件
image_directory = "./image"

#输出到同一目录下txt文件
out_file = image_directory + "/ocr_out.txt"

def get_file_content(filePath):  
    with open(filePath, 'rb') as fp:  
        return fp.read()  

fout = open(out_file, "w")

file_list = os.listdir(image_directory)
for i in range(0, len(file_list)):
    file_path = os.path.join(image_directory, file_list[i])
    file_kinds = filetype.guess(file_path)
    if file_kinds:
        file_type = file_kinds.extension
        if file_type in ['jpg', 'png', 'gif', 'bmp']:
            # 调用通用文字识别接口
            result = aipOcr.basicGeneral(get_file_content(file_path), options)

            words_result = result['words_result']

            for words in words_result:
                print(words['words'])
                fout.writelines(words['words'])
        else:
            print("[warning]【图像文件类型暂不支持】" + file_type)
    else:
        print("[warning]【文件类型无法识别】" + file_path)
print("\n文字识别运行结束！")
fout.close()