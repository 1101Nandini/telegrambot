import telebot
import docx

bot = telebot.TeleBot('7174749132:AAF2vTrgM6aQFYId9H1nuNL1_thRROPvT6s')

# Define the path to the docx file
docx_file_path = 'test.docx'

# Define the list of stop words
stop_words = ['the', 'is', 'in', 'on', 'at', 'are', 'a', 'an', 'of', 'for', 'to', 'and', 'or', 'with']

# Maximum length of the response content
MAX_RESPONSE_LENGTH = 500  # Change this value as needed

# Keywords that indicate a question
question_keywords = ['what is', 'which is', 'how is', 'what are', 'which are', 'how are', 'tell me about', 'why is', 'why are']

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to telegram bot")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    question = message.text.lower()
    response = generate_response(question)
    bot.reply_to(message, response)

def generate_response(question):
    # Check if the question starts with any of the question keywords
    for keyword in question_keywords:
        if question.startswith(keyword):
            # Extract the actual question without the keyword
            actual_question = question[len(keyword):].strip()
            
            # Remove stop words from the user's question
            question_words = actual_question.split()
            question_words = [word for word in question_words if word not in stop_words]
            actual_question = ' '.join(question_words)

            # Read the docx file
            text = read_docx(docx_file_path)

            # Find the relevant portion of text based on the user's query
            relevant_text = extract_relevant_text(text, actual_question)

            if relevant_text:
                return "From DOCX: {}".format(relevant_text)
            else:
                return "Sorry, I couldn't find relevant information for your question."

    # Check if the question matches any single keyword in the document
    # If yes, provide the corresponding answer
    if search_single_keyword_in_doc(question):
        return "From DOCX: {}".format(search_single_keyword_in_doc(question))

    # If the question doesn't match any predefined question format or single keyword, return a generic response
    return "Please ask relevant question."

def read_docx(file_path):
    doc = docx.Document(file_path)
    text = ''
    for para in doc.paragraphs:
        text += para.text
    return text

def extract_relevant_text(text, question):
    relevant_text = ''
    # You may need to customize this based on the structure of your docx file
    # Here, we find all occurrences of the user's query in the text
    index = text.lower().find(question)
    while index != -1:
        # Extract the relevant portion of text around each found index
        start_index = max(0, index - 100)
        end_index = min(len(text), index + len(question) + 100)
        relevant_text += text[start_index:end_index]
        # Find the next occurrence of the query
        index = text.lower().find(question, index + 1)

    return relevant_text



def search_single_keyword_in_doc(keyword):
    # Read the docx file
    text = read_docx(docx_file_path)
    # Check if the keyword is in the text
    if keyword.lower() in text.lower():
        # Return the text around the keyword
        index = text.lower().find(keyword.lower())
        start_index = max(0, index - 100)
        end_index = min(len(text), index + len(keyword) + 100)
        return text[start_index:end_index]
    return None

bot.polling()
