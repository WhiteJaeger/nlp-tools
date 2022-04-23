# NLP Tools

## N-gram based and Syntactic Translation Evaluation Metrics

This repository contains a Flask web application which aims to help with measuring the performance of the machine &
human translation. 

Translation evaluation metrics include:
* N-gram based:
    * BLEU
    * GLEU
    * Character n-gram F-score
    * NIST
    * METEOR
* Sentence Trees based:
    * Subtree Metric
    * Subtree Metric Augmented

Other NLP Tools:
* Context Part-of-speech tagger
* Sentence Trees builder

This app could be accessed either remotely - it is deployed at http://nlp-tools.herokuapp.com/ - or
locally - by following the steps below.

## Running the app locally

* Prerequisites:

    * Python version >= 3.8.
    * Node >= 16.
    * It is strongly recommended to create a [virtual environment](https://docs.python.org/3/library/venv.html) for the app.

0. Install server dependencies by running the following command:

    ```bash
    pip install -r requirements.txt
    ```
1. Download the following NLTK corpora: `stopwords punkt averaged_perceptron_tagger wordnet`

   with NLTK downloader:
    ```bash
    python -m nltk.downloader stopwords punkt averaged_perceptron_tagger wordnet
    ```
2. Install client dependencies with the following command:

   ```bash
   cd client && npm i && cd ..
   ```
3. Run the application:
   1. Set env variables: 
      1. `export FLASK_APP=server.py`
      1. `export SERVER_MODE=development`
      1. `export PYTHONPATH=${PYTHONPATH}:app`
   2. Start the server: 
      1. `flask run`
   3. Open an additional terminal tab and start the client:
      1. `cd client && npm run start`
4. Head to the `localhost:3000` in browser.
