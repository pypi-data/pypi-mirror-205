# roberta-base-en-plant-ner-case

A Named Entity Recognition (NER) model for plants based on the Roberta architecture.

## Installation

```bash
pip install roberta_base_en_plant_ner_case
```

## Usage

```python
import spacy
from roberta_base_en_plant_ner_case import load_model

nlp = load_model()
doc = nlp("Some example text here.")

for ent in doc.ents:
    print(ent.text, ent.label_)
```

## License

This package is licensed under the Apache 2.0 License.

## Author

This package was developed by [Mohammad Othman](https://mohammadothman.com/).

For more information and pre-trained models, please visit the [Hugging Face model hub](https://huggingface.co/MohammadOthman).