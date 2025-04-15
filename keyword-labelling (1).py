import openai
import pandas as pd
import time

# Set up your OpenAI API key
openai.api_key = ''

# Load the Excel file
file_path = " "
df = pd.read_excel(file_path)


# Function to extract keywords using the chat model
def extract_keywords(abstract_text):
    if not abstract_text:  # Check if the abstract is empty
        return "NaN"
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "user", "content": f"Extract 5 or less, relevant keywords from this abstract, separated by semicolons: {abstract_text}"}
        ],
        max_tokens=20,
        temperature=0.5,
    )
    return response.choices[0].message['content'].strip()


# Process in batches to avoid rate limits
batch_size = 30  # Adjust batch size based on API rate limits
for i in range(0, len(df), batch_size):
    batch = df[i:i+batch_size]
    df.loc[i:i+batch_size-1, 'Keyword'] = batch['Abstract'].apply(extract_keywords)
    
    # Add a slight delay between batches if necessary
    time.sleep(1)

# Save the updated DataFrame back to the Excel file
df.to_excel(file_path, index=False)

print("Keywords have been extracted and saved to the Excel file.")

