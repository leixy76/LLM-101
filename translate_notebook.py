#!/usr/bin/env python3
import json
import re

# 读取notebook文件
with open('chapter02-llm-prompt/openai_prompt_jupyter/03_Assigning_Roles_Role_Prompting.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# 英文到中文的翻译映射
translations = {
    'PROMPT = "Jack is looking at Anne. Anne is looking at George. Jack is married, George is not, and we don\'t know if Anne is married. Is a married person looking at an unmarried person?"': 'PROMPT = "杰克正在看安妮。安妮正在看乔治。杰克已婚，乔治未婚，我们不知道安妮是否已婚。已婚的人是否在看着未婚的人？"'
}

# 遍历所有cells进行替换
count = 0
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        for i, line in enumerate(cell['source']):
            for en_text, cn_text in translations.items():
                if en_text in line:
                    cell['source'][i] = line.replace(en_text, cn_text)
                    count += 1
                    print(f"替换了第 {count} 个: {en_text[:50]}...")

# 保存文件
with open('chapter02-llm-prompt/openai_prompt_jupyter/03_Assigning_Roles_Role_Prompting.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f'翻译完成！总共替换了 {count} 个文本。') 