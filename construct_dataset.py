# {"messages": [{"role": "system", "content": "You are roleplaying as a person named Eric Xue on an online chat app, whose online alias is Yumoo. He is a 21 years old male student studying Computer Science at the University of Toronto. He likes watching anime and playing games. He is fluently in both Chinese and English and can choose which to speak based on who he is talking to."}, {"role": "user", "content": "when tho?\nand where"}, {"role": "assistant", "content": "about 6-9 tmr\nmy friend's building's common room\nnear my place"}]}

# Load jsonl from template.jsonl

import json
import random
import argparse
import os

def main():
    # Process args and do preliminary checks
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_samples', type=int, default=50, help='Number of samples to include in the dataset')
    args = parser.parse_args()
    num_samples = args.num_samples

    if os.path.exists('dataset.jsonl'):
        confirm = input("It seems like you have already created a dataset, are you sure you want to overwrite it? Press Enter to continue...")
        if confirm != '':
            return
        os.remove('dataset.jsonl')
    
    # Load the prompts from template.jsonl
    name = input("Pleae enter your first name: ")
    system_msg = f'You are roleplaying as a person named {name} on an online chat app. You must respond as if you are this person and never break character.'
    
    with open('template.jsonl', 'r') as f:
        prompts = [json.loads(line) for line in f]
    random.shuffle(prompts)
    
    # Collect user response to prompts
    for i in range(min(num_samples, len(prompts))):
        prompt = prompts[i]['message']
        response = input(prompt + ' ')

        with open('dataset.jsonl', 'a') as f:
            data = {
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": response}
                ]
            }
            f.write(json.dumps(data) + '\n')
        
if __name__ == '__main__':
    main()