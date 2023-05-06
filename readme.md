# Interactive CSV Data Loader and Analyzer

This repository contains an interactive data loader and analyzer for CSV files, built using Python and Streamlit. The application allows users to select a CSV file from a folder, load its data, and analyze the data using various parameters.

## Features

- Select and load CSV files from a folder
- Initialize session state with parameters such as file names loaded, file list, data loaded, selected files, show preview, and show statistics
- Analyze loaded data, including the first 1000 rows of the file and the number of unique and duplicated values per column
- Select a column to show duplicated values

## Usage

To use this application, follow these steps:

1. Load the files you want to analyze in the folder dataset (or run gensampledataset.py to generate a sample dataset)
2. Check the dependencies in requirements.txt and install them if necessary
3. Run the following command in your terminal: `streamlit run main.py`

## Notes

This repository was largely created by Codex and the description was written by OpenAI. Contributions to the repository are welcome and encouraged.

Please note that this application is not intended for production use and may not be fully fault-tolerant. Additionally, this repository may be subject to certain license and usage restrictions. Please see the LICENSE file for more information.

## License

This repository is licensed under the [MIT License](https://opensource.org/licenses/MIT).
