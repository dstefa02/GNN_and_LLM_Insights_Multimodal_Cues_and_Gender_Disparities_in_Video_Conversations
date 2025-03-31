import time
from openai import OpenAI
import csv
import pandas as pd

gender = 'male'
# gender = 'female'

mydf = pd.read_csv(gender + "_Pitches_v2.csv", encoding="raw_unicode_escape")
data_dicts: list = mydf.to_dict('records')

client = OpenAI(api_key='')

base_message = '''I will provide a text from a pitch and you will hide the following identifiers: the name of the entrepreneur/presenter, the name of the product and the name of the company? DO NOT HIDE ANYTHING ELSE.'''

for i in range(0, len(data_dicts)):
    messages = [{"role": "system", "content": base_message}]
    messages.append(
        {"role": "user", "content": f"\"{data_dicts[i]['text']}\""},
    )
    print(messages)
    # print(i)
    
    response  = client.chat.completions.create(
        # messages=messages, model="gpt-4", temperature=0.0,
        messages=messages, model="gpt-4-turbo", temperature=0.0,
    )

    reply = response.choices[0].message.content
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})

    with open(gender + '_Pitches_ommited_identifiers.csv', 'a', newline='') as output_file:
        output_file.write(data_dicts[i]['pitch_id'] + ',' + reply + '\n')

    #print('sleeps')
    print('='*50)
    #time.sleep(2)

print('done')
