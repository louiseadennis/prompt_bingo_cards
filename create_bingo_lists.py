import sys
import re
from random import choice

filename = sys.argv[1]
challenge_name = sys.argv[2]

file_ext = ".txt"
filedir = "prompt_lists/"

upper_list_size_limit = 20

group_exclusions_keys = ['fandom', 'fiction', 'graphics', 'art', 'craft']
group_exclusions = {key: [] for key in group_exclusions_keys}

list_names = {}
lists = {}
list_num = 1

with open(filename, 'r') as file:
    for subfile_name in file:
        subfile = filedir + subfile_name.strip() + file_ext
        print("reading " + subfile)
        with open(subfile, 'r') as prompt_file:
            raw_list = [line.strip() for line in prompt_file]
            listname = raw_list.pop(0)
            print(listname)
            list_names[list_num] = listname
            list = []
            for raw_prompt in raw_list:
                print(raw_prompt)
                pattern = r'\d*\. (.*)'
                match = re.match(pattern, raw_prompt)
                try:
                    prompt = match.group(1)
                    if (match):
                        pattern_excl = '(.*)--- exc: (.*)'
                        match_excl = re.match(pattern_excl, prompt)
                        pattern_only = '(.*)--- only: (.*)'
                        match_only = re.match(pattern_only, prompt)
                        if (match_excl):
                            exclusion = match_excl.group(2)
                            match3 = re.match(challenge_name, exclusion)
                            if not match3:
                                list.append(match_excl.group(1))
                        elif (match_only):
                            only = match_only.group(2)
                            if (only == challenge_name):
                                list.append(match_only.group(1))
                        else:
                            list.append(prompt)
                except:
                    break
            print(list)
        
        while len(list) > upper_list_size_limit:
            list.remove(choice(list))
            
        lists[list_num] = list
        list_num = list_num + 1
                        
python_output = challenge_name + "python.txt"
post_output = challenge_name + "post.txt"

list_num = 1

for key in list_names.keys():
    list_name = list_names.get(key)
    with open(post_output, "a") as file:
        file.write(f'<b>{list_num}. {list_name}</b>\n')
    with open(python_output, "a") as file:
        file.write(f'list{list_num} = (')
        
    prompt_num = 1
    python_string = ""
    
    for prompt in lists.get(key):
        post_prompt = prompt
        type_pattern = '(.*)=== types: (.*)'
        type_match = re.match(type_pattern, prompt)
        if (type_match):
            prompt = type_match.group(1)
            post_prompt = f'{prompt} ('
            excs = type_match.group(2)
            for type in group_exclusions_keys:
                if re.match(excs, type):
                    group_exclusions.get(type).append('{list_num}.{prompt_num}')
                    post_prompt = f'{post_prompt} {type},'
            post_prompt = post_prompt[:-1]
            post_prompt = f'{post_prompt} )'
        
        with open(post_output, "a") as file:
            file.write(f'{prompt_num}. {post_prompt}\n')
        python_string = python_string + f'\"{prompt}\", "'
        prompt_num = prompt_num + 1
    
    python_string = python_string[:-2]
    with open(python_output, "a") as file:
        file.write(f'{python_string} );\n\n categories[{list_num}] = list{list_num}\n\n')
    with open(post_output, "a") as file:
        file.write("\n")
        
    list_num = list_num + 1
                
for type in group_exclusions_keys:
    type_filename = challenge_name + type + ".txt"
    with open(type_filename, "a") as file:
        for exclusion in group_exclusions.get(type):
            file.write(exclusion + "\n")
