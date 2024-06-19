import pdf2image
import pandas as pd
import re
import sys
import pyocr
import pyocr.builders
from PIL import Image, ImageEnhance, ImageFilter

file_path = r"C:\Users\masat\Documents\sumplepdf222.pdf"

gray_pdf = []

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))

all_text = []

#pdfを画像に変換
images = pdf2image.convert_from_path(file_path, dpi=350, fmt='png')
lang = 'eng'
#lang = 'jpn'
#画像オブジェクトからテキストに変換
for image in images:
    # コントラストを強化
    enhancer = ImageEnhance.Contrast(image)
    enhanced_image = enhancer.enhance(2.0)  #コントラスト係数を調整

    #コントラスト強化された画像をグレースケールに変換
    gray_image = enhanced_image.convert("L")
    
    #グレースケール画像を二値化
    threshold = 128
    binary_image = gray_image.point(lambda x: 0 if x < threshold else 255, '1')
    gray_pdf.append(binary_image)

    #二値化された画像にOCRを適用
    txt = tool.image_to_string(
        binary_image,
        lang=lang,
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )
    all_text.append(txt)

full_text = "\n".join(all_text)
print(full_text)



ocr_list = []

# 正規表現パターンのコンパイル
pattern = re.compile(r"(AVE|STD|RMS)=?(-?\d+[.,]\d*(?:\/\d+)?)[a-zA-Z]*(?:\/[a-zA-Z]*)?m")

# テキストからの数値抽出
matches = pattern.findall(full_text)

# 結果の表示
for match in matches:
    print(f"{match[0]}: {match[1]}")
    try:
        value = float(match[1])
    except ValueError:
        value = float('nan')  
    ocr_list.append((match[0], value))
    

print(len(ocr_list))


result = check_len_list(ocr_list)

print(result)

data = {'AVE': [], 'STD': [], 'RMS': []}
for key, value in ocr_list:
    data[key].append(value)

df = pd.DataFrame(data)
df
