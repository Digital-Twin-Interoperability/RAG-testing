# Running the App

1.) Create a folder named .streamlit (don't forget the period!)

2.) Under /.streamlit, make a file named secrets.toml

3.) secrets.toml holds your OpenAI API key. It should look like: OPENAI_API_KEY = "sk-..." (where "sk-..." is your key). Save.

4.) Launch from the terminal: streamlit run app.py (if this doesn't work, do python -m streamlit run app.py)


# What is This

This is a very simple example of how retrieval-augmented generation works to "fine tune" (note: this isn't actually fine-tuning, that's a separate process entirely) an LLM on a specific knowledge base (like a PDF you upload.)

# Things to Do

1.) Have the AI intelligently take inputs and determine what knowledge base would be best to use to answer.

1.5) ex. If the AI receives a call that says "Help me turn my rover over!", it should know to use how-to-turn-rovers-over.pdf for relevant instructions.

2.) Have fun!
