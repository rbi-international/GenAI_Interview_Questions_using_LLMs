# GenAI Interview Questions Generator

This project uses generative AI technologies to automatically create high-quality interview questions and answers from PDF documents. Simply upload a PDF document, and the system will generate a set of relevant questions and answers that help prepare for interviews or tests on that subject matter.

## 🔑 Key Features

- **PDF Processing**: Upload any PDF document to extract meaningful content
- **Question Generation**: Uses advanced LLMs to create relevant interview questions based on document content
- **Answer Generation**: Automatically generates comprehensive answers to each question
- **CSV Export**: Results are saved to a CSV file for easy use and sharing
- **Web Interface**: Simple and intuitive interface for uploading documents and retrieving results

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.13+
- **AI/ML**: LangChain, OpenAI GPT-3.5 Turbo
- **Vector Store**: FAISS for semantic search
- **Document Processing**: PyPDF for PDF parsing
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5, jQuery

## 📋 How It Works

1. **Upload a PDF**: Use the web interface to upload your PDF document
2. **Processing**: The system processes the document using a RAG (Retrieval-Augmented Generation) pipeline:
   - Extracts text from the PDF
   - Chunks the text into manageable segments
   - Creates embeddings for semantic search
   - Generates relevant interview questions
   - Creates comprehensive answers to each question
3. **Results**: Download a CSV file containing all generated questions and answers

## 🚀 Installation & Setup

### Prerequisites

- Python 3.10+ (3.13 recommended)
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/rbi-international/GenAI_Interview_Questions_using_LLMs.git
cd GenAI_Interview_Questions_using_LLMs

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Configuration

Create a `.env` file in the root directory with your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

### Running the Application

```bash
# Start the FastAPI server
python app.py
```

Visit `http://localhost:8080` in your browser to access the application.

## 📂 Project Structure

```
/
├── data/                # PDF files
├── research/            # Contains experimental notebooks
├── src/                 # Python source code
│   ├── helper.py        # Utility functions for PDF processing and LLM pipeline
│   ├── prompt.py        # Prompt templates for question generation
│   └── __init__.py
├── static/              # Static assets
│   ├── docs/            # Uploaded PDFs
│   └── output/          # Generated CSV files
├── templates/           # HTML templates
│   └── index.html       # Main application page
├── app.py               # FastAPI application
├── README.md            # This documentation
├── pyproject.toml       # Project configuration
└── requirements.txt     # Project dependencies
```

## 🤝 Usage Example

1. Visit the web application at `http://localhost:8080`
2. Click on the file upload area and select a PDF document
3. Click "Generate Q&A" to process the document
4. Wait for processing to complete
5. Click the download button to get your questions and answers as a CSV file

## 🧠 Technical Details

### RAG Pipeline

The system uses a Retrieval-Augmented Generation (RAG) approach:

1. **Document Loading**: PDF documents are loaded and parsed
2. **Text Chunking**: Content is divided into chunks for processing
3. **Embedding Generation**: Text chunks are converted to vector embeddings
4. **Question Generation**: LLM generates questions based on document content
5. **Answer Generation**: For each question, relevant context is retrieved and a comprehensive answer is generated

### Language Model

The system uses OpenAI's GPT-3.5 Turbo model for question and answer generation, with carefully crafted prompts to ensure high-quality outputs.

## 🔮 Future Improvements

- Support for more document formats (DOCX, TXT, etc.)
- Customizable question types and difficulty levels
- Multi-document processing
- Batch processing capabilities
- Answer evaluation and scoring

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

This project was developed with guidance and inspiration from:
- [DS with Bappy](https://www.youtube.com/@dswithbappy)
- [Bappy Ahmed's GitHub](https://github.com/entbappy)
- Bappy Ahmed's Udemy course: [Generative AI with AI Agents: MCP for Developers](https://www.udemy.com/course/generative-ai-with-ai-agents-mcp-for-developers)

---

Made with ❤️ by Rohit Bharti