Word Count: 2,150
1.	Introduction
In my organisation, Department for Transport (DfT), one of the practical obstacles for analysts is accessing the correct data on time and securely. Datasets are usually owned by different teams, stored in separate systems, and protected by access controls that require formal requests. It can take days for access even when data exists which can limit how quickly analysis can be done.
This project explores an alternative approach by using a publicly available government API. DfT publishes road traffic statistics through a web API which means the data can be accessed directly without relying on internal data owners. 
The goal was to build a data product that follows software engineering best practices. This included version control, automated testing, continuous integration, and clear documentation. The result is a prototype that could realistically sit inside my team’s workflow.

2.	Product Overview
The product is a command line data tool that retrieves traffic flow data from the Road Traffic API then converts it into a table which is exported as a CSV file together with a trend chart visual. The data used is Average Annual Daily Flow which represents how many vehicles typically pass a given road point each day.
The product is designed for analysts and planners who want a quick way to explore traffic patterns without manually querying the API or writing custom scripts. 
Running the tool produces two outputs:
•	A CSV file
•	A PNG visual chart
The tool therefore acts as a bridge between the raw API data and analytical requirements for the organisation.

 
3.	Design and Architecture
The system was designed as a simple and easy to understand data pipeline with each stage separated into a module. I took this approach to keep the codebase manageable and to reflect best practices in software engineering.
Before implementation, I created a system design diagram to outline the main components of the data product and visualise how data flows between them. This helped clarify module responsibilities and structure.
 
(Figure 1: system design diagram)
![System Design Diagram](<Docs/Images/Figure 1 system design diagram.png>)

The overall workflow follows a clear sequence. First, data is retrieved from the API and converted into a usable format. Then the data is processed into outputs and run through a simple command line interface. I was able to ensure each part was tested and issues resolved before progressing further with the development by splitting the process into separate components.

The pipeline was divided into four main parts:

API Client
The API client is responsible for communicating with the DfT Road Traffic API. It handles the URL and parameter construction as well as basic error handling. This ensures all external communication is manageable through a single point and issues such as API errors are resolved before progressing further.

Parser
The parser converts the raw JSON response returned by the API into a table that can be used for analyses. Separating this step makes it clear and easy to manage the data structure and allows testing the logic in isolation.

Pipeline
The pipeline module manages the overall process. It combines the API client and the parser, writes the cleaned data to disk as a CSV file and then generates a simple trend visual where appropriate. This module also represents the core functionality of this data product.

Command Line Interface (CLI)
The CLI provides a simple entry point for running the pipeline without requiring users to interact with the underlying code. This makes the tool easier to use for analysts or other users who are comfortable with the command line but do not want to modify Python scripts.

This modular structure reflects how data products are usually developed in my organisation. It supports incremental, test driven development and makes automated testing more straightforward.
 
4.	Project Planning and Workflow
The project was planned and managed using GitHub Issues, branches, pull requests, and a GitHub Projects board aligned to a lightweight agile workflow. GitHub Issues were used to capture the main requirements of the system with each issue representing a single feature or development stage. These included implementing the API client, adding the parser, building the data pipeline, introducing a command-line interface, writing tests, and configuring continuous integration.
A dedicated branch was created for each issue and the feature was implemented in isolation before being merged back into the main branch via a pull request. This followed a one-issue, one-branch, one-pull-request pattern. This made it easy to track progress and ensured that code changes, documentation and requirements remained aligned throughout development.
A GitHub Projects board was used as a planning and tracking tool. Issues were moved through the stages Todo, In Progress, and Done. This provided a clear overview of the project’s status at any point in time and helped manage scope while ensuring that changes were introduced incrementally. This workflow reflects how agile development is commonly practiced in my organisation and in other professional teams.
 
(Figure 2: Github Project Board)
![Github Project Board](<Docs/Images/Figure 2 Github Project Board.png>)
 
5.	Requirements Capture and MVP Development
The project requirements were captured and managed using GitHub Issues with each issue representing a single feature or development step. This approach allowed the product to be built incrementally rather than attempting to implement all functionality at once.
Development started with creating the basic project structure which included packaging, dependency management and a simple test to confirm that the test framework was working. This provided a good foundation for further development. The next step was implementing the API client which allowed data to be retrieved from the DfT Road Traffic API. At this stage, unit tests were written to verify correct URL handling and basic error scenarios before further functionality was added.
Once data retrieval was working, I created a parser module to convert the raw JSON into a structured table. This logic was tested in isolation using sample payloads to ensure the data transformation behaved as expected. Furthermore, the pipeline module was developed to combine the API client and parser, export the cleaned data to a CSV file and to create a simple trend visual. 
Finally, a command-line interface was added to allow the pipeline to be executed without modifying the code directly. At each stage, tests were added or extended to confirm that existing functionality still worked which ensured the system remained usable throughout development. This step-by-step, testing led approach resulted in a minimal viable product that could already retrieve, process, and visualise real traffic data before any additional enhancements were made.

 
6.	Testing and Continuous Integration
Testing was a core part of the development process and unit tests were written for each major part of the system.
Tests were written using pytest and were developed either before or alongside the implementation of each feature. This helped to catch issues early and ensured that each module behaved as expected before being integrated into the wider system.
Furthermore, continuous integration was set up using GitHub Actions. The CI workflow is triggered automatically on every push to the main branch and on pull requests. The pipeline installs the package in a clean environment and runs the full test suite. This ensures that failing tests are caught early and that broken code cannot be merged into the main branch.
Together, this ensured the implementation of the use of automated testing and CI/CD best practices in this projects development.
 
7.	How to Use the Product (User Documentation)
The repository should first be cloned. 
A Python virtual environment can then be created and activated followed by installing the package in editable mode:
pip install -e .

Once installed, the data pipeline can be run using the command line:
python -m road_traffic

Running the tool creates an outputs folder containing two files. The first is a CSV file (API-Road-trafficsample.csv) containing real traffic flow data retrieved from the DfT Road Traffic API. The second is a PNG image (Road-traffic_trend.png) showing a simple trend of average traffic volumes over time.
The CSV file can be opened in tools such as Excel, Power BI, or Python for further analysis. The chart provides a quick visual summary of the data.

To run the test suite manually, the following command can be used from the project root:
python -m pytest

 
8.	How the System Works (Technical Documentation)
The application is implemented as a Python package under src/road_traffic. The codebase is structured so that each part of the workflow has a clear responsibility and can be tested independently.
The overall data flow starts with an external API call and ends with files written to disk. Each stage of this process is handled by a separate module.

API Client (api_client.py)
The API client is responsible for all communication with the DfT Road Traffic API. It constructs request URLs, passes query parameters and performs basic error handling. Any issues with network requests or invalid responses are handled at this stage so that downstream code works with valid data.

Parser (parser.py)
The parser converts the raw JSON response returned by the API into a tabular structure. It handles different response formats and returns a Pandas DataFrame that can be used consistently by the rest of the system. Separating this logic makes it easier to test and adjust if the API response format changes.

Pipeline (pipeline.py)
The pipeline module coordinates the full workflow. It calls the API client to retrieve data, uses the parser to clean and structure the response, writes the resulting dataset to a CSV file, and generates a simple trend visual where appropriate. This module represents the core behaviour of the data product.

Command Line Interface (__main__.py)
The CLI provides a simple entry point so the pipeline can be run using a single command. This allows users to execute the workflow without interacting directly with the Python modules.

The application can be run locally using:
python -m road_traffic

Automated tests are written using pytest and cover the API client, parser, pipeline, and CLI. To run the full test suite locally:
python -m pytest

The same test process is also executed automatically using GitHub Actions. On every push or pull request to the main branch, the CI workflow installs the package and runs all tests. This ensures that changes do not break existing functionality and that the main branch remains stable. 

9.	Evaluation
This project set out to build a data product around the DfT Road Traffic API. The aim was to provide users with a simple way to retrieve traffic data from the API, export it as a usable CSV file and generate a basic visualisation to support an initial understanding of the data.

From a user perspective, the product is straightforward to use and behaves as expected. After installation, the user only needs to run a single command:
python -m road_traffic

This automatically contacts the DfT API, retrieves a sample of Average Annual Daily Flow data, and generates two outputs in the outputs folder: a CSV file and a PNG chart. The CSV file can be used for further analysis and the chart provides a quick visual summary of how total motor vehicle counts change over time. As a result, analysts or planners do not need prior knowledge of APIs or JSON formats to obtain useful data.

The system is straightforward and easy to follow from a technical point. The codebase is split into clear components with the API client managing communication with the DfT service, the parser converts raw JSON into tabular data, the pipeline coordinates the workflow, and the CLI provides a simple entry point. This separation improves readability, testability, and development. For example, additional API endpoints could be incorporated by extending the pipeline without rewriting the overall system. 

Automated testing and continuous integration are key strengths in the project. Unit tests cover the API client, parser, pipeline, and command-line interface which make it easier to change or extend the code without introducing issues. GitHub Actions runs the full test suite on every push and pull request which reflects best practices for protecting the main branch and supporting long-term maintainability.

The product also has clear limitations mainly due to its simplicity. There is no immediate support for filtering and the interface is not interactive. Furthermore, large queries may be slow or impractical for some users as the data is retrieved live from the API. These limitations are acceptable for an MVP and can be quickly improved in future development due to the modular nature of the product.

I also ensured that the project aligned with ethical and legal requirements including GDPR. However, no personal data or privacy risks were identified as the system uses publicly available non-personal data. The overall design therefore aligns with both my organisational data governance practices and wider regulatory requirements.

If the project were continued, I would include adding user-controlled filters, supporting additional DfT endpoints, and introducing a simple dashboard or web interface. Implementing local caching would also improve performance and reduce unnecessary API calls.

In summary, the project demonstrated how a realistic data product could be built using modern software engineering practices. It delivers usable outputs for end users alongside a clean, testable codebase for developers. 
