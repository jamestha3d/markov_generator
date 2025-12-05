def load_text(path):
    with open(path, "r", encoding="utf8") as f:
        return f.read()
    

def stream_train(file_path, model):
    """Train on very large files line-by-line"""
    with open(file_path, "r", encoding="utf8") as f:
        for line in f:
            model.train(line)