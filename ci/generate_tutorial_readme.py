"""Write a directory of tutorial notebooks to the README file.

Run this script from the root of the github repository.

"""
import os
from glob import glob


def main():

    readme_text = [
        "# Neuromatch Academy Tutorial Notebooks",
        "",
    ]

    day_paths = sorted(glob("tutorials/W?D?_*"))
    for day_path in day_paths:

        day_name = os.path.split(day_path)[-1]
        day_code, topic = day_name.split("_")

        # Split the UpperCamelCase topic name into separate words
        topic_words = []
        for letter in topic:
            if letter.isupper():
                topic_words.append(letter)
            else:
                topic_words[-1] += letter
        topic = " ".join(topic_words)

        # Note: this will fail if we have 10 notebooks
        notebooks = sorted(glob(f"{day_path}/*.ipynb"))

        if not notebooks:
            continue

        # Build the table header
        readme_text.extend([
            f"## {day_code} - {topic}",
            "",
        ])

        # Build the table itself
        readme_text.extend(write_badge_table(notebooks))

        readme_text.append("\n")

    # Write the README file
    with open("tutorials/README.md", "w") as f:
        f.write("\n".join(readme_text))


def write_badge_table(notebooks):

    table_text = [
        "|   | Runnable | Static |",
        "| - | -------- | ------ |",
    ]

    # Add each row of the table
    for i, local_path in enumerate(notebooks, 1):

        colab_badge = make_colab_badge(local_path)
        nbviewer_badge = make_nbviewer_badge(local_path)
        table_text.append(
            f"| Tutorial {i} | {colab_badge} | {nbviewer_badge} |"
        )
    table_text.append("\n")

    return table_text


def get_student_links(instructor_notebooks):

    student_notebooks = []
    for instructor_nb in instructor_notebooks:
        day_path, nb_fname = os.path.split(instructor_nb)
        student_notebooks.append(f"{day_path}/student/{nb_fname}")
    return student_notebooks


def make_colab_badge(local_path):
    """Generate a Google Colaboratory badge for a notebook on github."""
    alt_text = "Open In Colab"
    badge_svg = "https://colab.research.google.com/assets/colab-badge.svg"
    url_base = (
        "https://colab.research.google.com/"
        "github/NeuromatchAcademy/course-content/blob/master/"
    )
    return make_badge(alt_text, badge_svg, url_base, local_path)


def make_nbviewer_badge(local_path):
    """Generate an NBViewer badge for a notebook on github."""
    alt_text = "View the notebook"
    badge_svg = "https://img.shields.io/badge/render-nbviewer-orange.svg"
    url_base = (
        "https://nbviewer.jupyter.org/"
        "github/NeuromatchAcademy/course-content/blob/master/"
    )
    return make_badge(alt_text, badge_svg, url_base, local_path)


def make_badge(alt_text, badge_svg, url_base, local_path):
    """Generate a markdown element for a badge image that links to a file."""
    return f"[![{alt_text}]({badge_svg})]({url_base}/{local_path})"


if __name__ == "__main__":

    main()
