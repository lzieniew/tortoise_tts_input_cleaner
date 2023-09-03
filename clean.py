import re

import inflect


# Function to break a sentence into chunks of up to 180 words
def break_sentence(sentence):
    words = sentence.split()
    chunks = []
    for i in range(0, len(words), 180):
        chunk = ' '.join(words[i:i+180])
        chunks.append(chunk)
    return chunks


def process_text(text):
    text = text.replace('\n', ' ')
    text = re.sub(r'(\w+)- (\w+)', r'\1\2', text)
    text = text.replace('-', ' ')
    text = text.replace('—', ' ')
    text = text.replace('"', ' ')
    text = text.replace("'", ' ')
    text = text.replace("’", '')
    text = text.replace("'", '')
    text = text.replace('"', '')
    text = text.replace('“', '')
    text = text.replace('”', '')

    # Convert numbers to their word form
    p = inflect.engine()
    for word in text.split():
        if word.isdigit():
            text = text.replace(word, p.number_to_words(word))

    # Split multi-letter abbreviations into separate letters
    text = re.sub(r'\b([A-Z]{2,})\b', lambda x: ' '.join(list(x.group())), text)

    # Handle mixed-case abbreviations like SQLAlchemy
    text = re.sub(r'([A-Z]{2,})([a-z])', lambda x: ' '.join(list(x.group(1))) + ' ' + x.group(2), text)

    # Split text into sentences and start each sentence on a new line
    sentences = re.split('([.!?;])', text)
    processed_text = ''
    for i in range(0, len(sentences) - 1, 2):
        sentence = sentences[i] + sentences[i + 1]

        # Check if the sentence has more than 150 words
        if len(sentence.split()) > 150 and sentences[i + 1] == ';':
            sentence = sentence.replace(';', '.')

        # Check if the sentence contains at least one word character
        if re.search(r'\w', sentence):
            # Break the sentence into chunks of up to 180 words
            chunks = break_sentence(sentence.strip())
            for chunk in chunks:
                processed_text += chunk + '\n'

    return processed_text


if __name__ == '__main__':
    with open("input.txt", "r") as infile:
        input_text = infile.read()

    processed_text = process_text(input_text)

    with open("output.txt", "w") as outfile:
        outfile.write(processed_text)

    print("Text processing complete. Check output.txt for the result.")
