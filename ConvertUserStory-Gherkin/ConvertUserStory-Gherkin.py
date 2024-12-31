from openai import OpenAI

client = OpenAI(
    base_url="https://api.novita.ai/v3/openai",
    # Get the Novita AI API Key by referring to: https://novita.ai/docs/get-started/quickstart.html#_2-manage-api-key.
    api_key="6e03f062-926f-4d3e-ac1a-c07729d5b947",
)

model = "meta-llama/llama-3.1-8b-instruct"
stream = False  # or False
max_tokens = 512

# User stories
user_stories = [
     "As a user, I want to be notified if I enter incomplete or incorrect information in the search form so that I can correct it",
    "As a user, I want to log in to my account so that I can access my profile and booking history.",
    "As a user, I want to cancel a booking if my plans change so that I can free up the reserved seats.",
    "As a user, I want to view train details such as departure time, arrival time, and class type so that I can make an informed decision.",
    "As a user, I want to verify my ticket after I have obtained it, so that I can confirm its validity and ensure it is ready for use."
]


chat_completion_res = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "write gherkin scenario for this user story: \n As a user, I want to select a train from the search results and proceed to book tickets so that I can confirm my travel.",
        }
    ],
    stream=stream,
    max_tokens=max_tokens,
)


def generate_gherkin_from_user_story(user_story):
    prompt = f"Convert the following user story into Gherkin scenario:\n\n{user_story}\n\nGherkin Scenario:"
    chat_completion_res = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        stream=stream,
        max_tokens=max_tokens,
    )

    return (chat_completion_res.choices[0].message.content)
    


# Call the function to convert user story to Gherkin
for story in user_stories:
    gherkin = generate_gherkin_from_user_story(story)
    if gherkin:
        print(f"Gherkin for the user story: {gherkin}\n")
    else:
        print("Failed to generate Gherkin for this user story.")
