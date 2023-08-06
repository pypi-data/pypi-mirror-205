# Chowlk Converter - Unofficial fork

**IMPORTANT NOTICE**: This is an unofficial temporary fork of [Chowlk](https://github.com/oeg-upm/Chowlk). Please refer to the original repository.

![Logo](./resources/logo.png)

Tool to transform ontology conceptualizations made with diagrams.net into OWL code.

The conceptualizations should follow the [Chowlk visual notation](https://chowlk.linkeddata.es/notation.html). Please visit the specification for more details.

Citing Chowlk: If you used Chowlk in your work, please cite the [ESWC paper](https://2022.eswc-conferences.org/wp-content/uploads/2022/05/paper_90_Chavez-Feria_et_al.pdf):

```bib
@InProceedings{10.1007/978-3-031-06981-9_20,
author="Ch{\'a}vez-Feria, Serge
and Garc{\'i}a-Castro, Ra{\'u}l
and Poveda-Villal{\'o}n, Mar{\'i}a",
editor="Groth, Paul
and Vidal, Maria-Esther
and Suchanek, Fabian
and Szekley, Pedro
and Kapanipathi, Pavan
and Pesquita, Catia
and Skaf-Molli, Hala
and Tamper, Minna",
title="Chowlk: from UML-Based Ontology Conceptualizations to OWL",
booktitle="The Semantic Web",
year="2022",
publisher="Springer International Publishing",
address="Cham",
pages="338--352"
}
```

## How to use the tool

You have several options to use this tool.

### 1. The web application

1. Go to the [chowlk.linkeddata.es](https://chowlk.linkeddata.es/) web application.
1. Download the Chowlk template.
     * Complete version of the template [here](https://github.com/oeg-upm/chowlk_spec/blob/master/resources/chowlk-library-complete.xml)
     * Lightweight version of the template [here](https://github.com/oeg-upm/chowlk_spec/blob/master/resources/chowlk-library-lightweight.xml)
1. In diagrams.net go to File > Open Library from > Device ...
1. Select the library downloaded.
1. Make your conceptualization using the blocks that will appear on the side bar.
1. Download the diagram in xml format.
1. Drag and drop your diagram in the Service dropping area and download your TTL file.

### 2. The API

The following command line will return the ontology in Turtle format.

```bash
curl -F 'data=@/path/to/diagram.xml' https://chowlk.linkeddata.es/api
```

The service will return the following dictionary:

```json
{
  "ttl_data": "@prefix ns: ...",
  "new_namespaces": {"ns1": "https://namespace1.com#", "ns2": "https://namespace2.com#"},
  "errors": {"Concepts": [{"message": "Problem in text", "shape_id": "13", "value": "ns:Building Element"}],
             "Attributes": [{"message": "Problem in cardinality", "shape_id": 45, "value": "ns:ifcIdentifier"}],
             "Arrows": [],
             "Rhombuses": [],
             "Ellipses": [],
             "Namespaces": [],
             "Metadata": [],
             "Hexagons": [],
             "Individual": []}
}
```

* **ttl_data:** Contains the ontology generated from the diagram in Turtle format. It is returned in string format.
* **new_namespaces:** Contains the new namespaces created for the ontology, when prefixes are founded in the model but are not declared in the namespace block in the diagram. The returned object is a dictionary with the following format: {"prefix1": "namespace1", "prefix2": "namespace2"}
* **errors:** Contains the errors founded in the ontology diagram, organized by types. The following keywords can be founded: "Concepts", "Arrows", "Rhombuses", "Ellipses", "Attributes", "Namespaces", "Metadata", "Hexagons", "Individual". The value for these keywords is an array that may contain objects that have the following structure:

```json
{
  "message": "Some message related to the problem",
  "shape_id": "An integer id that identify the problematic shape in the diagram",
  "value": "the actual text related with the shape"
}
```

### 3. Running it from source

### Copy the project

```bash
git clone https://github.com/oeg-upm/Chowlk.git
git checkout webservice
```

### Requirements

```bash
pip install -r requirements.txt
```

### To convert a diagram

* If the desired format is ttl:

```bash
python converter.py path/to/diagram.xml output/path/ontology.ttl --type ontology --format ttl
```

* If the desired format is rdf/xml:

```bash
python converter.py path/to/diagram.xml output/path/ontology.xml --type ontology --format xml
```

### To run the app locally

```bash
python app.py
```

## Publications

* Chávez-Feria, S., García-Castro, R., Poveda-Villalón, M. (2022). Chowlk: from UML-Based Ontology Conceptualizations to OWL. In: , et al. The Semantic Web. ESWC 2022. Lecture Notes in Computer Science, vol 13261. Springer, Cham. https://doi.org/10.1007/978-3-031-06981-9_20

* Chávez-Feria, S., García-Castro, R., Poveda-Villalón, M. (2021). _Converting UML-based ontology conceptualizations to OWL with Chowlk. In ESWC (Poster and Demo Track)_

## Contact

* Serge Chávez-Feria (serge.chavez.feria@upm.es)
* Maria Poveda-Villalón (mpoveda@fi.upm.es)
