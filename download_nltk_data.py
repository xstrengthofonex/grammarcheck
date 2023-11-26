import nltk


def download_nltk_data():
    nltk.download("punkt")
    nltk.download("averaged_perceptron_tagger")
    # nltk.download("brown")
    # nltk.download("universal_tagset")
    # nltk.download("gutenberg")
    # nltk.download("treebank")


if __name__ == '__main__':
    download_nltk_data()
