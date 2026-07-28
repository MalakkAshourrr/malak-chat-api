from openai import OpenAI

client = OpenAI(
    api_key="api_gAAAAABqV53NXXTPzmZ-4KS",
    base_url="https://api-pilot-sandbox.aurai.solutions/v1"
)

response = client.chat.completions.create(
    model="Aurai-3.0",
    messages=[
        {
            "role": "user",
            "content": "Explain what Generative AI is in simple words."
        }
    ]
)

print(response.choices[0].message.content)
