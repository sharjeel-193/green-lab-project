
#convert_demo.py ln 62, taken from ...
def convert_prompt(prompt: str, retry_times: int = 3, type: str = "t2v", image_path: str = None):
    """
    Convert a prompt to a format that can be used by the model for inference
    """

    client = OpenAI()
    ## If you using with Azure OpenAI, please uncomment the below line and comment the above line
    # client = AzureOpenAI(
    #     api_key="",
    #     api_version="",
    #     azure_endpoint=""
    # )

    text = prompt.strip()
    for i in range(retry_times):
        if type == "t2v":
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"{sys_prompt_t2v}"},
                    {
                        "role": "user",
                        "content": 'Create an imaginative video descriptive caption or modify an earlier caption for the user input : " a girl is on the beach"',
                    },
                    {
                        "role": "assistant",
                        "content": "A radiant woman stands on a deserted beach, arms outstretched, wearing a beige trench coat, white blouse, light blue jeans, and chic boots, against a backdrop of soft sky and sea. Moments later, she is seen mid-twirl, arms exuberant, with the lighting suggesting dawn or dusk. Then, she runs along the beach, her attire complemented by an off-white scarf and black ankle boots, the tranquil sea behind her. Finally, she holds a paper airplane, her pose reflecting joy and freedom, with the ocean's gentle waves and the sky's soft pastel hues enhancing the serene ambiance.",
                    },
                    {
                        "role": "user",
                        "content": 'Create an imaginative video descriptive caption or modify an earlier caption for the user input : " A man jogging on a football field"',
                    },
                    {
                        "role": "assistant",
                        "content": "A determined man in athletic attire, including a blue long-sleeve shirt, black shorts, and blue socks, jogs around a snow-covered soccer field, showcasing his solitary exercise in a quiet, overcast setting. His long dreadlocks, focused expression, and the serene winter backdrop highlight his dedication to fitness. As he moves, his attire, consisting of a blue sports sweatshirt, black athletic pants, gloves, and sneakers, grips the snowy ground. He is seen running past a chain-link fence enclosing the playground area, with a basketball hoop and children's slide, suggesting a moment of solitary exercise amidst the empty field.",
                    },
                    {
                        "role": "user",
                        "content": 'Create an imaginative video descriptive caption or modify an earlier caption for the user input : " A woman is dancing, HD footage, close-up"',
                    },
                    {
                        "role": "assistant",
                        "content": "A young woman with her hair in an updo and wearing a teal hoodie stands against a light backdrop, initially looking over her shoulder with a contemplative expression. She then confidently makes a subtle dance move, suggesting rhythm and movement. Next, she appears poised and focused, looking directly at the camera. Her expression shifts to one of introspection as she gazes downward slightly. Finally, she dances with confidence, her left hand over her heart, symbolizing a poignant moment, all while dressed in the same teal hoodie against a plain, light-colored background.",
                    },
                    {
                        "role": "user",
                        "content": f'Create an imaginative video descriptive caption or modify an earlier caption in ENGLISH for the user input: " {text} "',
                    },
                ],
                model="glm-4-plus",  # glm-4-plus and gpt-4o have be tested
                temperature=0.01,
                top_p=0.7,
                stream=False,
                max_tokens=250,
            )
        else:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"{sys_prompt_i2v}"},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_to_url(image_path),
                                },
                            },
                        ],
                    },
                ],
                temperature=0.01,
                top_p=0.7,
                stream=False,
                max_tokens=250,
            )
        if response.choices:
            return response.choices[0].message.content
    return prompt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, required=True, help="Prompt to convert")
    parser.add_argument("--retry_times", type=int, default=3, help="Number of times to retry the conversion")
    parser.add_argument("--type", type=str, default="t2v", help="Type of conversion (t2v or i2v)")
    parser.add_argument("--image_path", type=str, default=None, help="Path to the image file")
    args = parser.parse_args()

    converted_prompt = convert_prompt(args.prompt, args.retry_times, args.type, args.image_path)
    print(converted_prompt)


def convert_prompt_unswitched(prompt: str, retry_times: int = 3, type: str = "t2v", image_path: str = None):
    """
    Convert a prompt to a format that can be used by the model for inference
    """

    client = OpenAI()
    ## If you using with Azure OpenAI, please uncomment the below line and comment the above line
    # client = AzureOpenAI(
    #     api_key="",
    #     api_version="",
    #     azure_endpoint=""
    # )

    text = prompt.strip()
    if type == "t2v":
        for i in range(retry_times):
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"{sys_prompt_t2v}"},
                    {
                        "role": "user",
                        "content": 'Create an imaginative video descriptive caption or modify an earlier caption for the user input : " a girl is on the beach"',
                    },
                    {
                        "role": "assistant",
                        "content": "A radiant woman stands on a deserted beach, arms outstretched, wearing a beige trench coat, white blouse, light blue jeans, and chic boots, against a backdrop of soft sky and sea. Moments later, she is seen mid-twirl, arms exuberant, with the lighting suggesting dawn or dusk. Then, she runs along the beach, her attire complemented by an off-white scarf and black ankle boots, the tranquil sea behind her. Finally, she holds a paper airplane, her pose reflecting joy and freedom, with the ocean's gentle waves and the sky's soft pastel hues enhancing the serene ambiance.",
                    },
                    {
                        "role": "user",
                        "content": 'Create an imaginative video descriptive caption or modify an earlier caption for the user input : " A man jogging on a football field"',
                    },
                    {
                        "role": "assistant",
                        "content": "A determined man in athletic attire, including a blue long-sleeve shirt, black shorts, and blue socks, jogs around a snow-covered soccer field, showcasing his solitary exercise in a quiet, overcast setting. His long dreadlocks, focused expression, and the serene winter backdrop highlight his dedication to fitness. As he moves, his attire, consisting of a blue sports sweatshirt, black athletic pants, gloves, and sneakers, grips the snowy ground. He is seen running past a chain-link fence enclosing the playground area, with a basketball hoop and children's slide, suggesting a moment of solitary exercise amidst the empty field.",
                    },
                    {
                        "role": "user",
                        "content": 'Create an imaginative video descriptive caption or modify an earlier caption for the user input : " A woman is dancing, HD footage, close-up"',
                    },
                    {
                        "role": "assistant",
                        "content": "A young woman with her hair in an updo and wearing a teal hoodie stands against a light backdrop, initially looking over her shoulder with a contemplative expression. She then confidently makes a subtle dance move, suggesting rhythm and movement. Next, she appears poised and focused, looking directly at the camera. Her expression shifts to one of introspection as she gazes downward slightly. Finally, she dances with confidence, her left hand over her heart, symbolizing a poignant moment, all while dressed in the same teal hoodie against a plain, light-colored background.",
                    },
                    {
                        "role": "user",
                        "content": f'Create an imaginative video descriptive caption or modify an earlier caption in ENGLISH for the user input: " {text} "',
                    },
                ],
                model="glm-4-plus",  # glm-4-plus and gpt-4o have be tested
                temperature=0.01,
                top_p=0.7,
                stream=False,
                max_tokens=250,
            )
        if response.choices:
            return response.choices[0].message.content

    else:
        for i in range(retry_times):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"{sys_prompt_i2v}"},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_to_url(image_path),
                                },
                            },
                        ],
                    },
                ],
                temperature=0.01,
                top_p=0.7,
                stream=False,
                max_tokens=250,
            )
        if response.choices:
            return response.choices[0].message.content
    return prompt

