import os
import random
import glob
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simple in-memory storage
image_votes_count = defaultdict(lambda: defaultdict(dict))
image_votes = {
    "1":0,
    "2":0
}
@app.route('/', methods=['GET', 'POST'])
def index():
    global image_votes
    if request.method == 'POST':
        selected_image = request.form.get('image_choice')
        selected_input = request.form.get('selected_input')
        if not selected_image:
            return redirect(url_for('index'))
        count = image_votes_count[selected_input].get(selected_image, 0)
        image_votes_count[selected_input][selected_image] = count+1
        image_votes[selected_image] += 1
        return redirect(url_for('index'))

    # Calculate the score (percentage of votes for each image)
    total_votes = sum(image_votes.values())
    if total_votes > 0:
        image_1_score = (image_votes['1'] / total_votes) * 100
        image_2_score = (image_votes['2'] / total_votes) * 100
    else:
        image_1_score = image_2_score = 0

    # Assuming the filename is 'image.jpg' and folders are 'input_images' and 'generated_images'
    path = 'input_images'
    selected_input = get_random_input_image(path)
    print(selected_input)
    prompt_file = selected_input.split(".")[0] + ".txt"
    prompt_path = os.path.join('static', 'input_prompt', prompt_file)
    file = open(prompt_path, 'r')
    prompt_input = file.readlines()
    input_image_url = f"input_images/{selected_input}"
    generated_image_1_url = f"generated_images_1/{selected_input}"
    generated_image_2_url = f"generated_images_2/{selected_input}"
    generated_prompt_url = f"input_prompt/{prompt_input}"
    return render_template('index.html', 
                            selected_input=selected_input,
                            input_image_url=input_image_url, 
                            generated_image_1_url=generated_image_1_url,
                            generated_image_2_url=generated_image_2_url,
                            text =prompt_input,
                            image_1_score=image_1_score,
                            image_2_score=image_2_score)

def get_random_input_image(path):
    # Logic to randomly select an input image.
    path = os.path.join('static',path, "*")
    # print(path)
    names = [os.path.basename(x) for x in glob.glob(path)]
    # print(names)
    return random.choice(names)

def get_random_generated_images():
    # Logic to randomly select two generated images.
    pass

def get_associated_text_prompt(image):
    # Logic to get the text prompt associated with the provided image.
    pass

@app.route('/results')
def results():
    total_votes = sum(image_votes.values())
    if total_votes > 0:
        image_1_score = (image_votes['1'] / total_votes) * 100
        image_2_score = (image_votes['2'] / total_votes) * 100
    else:
        image_1_score = image_2_score = 0
    
    return render_template('results.html', 
                           image_1_score=image_1_score, 
                           image_2_score=image_2_score,
                           image_votes_count=image_votes_count)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
