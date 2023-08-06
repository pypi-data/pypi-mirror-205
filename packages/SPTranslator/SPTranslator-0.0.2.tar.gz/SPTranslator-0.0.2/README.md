# SPTranslator
SPTranslator(SyntaxPreserveTranslator) is a Python library powered by OpenAI API and designed for developers who work with multilingual projects.
This library seamlessly translates in-code comments and documentation while meticulously preserving the syntax and structure of your source code and data.
SPTranslator supports a wide range of markup languages(e.g., HTML, LaTeX), programming languages(e.g., Python), and data formats(e.g., JSON) and effortlessly integrates with your existing workflow.

# Usage
To use SPTranslator, first install the required dependencies:

```bash
pip install -r requirements.txt
```

Then, set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key"
```

Or set `api_key` to its value:

```python
from sptranslator.translator import Translator
translator = Translator(source_lang="English",target_lang="French",syntax="latex",api_key="your-api-key")
```

Now, you can use the library to translate text in various markup languages, programming languages, and data formats. Here's an example of translating a LaTeX document from English to French:

```python
from sptranslator.translator import Translator

source_lang = "English"
target_lang = "French"
syntax = "latex"
input_text = 
"""\section{Introduction}

There are two steps in our framework: {\em pre-training} and {\em fine-tuning}.

\section{Conclusion}

Our experiments demonstrate the effectiveness of our method."""

translator = Translator(source_lang, target_lang, syntax)
translated_text = translator.translate_text(input_text)

print(translated_text)
```

This will output the translated LaTeX code:

```LaTeX
\section{Introduction}

Il y a deux étapes dans notre cadre: {\em pré-entraînement} et {\em ajustement fin}.

\section{Conclusion}

Nos expériences démontrent l'efficacité de notre méthode.
```

And here's another example of translating a file from English to French:

```python
from sptranslator.translator import Translator

source_lang = "English"
target_lang = "French"
syntax = "latex"
input_path  = "./tests/experiments_details.tex"
output_path = "./tests/experiments_details_fr.tex"

translator = Translator(source_lang, target_lang, syntax)
translator.translate_file(input_path, output_path)
```

# Contributing
We welcome contributions to this project. To contribute, please follow these steps:

1. Fork this repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

# License
This project is licensed under the MIT License. See the [LICENSE file](https://github.com/uta0x89/SPTranslator/blob/main/LICENSE) for details.
