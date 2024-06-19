import pdf2image
import pandas as pd
import re
import sys
import pyocr
import pyocr.builders
from PIL import Image, ImageEnhance, ImageFilter

#JP Singapore Thailand Hanoi Indonesia UP MJIIT 

inputfile = 

outputfile = inputfile + "gray"
file_path = r"" + inputfile + r".pdf"
output_pdf_path = r"" + outputfile + r".pdf"


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
images = pdf2image.convert_from_path(file_path, dpi=350, fmt='png' , first_page=3)
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


gray_pdf[0].save(output_pdf_path, save_all=True, append_images=gray_pdf[1:])  

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

#すべての数値でOCR出来たのか確認す
def check_len_list(lis):
    if len(lis) % 9 == 0:
        return "割り切れる"
    else:
        return "割り切れない"

result = check_len_list(ocr_list)

print(result)

data = {'AVE': [], 'STD': [], 'RMS': []}
for key, value in ocr_list:
    data[key].append(value)

df_all = pd.DataFrame(data)
df_all

df1 = df_all.iloc[0::3, :]
df11 = df1.rename(columns={'AVE': 'AVE1' , 'STD' : 'STD1' , 'RMS' : 'RMS1'})
df2 = df_all.iloc[1::3, :]
df22 = df2.rename(columns={'AVE': 'AVE2' , 'STD' : 'STD2' , 'RMS' : 'RMS2'})
df3 = df_all.iloc[2::3, :]
df33 = df3.rename(columns={'AVE': 'AVE3' , 'STD' : 'STD3' , 'RMS' : 'RMS3'})

# 行インデックスをリセット
df11_reset = df11.reset_index(drop=True)
df22_reset = df22.reset_index(drop=True)
df33_reset = df33.reset_index(drop=True)

# リセットしたインデックスでデータフレームを結合
result = pd.concat([df11_reset, df22_reset, df33_reset], axis = 1)

result = result[['AVE1', 'AVE2', 'AVE3', 'STD1' , 'STD2' , 'STD3' , 'RMS1' , 'RMS2' , 'RMS3']]
ave = (result['AVE1'] ** 2 + result['AVE2'] ** 2) ** 0.5

std = (result['STD1'] ** 2 + result['STD2'] ** 2) ** 0.5
rms = (result['RMS1'] ** 2 + result['RMS2'] ** 2) ** 0.5

result1 = pd.concat([result, ave], axis = 1)

print(result)

result.to_csv(r"" + inputfile + r".csv")