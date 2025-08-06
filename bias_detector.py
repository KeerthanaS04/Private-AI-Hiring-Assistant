from model.gemma_runner import GemmaModel

def detect_bias_in_text(text):
    gemma = GemmaModel()
    prompt = f"Analyze the following resume text and higlight any potential biased language: \n{text}"
    return gemma.generate(prompt)