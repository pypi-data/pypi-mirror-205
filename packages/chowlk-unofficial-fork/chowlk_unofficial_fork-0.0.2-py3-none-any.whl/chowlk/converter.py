import argparse

from chowlk.transformations import transform_ontology
from chowlk.utils import read_drawio_xml


def converter(diagram_path, output_path, type, format):
    root = read_drawio_xml(diagram_path)
    ontology_turtle, ontology_xml, namespaces, errors = transform_ontology(
        root
    )

    file = open(output_path, mode="w")

    if format == "ttl":
        file.write(ontology_turtle)
    elif format == "xml":
        file.write(ontology_xml)

    print_errors(errors)
    file.close()


def print_errors(errors):
    for error_type in errors:
        error = errors[error_type]
        if isinstance(error, list):
            for content in error:
                if "message" in content:
                    print(
                        "\nError " + error_type + ": " + content.pop("message")
                    )
                else:
                    print("\nError " + error_type + ": ")
                for type in content:
                    print("\t" + type + ": " + content[type])
        else:
            print("\nError " + error_type + ": " + error.pop("message"))
            for type in error:
                print("\t" + type + ": " + error[type])


def main():
    parser = argparse.ArgumentParser(
        description="Convert an xml conceptualization into an ontology."
    )
    parser.add_argument(
        "diagram_path", type=str, help="the path where the diagram is located"
    )
    parser.add_argument(
        "output_path",
        type=str,
        help="the desired location for the generated ontology",
    )
    parser.add_argument(
        "--type", type=str, default="ontology", help="ontology or rdf data"
    )
    parser.add_argument(
        "--format", type=str, default="ttl", help="file format: ttl or xml"
    )
    args = parser.parse_args()

    converter(args.diagram_path, args.output_path, args.type, args.format)


if __name__ == "__main__":
    main()
