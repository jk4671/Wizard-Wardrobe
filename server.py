from flask import Flask, render_template, request, jsonify, redirect, url_for
import openai  # Assuming you've set up OpenAI API access
import openai_secrets  # For storing your OpenAI API key


app = Flask(__name__)

# Set up the OpenAI client
client = openai.OpenAI(api_key=openai_secrets.SECRET_KEY)


# Metadata structure
meta_data = {
    "gender": "",
    "age": 0,
    "outfit_type": "",
    "occasion": "",
    "core": "",
    "outfit_choices": {
        "top": [],
        "bottom": [],
        "accessory": [],
    },
    "outfit_selected": {
        "top": [],
        "bottom": [],
        "accessory": [],
    },
    "generation": None
}

fashion_cores = {
    "Cottagecore": {
        "Aesthetic": "Romanticizing rural life and simplicity.",
        "Elements": "Flowy dresses, floral prints, lace, straw hats, soft cardigans, and aprons.",
        "Colors": "Pastels, earthy tones, whites, and florals.",
        "Image": "/static/images/cottagecore.webp"
    },
    "Dark Academia": {
        "Aesthetic": "Scholarly, mysterious, and vintage.",
        "Elements": "Tweed blazers, turtlenecks, plaid skirts, Oxford shoes, button-up shirts, and trench coats.",
        "Colors": "Browns, dark greens, blacks, and grays.",
        "Image": "/static/images/darkAcademia.webp"
    },
    "Light Academia": {
        "Aesthetic": "Softer, more optimistic counterpart of dark academia.",
        "Elements": "Lightweight fabrics, cozy knits, pleated skirts, cardigans, and loafers.",
        "Colors": "Creams, beiges, light browns, and soft pastels.",
        "Image": "/static/images/lightAcademia.webp"
    },
    "Fairycore": {
        "Aesthetic": "Enchanting and ethereal, inspired by nature and fairytales.",
        "Elements": "Sheer fabrics, ruffles, floral headpieces, lace-up boots, and wings as accessories.",
        "Colors": "Soft greens, lilacs, whites, and floral pastels.",
        "Image": "/static/images/fairycore.webp"
    },
    "Y2K": {
        "Aesthetic": "Early 2000s nostalgia with a futuristic twist.",
        "Elements": "Low-rise jeans, baby tees, crop tops, metallics, chunky sneakers, and mini handbags.",
        "Colors": "Neon, metallics, pinks, and bright blues.",
        "Image": "/static/images/y2k.webp"
    },
    "Goblincore": {
        "Aesthetic": "Embraces the chaotic, messy, and earthy elements of nature.",
        "Elements": "Overalls, utility vests, mushroom motifs, earthy textures, and unpolished jewelry.",
        "Colors": "Earthy greens, browns, and rusts.",
        "Image": "/static/images/goblincore.webp"
    },
    "Grungecore": {
        "Aesthetic": "Inspired by 90s grunge music and fashion.",
        "Elements": "Flannel shirts, ripped jeans, band tees, combat boots, and oversized sweaters.",
        "Colors": "Black, gray, red, and muted earth tones.",
        "Image": "/static/images/grungecore.webp"
    },
    "Normcore": {
        "Aesthetic": "Focuses on simple, functional, and minimalistic clothing.",
        "Elements": "Plain jeans, white tees, sneakers, neutral jackets, and minimal accessories.",
        "Colors": "Neutral shades like white, black, gray, and beige.",
        "Image": "/static/images/normcore.webp"
    },
    "Kidcore": {
        "Aesthetic": "Nostalgic, playful, and childlike.",
        "Elements": "Bright colors, cartoon motifs, oversized tees, jelly shoes, and playful accessories.",
        "Colors": "Primary colors and bright, playful hues.",
        "Image": "/static/images/kidcore.webp"
    },
    "Angelcore": {
        "Aesthetic": "Soft, dreamy, and ethereal.",
        "Elements": "White dresses, lace, sheer fabrics, angel wings, and halos as accessories.",
        "Colors": "White, silver, pale blue, and pastels.",
        "Image": "/static/images/angelcore.webp"
    },
    "Cybercore": {
        "Aesthetic": "Futuristic, cyberpunk-inspired fashion.",
        "Elements": "Metallic fabrics, neon accents, futuristic sunglasses, cargo pants, and tech accessories.",
        "Colors": "Neon greens, blacks, silvers, and purples.",
        "Image": "/static/images/cybercore.webp"
    },
    "Royalcore": {
        "Aesthetic": "Regal, luxurious, and inspired by historical royalty.",
        "Elements": "Corsets, ball gowns, tiaras, lace gloves, and pearl jewelry.",
        "Colors": "Deep reds, golds, blues, and rich purples.",
        "Image": "/static/images/royalcore.webp"
    },
    "Egirl/Eboy Core": {
        "Aesthetic": "Edgy, internet-influenced, and youth-oriented.",
        "Elements": "Plaid skirts, oversized hoodies, striped long-sleeve shirts, chains, and chunky boots.",
        "Colors": "Black, neon green, red, and dark tones.",
        "Image": "/static/images/egirBoycore.webp"
    }
}



@app.route('/submit_occasion', methods=['POST'])
def submit_occasion():
    global meta_data
    data = request.get_json()

    occasion = data.get("occasion")
    if occasion:
        meta_data["occasion"] = occasion
        print(f"Occasion received: {occasion}")

    return jsonify(meta_data)

@app.route('/submit_details', methods=['POST'])
def submit_details():
    global meta_data  # Declare global meta_data before using it
    data = request.get_json()

    gender = data.get("gender")
    age = data.get("age")
    outfit_type = data.get("outfit_type")

    if gender and age and outfit_type:
        meta_data["gender"] = gender
        meta_data["age"] = int(age)
        meta_data["outfit_type"] = outfit_type
        print(f"Gender: {gender}, Age: {age}, Outfit Type: {outfit_type}")

    return jsonify(meta_data)

@app.route('/')
@app.route('/')
def home():
    # Check if the route is accessed with 'clear' query parameter
    if request.args.get('clear') == 'true':
        global meta_data
        meta_data = {
            "gender": "",
            "age": 0,
            "outfit_type": "",
            "occasion": "",
            "core": "",
            "outfit_choices": {
                "top": [],
                "bottom": [],
                "accessory": [],
            },
            "outfit_selected": {
                "top": [],
                "bottom": [],
                "accessory": [],
            },
            "generation": None
        }
    return render_template('home.html', data=meta_data, fashion_cores=fashion_cores)

@app.route('/edit_details')
def edit_details():
    return render_template('home.html', data=meta_data, fashion_cores=fashion_cores)


@app.route('/select_core', methods=['POST'])
def select_core():
    global meta_data
    data = request.get_json()

    selected_core = data.get("core")
    if selected_core:
        meta_data["core"] = selected_core
        print(f"Selected Fashion Core: {selected_core}")

    return jsonify({"redirect": url_for('summary')})

@app.route('/summary')
def summary():
    return render_template('summary.html', data=meta_data, fashion_cores=fashion_cores)

@app.route('/generate_outfits', methods=['POST'])
def generate_outfits():
    print("Request received at /generate_outfits")
    global meta_data

    # Generate keywords based on user data
    keywords = get_keywords_for_headline(
        meta_data["age"], 
        meta_data["gender"], 
        meta_data["outfit_type"], 
        meta_data["occasion"], 
        meta_data["core"]
    )

    # Validate and replace outfit choices
    validated_keywords = validate_and_replace_outfit_choices(
        keywords, 
        meta_data['age'], 
        meta_data['gender'], 
        meta_data['outfit_type'], 
        meta_data['occasion'], 
        meta_data['core'], 
        api_call_limit=5
    )

    # Update meta_data with validated outfit choices
    meta_data["outfit_choices"] = validated_keywords
    print(validated_keywords)

    # Return the validated outfit choices as a JSON response
    return jsonify(validated_keywords)

@app.route('/submit_outfit_selection', methods=['POST'])
def submit_outfit_selection():
    global meta_data
    data = request.get_json()

    # Extract the selected items from the request
    selected_top = data.get("top")
    selected_bottom = data.get("bottom")
    selected_accessory = data.get("accessory")

    # Update meta_data with the selected outfit components
    if selected_top and selected_bottom and selected_accessory:
        meta_data["outfit_selected"]["top"] = [selected_top]
        meta_data["outfit_selected"]["bottom"] = [selected_bottom]
        meta_data["outfit_selected"]["accessory"] = [selected_accessory]
        print("Outfit selection updated:", meta_data["outfit_selected"])

        # Generate the image based on the selected outfit
        prompt = create_image_prompt(
            meta_data["outfit_selected"],
            meta_data["gender"],
            meta_data["age"],
            meta_data["occasion"],
            meta_data["outfit_type"],
            meta_data["core"]
        )

        image_url = generate_and_validate_image(prompt, meta_data)
        if image_url:
            meta_data["generation"] = image_url
            return jsonify({"image_url": image_url})
        else:
            return jsonify({"error": "Failed to generate a valid image."}), 500
    else:
        return jsonify({"error": "Incomplete selection"}), 400


@app.route('/generate_image', methods=['POST'])
def generate_image():
    global meta_data
    print("Generating image...")

    # Create the prompt based on the selected outfit
    prompt = create_image_prompt(
        meta_data["outfit_selected"],
        meta_data["gender"],
        meta_data["age"],
        meta_data["occasion"],
        meta_data["outfit_type"],
        meta_data["core"]
    )
    print(f"Image generation prompt: {prompt}")

    # Generate and validate the image
    try:
        image_url = generate_and_validate_image(prompt, meta_data)
        if image_url:
            meta_data["generation"] = image_url
            print(f"Image successfully generated: {image_url}")
            return jsonify({"redirect": url_for('show_image')})
        else:
            print("Failed to generate a valid image.")
            return jsonify({"error": "Failed to generate a valid image. Please try again."}), 500
    except Exception as e:
        print(f"Error during image generation: {e}")
        return jsonify({"error": "An error occurred during image generation. Please try again later."}), 500

def get_keywords_for_headline(age, gender, outfit_type, occasion, core):
    prompt = f"""I am a {age}-year-old {gender} looking for {outfit_type} outfits. I want to dress for {occasion}. Here's the fashion core I like to wear: {core}.

                Please give me inspiration for various pieces categorized as "Top", "Bottom", and "Accessory". Ensure that:
                - Only include items typically worn on the upper body for "Top" (e.g., shirts, jackets).
                - Only include items typically worn on the lower body for "Bottom" (e.g., pants, skirts).
                - Accessories should include items like watches and scarves.

                Format the response like this:

                Top:
                1. keyword1
                2. keyword2
                3. keyword3

                Bottom:
                4. keyword4
                5. keyword5
                6. keyword6

                Accessory:
                7. keyword7
                8. keyword8
                9. keyword9
                """

    response_raw = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )

    response = response_raw.choices[0].message.content

    # Parse the response into a keyword dictionary
    return parse_keywords_from_gpt_response(response)

def parse_keywords_from_gpt_response(keyword_response):
    keyword_dict = {"top": [], "bottom": [], "accessory": []}
    lines = keyword_response.strip().split('\n')
    current_category = None

    for line in lines:
        line = line.strip()
        if line.lower().startswith("top:"):
            current_category = "top"
        elif line.lower().startswith("bottom:"):
            current_category = "bottom"
        elif line.lower().startswith("accessory:"):
            current_category = "accessory"
        elif line and current_category:
            keyword = line.split('.', 1)[-1].strip()
            keyword_dict[current_category].append(keyword)

    return keyword_dict

def validate_and_replace_outfit_choices(outfit_choices, age, gender, outfit_type, occasion, core, api_call_limit=10):
    api_call_count = 0

    def verify_item_category(item, category):
        nonlocal api_call_count
        if api_call_count >= api_call_limit:
            return False

        prompt = f"""The item "{item}" is categorized as "{core}" fashion core suitable for the occasion of "{occasion}". Is this correct?
                    - "Top" items include shirts, jackets, hoodies.
                    - "Bottom" items include pants, shorts, joggers.
                    - "Accessory" items include scarves, gloves, watches.

                    Respond with "Yes" if it fits the category, or "No" if it does not."""

        response_raw = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10
        )

        api_call_count += 1
        return response_raw.choices[0].message.content.strip().lower() == "yes"

    def generate_new_item(category, age, gender, outfit_type, occasion, core):
        nonlocal api_call_count
        if api_call_count >= api_call_limit:
            return None

        prompt = f"""I need a replacement item for the "{category}" category.
                    I am a {age}-year-old {gender} looking for {outfit_type} outfits for {occasion}.
                    Here's the fashion core I like to wear: {core}.

                    Please suggest one new item with this fashion core {core} for the "{category}" category.
                    Only respond with the format:
                    item_name"""

        response_raw = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20
        )

        api_call_count += 1
        new_item = response_raw.choices[0].message.content.strip()

        if not new_item:
            return generate_new_item(category, age, gender, outfit_type, occasion, core)

        return new_item

    categories = ["top", "bottom", "accessory"]
    for category in categories:
        for i, item in enumerate(outfit_choices[category]):
            if api_call_count >= api_call_limit:
                return outfit_choices

            if not item or not verify_item_category(item, category):
                new_item = generate_new_item(category, age, gender, outfit_type, occasion, core)
                if new_item:
                    outfit_choices[category][i] = new_item

    return outfit_choices

def create_image_prompt(outfit_selected, gender, age, occasion, outfit_type, core):
    if not outfit_selected["top"] and not outfit_selected["bottom"]:
        return f"A {gender} mannequin standing in a neutral background, realistic style"

    top_keywords = ", ".join(outfit_selected["top"])
    bottom_keywords = ", ".join(outfit_selected["bottom"])
    accessory_keywords = ", ".join(outfit_selected["accessory"]) if outfit_selected["accessory"] else ""

    prompt = f"""Generate a high-quality, single, full-body fashion photo of a {age}-year-old {gender}, styled for {occasion} in {outfit_type} clothing with {core} fashion core.
            This image must include:
            - Top: {top_keywords}
            - Bottom: {bottom_keywords}
            - Accessories: {accessory_keywords}
            
            Ensure the following:
            - Only one person in the image. No additional people or models should be present.
            - Full-body, head-to-toe shot, including the feet clearly in the frame.
            - Model should be standing straight, centered in the frame, and fully visible.
            - Use a neutral background with no distractions.
            - No text or descriptions should appear in the image.
            
            Make the outfit and person stand out like a fashion catalog or Pinterest-style inspiration photo, with the full body, including the feet, visible.
            """

    return prompt

def validate_image_with_prompt(prompt, image_url, meta_data, api_call_limit=10):
    api_call_count = 0
    outfit_selected = meta_data["outfit_selected"]
    top_keywords = ", ".join(outfit_selected["top"])
    bottom_keywords = ", ".join(outfit_selected["bottom"])
    accessory_keywords = ", ".join(outfit_selected["accessory"]) if outfit_selected["accessory"] else ""
    gender = meta_data["gender"]
    age = meta_data["age"]
    occasion = meta_data["occasion"]
    outfit_type = meta_data["outfit_type"]
    core = meta_data["core"]

    validation_prompt = f""" The following image was generated using this prompt:

        "{prompt}"

        Image URL: {image_url}

        Does this image include the following details from the meta_data:
        - Top: {top_keywords}
        - Bottom: {bottom_keywords}
        - Accessories: {accessory_keywords}
        - Styled for a {age}-year-old {gender} for the {occasion} in {outfit_type} clothing with {core} fashion core.

        Respond with "Yes" if the image fits all of these criteria, and "No" if it does not.
    """

    def call_validation_api(validation_prompt):
        nonlocal api_call_count
        if api_call_count >= api_call_limit:
            return None

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": validation_prompt}],
                max_tokens=50
            )
            api_call_count += 1
            response_content = response.choices[0].message.content.strip().lower()
            print(f"Validation API response: {response_content}")
            return response_content == "yes"
        except Exception as e:
            print(f"Error during validation API call: {e}")
            return False

    response_content = call_validation_api(validation_prompt)
    return response_content

def generate_images(prompt):
    try:
        response_image = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        print(f"API response: {response_image}")
        if not response_image or not response_image.data:
            print("No data received from API.")
            return []

        url = response_image.data[0].url
        return [{"prompt": prompt, "url": url}]
    except Exception as e:
        print(f"Error in generate_images: {e}")
        return []

def generate_and_validate_image(prompt, meta_data, max_attempts=3):
    attempts = 0
    valid_image = False
    image_url = None

    while not valid_image and attempts < max_attempts:
        try:
            print(f"Attempt {attempts + 1}: Generating image...")
            images = generate_images(prompt)
            
            # Log the response
            if not images:
                print("No images returned by the API.")
                break

            image_url = images[0].get('url')
            if not image_url:
                print("Image URL not found in the response.")
                break

            print(f"Generated Image URL: {image_url}")

            # Validate the generated image
            valid_image = validate_image_with_prompt(prompt, image_url, meta_data)
            print(f"Validation Result: {'Valid' if valid_image else 'Invalid'}")

            if valid_image:
                print(f"Valid image found: {image_url}")
            else:
                print("Image does not match the prompt. Trying again...")

        except Exception as e:
            print(f"Error during image generation attempt {attempts + 1}: {e}")

        attempts += 1

    return image_url if valid_image else None


if __name__ == '__main__':
    app.run(debug=True)