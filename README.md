# iCloud Media Orderer

## Overview
The iCloud Media Orderer is a Python application designed to organize your photos and videos downloaded from iCloud. When you download media from iCloud, the original creation dates are often lost, leading to disordered files. This application reads metadata from your media files and renames them based on their creation dates, restoring their proper order.

## Features
- Automatically renames photos and videos based on their metadata.
- Supports various file formats including JPG, JPEG, PNG, HEIC, MOV, and MP4.
- Provides a user-friendly interface using Streamlit.
- Allows selection of specific file types to rename.
- Handles errors by moving problematic files to a separate directory.

## Prerequisites
- Python 3.6 or higher
- Streamlit
- PIL (Pillow)
- Hachoir
- ExifTool

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/henukk/icloud-media-orderer.git
   cd icloud-media-orderer
   ´´´

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ´´´

3. Download and install ExifTool:
   - For Windows: Download the executable from the [ExifTool website](https://exiftool.org/) and place it in the `exiftool` directory within the project folder.

## Usage
1. Run the application:
   ```bash
   streamlit run main.py
   ´´´

2. In the Streamlit interface:
   - Click "Select Directory" to choose the folder containing your iCloud media files.
   - The application will display the file extensions found in the selected directory.
   - Select the file types you want to process.
   - Click "Order" to start renaming the files based on their metadata.

## File Structure
- `main.py`: The main script to run the Streamlit application.
- `file_handler.py`: Contains functions for reading metadata and renaming files.
- `utils.py`: Utility functions used in the Streamlit interface.
- `requirements.txt`: List of required Python packages.

## Contributing
If you'd like to contribute to the project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
   ```bash
   git checkout -b feature-name
   ´´´
3. Commit your changes.
   ```bash
   git commit -m "Description of feature or fix"
   ´´´
4. Push to the branch.
   ```bash
   git push origin feature-name
   ´´´
5. Create a pull request on GitHub.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements
- [ExifTool](https://exiftool.org/) by Phil Harvey for reading and writing metadata.
- [Streamlit](https://streamlit.io/) for creating the web interface.

---

By following these steps, you will be able to efficiently organize your iCloud photos and videos, restoring the original order based on the metadata creation dates. Enjoy your neatly ordered media library!
