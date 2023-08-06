import os
import spacy
from spacy.util import get_package_path

package_path = get_package_path("roberta_base_en_plant_ner_case")
model_path = os.path.join(package_path, "model")

def load_model():
    return spacy.load(model_path)
