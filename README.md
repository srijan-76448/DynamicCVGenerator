# DynamicCVGenerator

![](https://visitcount.itsvg.in/api?style=plastic&id=srijan-76448.DynamicCVGenerator&icon=0&color=1)
![](https://img.shields.io/badge/Version-14.12.2024-darkblue?style=plastic)

This Python script generates a professional resume in PDF format. It leverages JSON data files to define user information, styles, and templates. The script processes this data, generates Markdown, and then converts it to a polished PDF document using `wkhtmltopdf`.

## Installation

1. Install `python` and `pip` if you haven't done so already.
2. Clone the repository: `git clone https://github.com/srijan-76448/DynamicCVGenerator.git`
3. Navigate to the repository directory: `cd DynamicCVGenerator/src`

## Usage

1. Create a JSON file containing the necessary data named `data.jsonc`. please maintain the format mentioned in the `struct.jsonc` file.
2. Add your images to the `imgs` directory. `This feature is not yet complete.`
3. Run the script with the following command: `python main.py [input file] [output file]`

> **Note**: <br>
> Create all the files as `jsonc` not `json`.
