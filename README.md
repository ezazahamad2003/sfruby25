# CompetitorCrusher

CompetitorCrusher is an AI-powered competitive intelligence engine designed to perform deep research and analysis on any company. By providing a company profile in a `.txt` or `.pdf` file, the tool leverages the Perplexity AI API to generate a comprehensive 7-part report covering the competitive landscape.

## Features

-   **Dynamic Input**: Accepts a file path for company data (`.txt` or `.pdf`).
-   **PDF Content Extraction**: Automatically extracts text from PDF files for analysis.
-   **AI-Powered Analysis**: Uses the `sonar-deep-research` model from Perplexity for high-quality insights.
-   **Comprehensive 7-Part Reporting**:
    1.  **Competitor Identification**: Pinpoints direct, indirect, and emerging competitors.
    2.  **Products & Services Analysis**: Compares feature sets, roadmaps, and innovations.
    3.  **Pricing Strategy Analysis**: Investigates pricing models, tiers, and customer value perception.
    4.  **Marketing & Sales Strategy**: Analyzes branding, channels, and campaign effectiveness.
    5.  **Customer Experience & Sentiment**: Evaluates customer support, reviews, and loyalty.
    6.  **Business Operations & Financial Health**: Assesses market share, funding, and operational efficiency.
    7.  **SWOT Analysis**: Provides a detailed breakdown of Strengths, Weaknesses, Opportunities, and Threats.
-   **JSON Output**: Saves the detailed analysis to a timestamped `.json` file for easy review and integration.

## Technology Stack

-   **Language**: Python 3
-   **AI Engine**: Perplexity AI API (`sonar-deep-research`)
-   **Core Libraries**:
    -   `requests`: For making API calls.
    -   `PyPDF2`: For extracting text from PDF files.
    -   `python-dotenv`: for managing environment variables.

## Setup and Installation

Follow these steps to get the CompetitorCrusher engine running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/ezazahamad2003/sfruby25.git
cd sfruby25
```

### 2. Set Up a Virtual Environment (Recommended)

It's best practice to use a virtual environment to manage project dependencies.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

All required libraries are listed in the `requirements.txt` file.

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Your API Key

The script requires a Perplexity API key to function.

1.  Create a new file named `.env` inside the `backend` directory.
2.  Open the `.env` file and add your API key in the following format:

    ```
    PERPLEXITY_API_KEY=your_api_key_here
    ```

    Replace `your_api_key_here` with your actual key from the [Perplexity AI platform](https://www.perplexity.ai/).

## Usage

1.  **Prepare Your Company Data**: Create a `.txt` file (or use a `.pdf`) containing the company profile or data you want to analyze. An example file, `company_data.txt`, is included in the `backend` directory.

2.  **Run the Script**: Navigate to the `backend` directory and run the main script.

    ```bash
    cd backend
    python main.py
    ```

3.  **Provide the File Path**: When prompted, enter the path to your company data file.
    -   To use the included example, simply press **Enter**.
    -   To use your own file, type the path (e.g., `C:\Users\YourUser\Documents\my_company.pdf`) and press **Enter**.

4.  **Get Your Report**: The script will begin the analysis, which may take several minutes. Once complete, it will save a detailed report in a `.json` file in the `backend` directory (e.g., `competitor_analysis_YourCompany_20250720_123000.json`). 