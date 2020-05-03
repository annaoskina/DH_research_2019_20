import re
import MeCab
import csv
import os
import matplotlib.pyplot as plt
from pymecab.pymecab import PyMecab

def open_file(path, filename):
      with open('/home/anna/DH_research_2019-20/Source_for_research/{}'.format(filename), 'r', encoding = 'Shift-JIS') as f:
            print('\n', filename)
            raw_file = f.read()
      return raw_file

def clean_the_text(raw_file):
      step_1 = re.sub('(----------).+(---------)', '', raw_file, flags=re.DOTALL)
      step_2 = re.sub('［＃.+?］', '', step_1)
      clean_txt = re.sub('(底本：「).+?(ボランティアの皆さんです。)', '', step_2, flags=re.DOTALL)
      return clean_txt

def parse_with_kindai(clean_txt):
      m = MeCab.Tagger('-d /home/anna/Documents/UniDic-kindai_1603')
      parsed_txt = m.parse(clean_txt)
      parsed_txt = parsed_txt.replace(',', '\t')
      parsed_by_words = parsed_txt.split('\n')
      return parsed_txt #один список разобранных слов

def parse_with_ipadic(clean_txt):
      mecab = PyMecab()
      tokenized_txt = []
      for token in mecab.tokenize(clean_txt):
            tokenized_txt.append(token)
      return tokenized_txt

def count_katakana(parsed_txt1):
      parsed_txt1 = parsed_txt1.split('\n')
      katakana_counter = 0
      katakana_list = []
      katakana_array = []
      lines_counter = 0
      for i, token in enumerate(parsed_txt1):
            lines_counter += 1
            if i < len(parsed_txt1):
                  token = token.split('\t')
                  if len(token) > 12:
                        if '外' in token[12]:
                              if 12450 <= ord(token[0][0]) <= 12538: #включаю катакану
                                    if i:
                                          if parsed_txt1[i-1][0] == '《':
                                                continue
                                          else:
                                                katakana_counter += 1
                                                katakana_list.append(token[0])
                                    else:
                                          katakana_counter += 1
                                          katakana_list.append(token[0])
                        elif '固' in token[12]:
                              if 12450 <= ord(token[0][0]) <= 12538: #включаю катакану
                                    if i:
                                          if parsed_txt1[i-1][0] == '《':
                                                continue
                                          else:
                                                katakana_counter += 1
                                                katakana_list.append(token[0])
                                    else:
                                          katakana_counter += 1
                                          katakana_list.append(token[0])
                  if 1 < len(token) <= 7: #здесь попадается мусор, и я не знаю, как от него избавиться
                        if 12450 <= ord(token[0][0]) <= 12538:
                              katakana_counter += 1
                              katakana_list.append(token[0])
                  if (lines_counter % 5000 == 0):
                        katakana_array.append(katakana_counter)
                        katakana_counter = 0
      katakana_array.append(katakana_counter)
      #print(katakana_list)
      print(len(katakana_list))
      print(katakana_array)
      return katakana_array

def count_romaji(parsed_txt2):
      romaji_counter = 0
      romaji_list = []
      romaji_array = []
      lines_counter = 0
      for token in parsed_txt2:
            lines_counter += 1
            if token[0]:
                  if 65 <= ord(token[0][0]) <= 122: #включаю латиницу half-width (H)
                        romaji_counter += 1
                        romaji_list.append(token[0])
                  if 65313 <= ord(token[0][0]) <= 65338: #включаю латиницу full-width (Ｈ)
                        romaji_counter += 1
                        romaji_list.append(token[0])
                  if(lines_counter % 5000 == 0):
                        romaji_array.append(romaji_counter)
                        romaji_counter = 0
      romaji_array.append(romaji_counter)
      print(romaji_list)
      print(len(romaji_list))
      #print(romaji_array)
      return romaji_array

def count_kanji(parsed_txt1):
      stop_words = ['恨', '己ら', '幇', '疊', '汗', '八', '主思', '打', '峰', '粥', '負', '志', '丘']
      sanskrit_words = ['陀羅尼', '舎利', '仏陀', '波羅葦僧', '波羅密', '迦陵頻伽', '修羅', '奈落', '涅槃', '世尊', '維摩', '琉璃', '南無', '弥陀', '比丘尼', '卒都婆', '卒堵婆', '阿弥', '玻璃', '菩薩', '良人', '檀那', '旦', '旦那', '于蘭盆', '盂蘭盆', '羅漢', '陀羅', '伽藍', '刹那', '沙弥', '沙門', '痘痕', '天麩羅', '天ぷら', '三昧', '伽羅', '般若', '卒塔婆', '袈裟', '塔婆', '娑婆', '達磨', '夜叉', '菩提', '婆羅門']
      chinese_words = ['摩訶', '損徳', '拉麺', '鴛鴦', '善知鳥', '山神', '姉夫']
      korean_words = ['両班']
      parsed_txt1 = parsed_txt1.split('\n')
      kanji_counter = 0
      kanji_list = []
      kanji_array = []
      lines_counter = 0
      for i, token in enumerate(parsed_txt1):
            lines_counter += 1
            if i < len(parsed_txt1):
                  token = token.split('\t') #token - это список (слово + разбор)
                  if len(token) > 12:
                        if '外' in token[12]:
                              if not 65 <= ord(token[0][0]) <= 122 \
                                 and not 65313 <= ord(token[0][0]) <= 65338 \
                                 and not 12450 <= ord(token[0][0]) <= 12538 \
                                 and not 12352 <= ord(token[0][0]) <= 12447 \
                                 and not 65296 <= ord(token[0][0]) <= 65305 \
                                 and not 48 <= ord(token[0][0]) <= 57 \
                                 and token[0] not in stop_words \
                                 and token[0] not in sanskrit_words \
                                 and token[0] not in chinese_words \
                                 and token[0] not in korean_words:
                                    kanji_counter += 1
                                    kanji_list.append(token[0])
                                    #print(token[0], token[12])
                  if token[0] == '《':
                        new_token = parsed_txt1[i+1].split('\t')
                        furigana = new_token[0]
                        if 12450 <= ord(furigana[0]) <= 12538: #если первый символ - это катакана
                              maybe_kanji_token = parsed_txt1[i-1].split('\t')
                              if len(maybe_kanji_token) > 12:
                                    if not 65 <= ord(maybe_kanji_token[0][0]) <= 122\
                                       and not 65313 <= ord(maybe_kanji_token[0][0]) <= 65338\
                                       and '外' not in maybe_kanji_token[12]:
                                          maybe_kanji_token = parsed_txt1[i-2].split('\t')
                                          if len(maybe_kanji_token) > 12:
                                                if '外' not in maybe_kanji_token[12]:
                                                      furigana = '*' + furigana
                                                      kanji_counter += 1
                                                      kanji_list.append(furigana)
                  if (lines_counter % 5000 == 0):
                        kanji_array.append(kanji_counter)
                        kanji_counter = 0
      kanji_array.append(kanji_counter)
      #print(kanji_list)
      #print(len(kanji_list))
      #print(kanji_array)
      return kanji_array

def write_result_tsv (filename, parsed_txt):
      with open('/home/anna/DH_research_2019-20/Files_tsv_kindai/{}.tsv'.format(filename), 'w', encoding = 'utf-8') as fw:
            fw.write("{}".format(parsed_txt))

def visualization(result, filename):
      plt.plot(result[0], 'g', label='katakana', linewidth=3)
      #print('result[0] = ', result[0])
      plt.plot(result[1], 'b', label='kanji', linewidth=3)
      #print('result[1] = ', result[1])
      plt.plot(result[2], 'red', label='romaji', linewidth=3)
      #print('result[2] = ', result[2])
      plt.title(filename)
      plt.savefig('/home/anna/DH_research_2019-20/Results_plot/{}.png'.format(filename))
      #plt.show()

def main():
      path = '/home/anna/DH_research_2019-20/Source_for_research'
      files = os.listdir(path)
      for filename in files:
            if not filename.endswith('.txt'):
                  continue
            raw_file = open_file(path, filename)
            clean_txt = clean_the_text(raw_file)
            parsed_txt1 = parse_with_kindai(clean_txt)
            parsed_txt2 = parse_with_ipadic(clean_txt)
            #write_result_tsv(filename, parsed_txt)
            count_katakana(parsed_txt1)
            count_romaji(parsed_txt2)
            count_kanji(parsed_txt1)
            
if __name__ == '__main__':
      main()
