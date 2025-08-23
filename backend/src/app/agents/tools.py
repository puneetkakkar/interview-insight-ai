import math
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import numexpr
import re

from langchain_core.tools import BaseTool, tool


def calculator_func(expression: str) -> str:
    """Calculates a math expression using numexpr.

    Useful for when you need to answer questions about math using numexpr.
    This tool is only for math questions and nothing else. Only input
    math expressions.

    Args:
        expression (str): A valid numexpr formatted math expression.

    Returns:
        str: The result of the math expression.
    """

    try:
        local_dict = {"pi": math.pi, "e": math.e}
        output = str(
            numexpr.evaluate(
                expression.strip(),
                global_dict={},  # restrict access to globals
                local_dict=local_dict,  # add common mathematical functions
            )
        )
        return re.sub(r"^\[|\]$", "", output)
    except Exception as e:
        raise ValueError(
            f'calculator("{expression}") raised error: {e}.'
            " Please try again with a valid numerical expression"
        )


calculator: BaseTool = tool(calculator_func)
calculator.name = "Calculator"


# Format retrieved documents
def format_contexts(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def load_chroma_db():
    # Create the embedding function for our project description database
    try:
        embeddings = OpenAIEmbeddings()
    except Exception as e:
        raise RuntimeError(
            "Failed to initialize OpenAIEmbeddings. Ensure the OpenAI API key is set."
        ) from e

    # Load the stored vector database
    chroma_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    retriever = chroma_db.as_retriever(search_kwargs={"k": 5})
    return retriever


def database_search_func(query: str) -> str:
    """Searches chroma_db for information in the company's handbook."""
    # Get the chroma retriever
    retriever = load_chroma_db()

    # Search the database for relevant documents
    documents = retriever.invoke(query)

    # Format the documents into a string
    context_str = format_contexts(documents)

    return context_str


database_search: BaseTool = tool(database_search_func)
database_search.name = (
    "Database_Search"  # Update name with the purpose of your database
)


def transcript_parser_func(transcript_text: str) -> str:
    """Parse transcript text to extract timestamps and content segments.
    
    Args:
        transcript_text (str): Raw transcript text with timestamps
        
    Returns:
        str: JSON string containing parsed segments with timestamps and content
    """
    import json
    
    # Regex patterns for different timestamp formats
    timestamp_patterns = [
        r'(\d{1,2}:\d{2}:\d{2})',  # HH:MM:SS or H:MM:SS
        r'(\d{1,2}:\d{2})',        # MM:SS or M:SS
    ]
    
    segments = []
    lines = transcript_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        timestamp = None
        content = line
        
        # Try to extract timestamp from the beginning of the line
        for pattern in timestamp_patterns:
            match = re.match(pattern, line)
            if match:
                timestamp = match.group(1)
                # Remove timestamp from content
                content = line[len(timestamp):].strip()
                # Remove common separators
                if content.startswith(('-', ':', '|', '>')):
                    content = content[1:].strip()
                break
        
        if content:  # Only add non-empty content
            segments.append({
                "timestamp": timestamp,
                "content": content
            })
    
    return json.dumps(segments, indent=2)


def entity_extractor_func(text: str) -> str:
    """Extract named entities from text including people, companies, and technical terms.
    
    Args:
        text (str): Text to analyze for entities
        
    Returns:
        str: JSON string containing categorized entities
    """
    import json
    
    # Simple pattern-based entity extraction
    # In production, you might want to use spaCy or similar NLP library
    
    entities = {
        "people": [],
        "companies": [],
        "technologies": [],
        "locations": []
    }
    
    # Common tech terms and programming languages
    tech_keywords = [
        "python", "javascript", "react", "node", "docker", "kubernetes",
        "aws", "gcp", "azure", "postgresql", "mongodb", "redis",
        "fastapi", "django", "flask", "express", "angular", "vue",
        "typescript", "java", "go", "rust", "c++", "sql"
    ]
    
    # Look for capitalized words (potential names/companies)
    words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
    
    # Extract tech terms (case insensitive)
    text_lower = text.lower()
    for tech in tech_keywords:
        if tech in text_lower:
            entities["technologies"].append(tech.title())
    
    # Simple heuristics for people vs companies
    for word in words:
        word_parts = word.split()
        if len(word_parts) == 2 and all(len(part) > 2 for part in word_parts):
            # Likely a person name (First Last)
            entities["people"].append(word)
        elif len(word_parts) == 1 and len(word) > 3:
            # Could be a company
            entities["companies"].append(word)
    
    # Remove duplicates and common false positives
    for key in entities:
        entities[key] = list(set(entities[key]))
        # Remove common words that aren't actually entities
        entities[key] = [e for e in entities[key] if e.lower() not in ['the', 'and', 'or', 'but', 'this', 'that']]
    
    return json.dumps(entities, indent=2)


def sentiment_analyzer_func(text: str) -> str:
    """Analyze sentiment and extract highlights and lowlights from transcript.
    
    Args:
        text (str): Text to analyze for sentiment
        
    Returns:
        str: JSON string containing highlights and lowlights
    """
    import json
    
    # Simple keyword-based sentiment analysis
    positive_keywords = [
        "excellent", "great", "good", "perfect", "amazing", "outstanding",
        "impressed", "love", "fantastic", "wonderful", "brilliant",
        "solved", "successful", "achieved", "accomplished", "clear"
    ]
    
    negative_keywords = [
        "bad", "terrible", "awful", "horrible", "wrong", "failed",
        "error", "problem", "issue", "struggle", "difficulty",
        "confused", "unclear", "stuck", "frustrated", "worried"
    ]
    
    sentences = re.split(r'[.!?]+', text)
    highlights = []
    lowlights = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 20:  # Skip very short sentences
            continue
            
        sentence_lower = sentence.lower()
        positive_score = sum(1 for word in positive_keywords if word in sentence_lower)
        negative_score = sum(1 for word in negative_keywords if word in sentence_lower)
        
        if positive_score > negative_score and positive_score > 0:
            highlights.append(sentence.strip())
        elif negative_score > positive_score and negative_score > 0:
            lowlights.append(sentence.strip())
    
    return json.dumps({
        "highlights": highlights[:5],  # Top 5 highlights
        "lowlights": lowlights[:5]     # Top 5 lowlights
    }, indent=2)


def content_categorizer_func(content: str) -> str:
    """Categorize content segments into interview phases.
    
    Args:
        content (str): Content to categorize
        
    Returns:
        str: Category name
    """
    content_lower = content.lower()
    
    # Define categories and their keywords
    categories = {
        "introduction": ["introduce", "background", "tell me about yourself", "experience"],
        "problem_description": ["problem", "challenge", "issue", "requirement", "task"],
        "solution_discussion": ["solution", "approach", "implement", "design", "architecture"],
        "coding": ["code", "function", "algorithm", "data structure", "implementation"],
        "testing": ["test", "debug", "validate", "verify", "edge case"],
        "questions": ["question", "ask", "clarify", "understand", "explain"],
        "conclusion": ["conclusion", "final", "summary", "next steps", "feedback"]
    }
    
    # Score each category
    category_scores = {}
    for category, keywords in categories.items():
        score = sum(1 for keyword in keywords if keyword in content_lower)
        if score > 0:
            category_scores[category] = score
    
    # Return the highest scoring category, or "discussion" as default
    if category_scores:
        return max(category_scores.items(), key=lambda x: x[1])[0]
    return "discussion"


# Create tools
transcript_parser: BaseTool = tool(transcript_parser_func)
transcript_parser.name = "TranscriptParser"

entity_extractor: BaseTool = tool(entity_extractor_func)
entity_extractor.name = "EntityExtractor"

sentiment_analyzer: BaseTool = tool(sentiment_analyzer_func)
sentiment_analyzer.name = "SentimentAnalyzer"

content_categorizer: BaseTool = tool(content_categorizer_func)
content_categorizer.name = "ContentCategorizer"
