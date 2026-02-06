# Contributing to Vector DB vs SQL DB Comparison

Thank you for your interest in contributing to this educational project! This document provides guidelines for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Setup](#development-setup)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Pull Request Process](#pull-request-process)
8. [Reporting Issues](#reporting-issues)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, background, or identity.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Accept criticism gracefully
- Prioritize the project's educational value

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal attacks
- Publishing private information
- Unprofessional conduct

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of databases
- Familiarity with Flask (for backend contributions)
- HTML/CSS/JavaScript knowledge (for frontend contributions)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/vectordb-vs-sqldb.git
   cd vectordb-vs-sqldb
   ```
3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/vectordb-vs-sqldb.git
   ```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

1. **Bug Fixes**
   - Fix issues in existing code
   - Improve error handling
   - Resolve edge cases

2. **Feature Enhancements**
   - Add new search capabilities
   - Improve UI/UX
   - Add visualization features

3. **Documentation**
   - Improve existing docs
   - Add tutorials
   - Create examples

4. **Performance Improvements**
   - Optimize database queries
   - Improve search algorithms
   - Reduce load times

5. **Testing**
   - Add unit tests
   - Create integration tests
   - Improve test coverage

## Development Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Development Dependencies

```bash
pip install pytest pytest-cov black flake8 mypy
```

### 4. Run the Application

```bash
./scripts/start.sh
```

### 5. Verify Setup

```bash
# Check backend health
curl http://localhost:5000/api/health

# Expected response:
# {"status": "healthy", "message": "API is running"}
```

## Coding Standards

### Python Code Style

We follow PEP 8 with some modifications:

```python
# Good
def search_products(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Search for products using the given query.
    
    Args:
        query: Search query string
        limit: Maximum number of results
        
    Returns:
        List of product dictionaries
    """
    results = []
    # Implementation
    return results

# Bad
def search(q,l=20):
    r=[]
    return r
```

### Key Principles

1. **Clear Naming**
   - Use descriptive variable names
   - Functions should be verbs
   - Classes should be nouns

2. **Documentation**
   - Add docstrings to all functions
   - Include type hints
   - Comment complex logic

3. **Error Handling**
   - Use try-except blocks
   - Provide meaningful error messages
   - Log errors appropriately

4. **Code Organization**
   - Keep functions small and focused
   - Group related functionality
   - Maintain separation of concerns

### JavaScript Code Style

```javascript
// Good
async function performSearch(query) {
    try {
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        return await response.json();
    } catch (error) {
        console.error('Search failed:', error);
        throw error;
    }
}

// Bad
function search(q){
    fetch(url).then(r=>r.json())
}
```

### CSS Code Style

```css
/* Good */
.product-card {
    background: white;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
}

/* Bad */
.pc{background:#fff;border-radius:8px;padding:15px;margin-bottom:15px}
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_traditional_db.py
```

### Writing Tests

Create test files in the `tests/` directory:

```python
# tests/test_traditional_db.py
import pytest
from backend.traditional_db import TraditionalDB

def test_insert_product():
    db = TraditionalDB(":memory:")
    product_id = db.insert_product(
        "Test Product",
        "Test Description",
        "Test Category",
        99.99
    )
    assert product_id > 0

def test_search_exact():
    db = TraditionalDB(":memory:")
    db.insert_product("Laptop", "Gaming laptop", "Electronics", 999.99)
    results, time = db.search_exact("laptop")
    assert len(results) > 0
    assert results[0]['name'] == "Laptop"
```

### Test Coverage Goals

- Aim for >80% code coverage
- Test both success and failure cases
- Include edge cases
- Test error handling

## Pull Request Process

### Before Submitting

1. **Update your fork**
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, documented code
   - Follow coding standards
   - Add tests for new features

4. **Test your changes**
   ```bash
   pytest
   ./scripts/start.sh  # Manual testing
   ```

5. **Format your code**
   ```bash
   black backend/
   flake8 backend/
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

### Commit Message Guidelines

Use clear, descriptive commit messages:

```
Good:
- "Add semantic search caching for improved performance"
- "Fix: Resolve CORS issue in production environment"
- "Docs: Update deployment guide with Docker instructions"

Bad:
- "fix bug"
- "update"
- "changes"
```

### Submitting the Pull Request

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request on GitHub**
   - Provide a clear title
   - Describe what changes you made
   - Explain why the changes are needed
   - Reference any related issues

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement
   
   ## Testing
   - [ ] Tests pass locally
   - [ ] Added new tests
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] No breaking changes
   ```

### Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Your contribution will be acknowledged

## Reporting Issues

### Before Creating an Issue

1. Search existing issues
2. Check documentation
3. Try the latest version
4. Gather relevant information

### Creating a Good Issue

Use the issue template:

```markdown
## Description
Clear description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: macOS 12.0
- Python: 3.9.7
- Browser: Chrome 95

## Screenshots
If applicable

## Additional Context
Any other relevant information
```

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed

## Development Workflow

### Typical Workflow

1. **Pick an issue** or create one
2. **Discuss approach** in the issue
3. **Fork and branch** from main
4. **Implement changes** with tests
5. **Submit PR** with clear description
6. **Address feedback** from reviewers
7. **Merge** when approved

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Code refactoring

## Additional Resources

### Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Vector Databases Guide](https://www.pinecone.io/learn/vector-database/)
- [Sentence Transformers](https://www.sbert.net/)

### Project Resources

- [README.md](README.md) - Project overview
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Technical architecture
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deployment guide
- [COMPARISON.md](docs/COMPARISON.md) - Database comparison

## Questions?

If you have questions:
1. Check the documentation
2. Search existing issues
3. Create a new issue with the `question` label
4. Join our discussions

## Recognition

Contributors will be:
- Listed in the project README
- Acknowledged in release notes
- Credited in documentation

Thank you for contributing to this educational project! Your efforts help others learn about database technologies.