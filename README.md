
# SmartSheet Agents - Excel/CSV AI Assistant Code 

## Features:
**1. Dynamic Model Selection**

Automatically detects all your installed Ollama models
**Dropdown selection** for easy model switching
Connection status monitoring

**2. AI Agents**

* **Code Generation Agent:** Smarter code generation with better prompting
* **Code Review Agent:** Validates code safety and correctness
* **Data Insight Agent:** Provides automatic dataset analysis

**3. Safety & Reliability**

- Code safety validation (blocks dangerous operations)
- Error handling and user feedback
- Isolated code execution environment

**4. User Experience**

- Responsive UI with sidebar configuration
- Predefined example prompts for common tasks
- Real-time progress indicators
- Advanced settings panel

**5. Data Processing**

- Support for multiple CSV encodings
- Excel file handling
- Download options for both Excel and CSV formats
- Data preview with adjustable row count

**6. Smart Code Extraction**

- Code block parsing from LLM responses
- Handles various response formats
- Better code cleaning and validation

## 🔧 Usage Instructions:

**Setup Requirements:** 
- python 3.11++ or above
- Ollama on local system

**Install required Libraries:** 
```bash
pip install requirments.txt
```
**Start the ollama server inside command prompt**:

```bash
ollama serve  # Start Ollama server
```

**Run the Application:**
```bash
streamlit run main.py
```

**Use the Interface:**

- Select your preferred model from the dropdown
- Upload CSV/Excel files
- Use natural language prompts or example commands
- Review generated code before execution
- Download processed results



**💡 Example Prompts You Can Try:**

- "Add a profit margin column calculated as (revenue - cost) / revenue * 100"
- "Filter rows where sales are above the median value"
- "Create a summary table grouped by category"
- "Find all rows with missing values and highlight them"
- "Calculate running totals for the amount column"
