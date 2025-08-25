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
    
    # Enhanced regex patterns for different timestamp formats
    timestamp_patterns = [
        # Standard formats with optional square brackets or parentheses
        r'^\s*[\[\(]?(\d{1,2}:\d{2}:\d{2}(?:\.\d{3})?)\s*[\]\)]?\s*[-:\|>]?\s*',  # [HH:MM:SS.mmm] or (HH:MM:SS)
        r'^\s*[\[\(]?(\d{1,2}:\d{2})\s*[\]\)]?\s*[-:\|>]?\s*',                      # [MM:SS] or (MM:SS)
        r'^\s*[\[\(]?(\d{2,3}:\d{2})\s*[\]\)]?\s*[-:\|>]?\s*',                      # [MMM:SS] (for long videos)
        
        # Timestamp at the beginning with various separators
        r'^(\d{1,2}:\d{2}:\d{2}(?:\.\d{3})?)\s*[-:\|>]\s*',  # HH:MM:SS.mmm - content
        r'^(\d{1,2}:\d{2})\s*[-:\|>]\s*',                     # MM:SS - content
        
        # Timestamp ranges (start-end)
        r'^\s*[\[\(]?(\d{1,2}:\d{2}(?::\d{2})?)\s*-\s*\d{1,2}:\d{2}(?::\d{2})?\s*[\]\)]?\s*[-:\|>]?\s*',
        
        # SRT subtitle format (just the number part)
        r'^\d+\s*$',  # Skip SRT sequence numbers
        
        # Zoom/Teams meeting format
        r'^(\d{1,2}:\d{2}:\d{2})\s+[A-Za-z\s]+:\s*',  # HH:MM:SS Speaker Name: content
        
        # YouTube format
        r'^(\d{1,2}:\d{2})\s*(.+?)$',  # MM:SS content (fallback)
    ]
    
    segments = []
    lines = transcript_text.split('\n')
    current_speaker = None
    
    for line_num, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        # Skip SRT sequence numbers
        if re.match(r'^\d+\s*$', line):
            continue
        
        # Skip SRT timing lines (00:00:01,234 --> 00:00:05,678)
        if '-->' in line and re.search(r'\d{2}:\d{2}:\d{2}', line):
            continue
            
        timestamp = None
        content = line
        speaker = None
        
        # Try to extract timestamp from the beginning of the line
        for i, pattern in enumerate(timestamp_patterns):
            if i == len(timestamp_patterns) - 1:  # Last pattern is the fallback
                match = re.match(pattern, line)
                if match and ':' in match.group(1):
                    timestamp = match.group(1)
                    content = match.group(2) if match.lastindex and match.lastindex > 1 else ""
                    break
            else:
                match = re.match(pattern, line)
                if match:
                    timestamp = match.group(1)
                    # Remove timestamp and separators from content
                    content = re.sub(pattern, '', line).strip()
                    break
        
        # Special handling for speaker identification
        speaker_patterns = [
            r'^([A-Z][a-zA-Z\s]+):\s*(.+)$',  # Speaker Name: content
            r'^([A-Z][a-zA-Z\s]+)\s*-\s*(.+)$',  # Speaker Name - content
        ]
        
        for speaker_pattern in speaker_patterns:
            speaker_match = re.match(speaker_pattern, content)
            if speaker_match:
                potential_speaker = speaker_match.group(1).strip()
                # Check if it's likely a speaker name (not too long, not common words)
                if (len(potential_speaker.split()) <= 3 and 
                    len(potential_speaker) <= 30 and
                    potential_speaker.lower() not in ['interviewer', 'candidate', 'question', 'answer']):
                    speaker = potential_speaker
                    content = speaker_match.group(2).strip()
                    current_speaker = speaker
                break
        
        # If no timestamp found but we have previous context, try to infer
        if not timestamp and segments and content:
            # Check if this might be a continuation of previous content
            last_segment = segments[-1]
            if (len(content.split()) < 10 and 
                last_segment.get('timestamp') and
                not content.lower().startswith(('hello', 'hi', 'good', 'thank', 'so'))):
                # Likely a continuation, append to previous segment
                last_segment['content'] += ' ' + content
                continue
        
        # Clean up content
        content = content.strip()
        
        # Remove common transcript artifacts
        content = re.sub(r'\[inaudible\]', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\[unclear\]', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\[background noise\]', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
        content = content.strip()
        
        if content and len(content) > 2:  # Only add non-empty, meaningful content
            segment = {
                "timestamp": timestamp,
                "content": content
            }
            
            # Add speaker information if identified
            if speaker or current_speaker:
                segment["speaker"] = speaker or current_speaker
            
            # Add line number for debugging purposes
            segment["line_number"] = line_num + 1
            
            segments.append(segment)
    
    # Post-processing: merge very short segments with the next one
    merged_segments = []
    i = 0
    while i < len(segments):
        current = segments[i]
        
        # If current segment is very short and next exists, consider merging
        if (i < len(segments) - 1 and 
            len(current['content'].split()) <= 3 and
            not current['content'].endswith(('.', '!', '?'))):
            
            next_segment = segments[i + 1]
            # Merge if they're close in time or no timestamps
            if (not current.get('timestamp') or not next_segment.get('timestamp') or
                _timestamps_close(current.get('timestamp'), next_segment.get('timestamp'))):
                
                merged_content = current['content'] + ' ' + next_segment['content']
                merged_segment = {
                    "timestamp": current.get('timestamp') or next_segment.get('timestamp'),
                    "content": merged_content.strip()
                }
                
                # Preserve speaker info
                if current.get('speaker') or next_segment.get('speaker'):
                    merged_segment["speaker"] = current.get('speaker') or next_segment.get('speaker')
                
                merged_segment["line_number"] = current.get('line_number', i + 1)
                merged_segments.append(merged_segment)
                i += 2  # Skip both segments
                continue
        
        merged_segments.append(current)
        i += 1
    
    return json.dumps(merged_segments, indent=2)


def _timestamps_close(ts1: str, ts2: str, max_diff_seconds: int = 30) -> bool:
    """Check if two timestamps are close enough to be merged."""
    if not ts1 or not ts2:
        return True
        
    def parse_time(ts: str) -> int:
        """Convert timestamp to seconds."""
        if not ts or ':' not in ts:
            return 0
        parts = ts.split(':')
        try:
            if len(parts) == 2:  # MM:SS
                return int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:  # HH:MM:SS
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        except ValueError:
            pass
        return 0
    
    time1 = parse_time(ts1)
    time2 = parse_time(ts2)
    
    return abs(time1 - time2) <= max_diff_seconds


def entity_extractor_func(text: str) -> str:
    """Extract named entities from text including people, companies, and technical terms.
    
    Args:
        text (str): Text to analyze for entities
        
    Returns:
        str: JSON string containing categorized entities
    """
    import json
    
    # Enhanced pattern-based entity extraction
    # Comprehensive keyword-based approach for interview transcripts
    
    entities = {
        "people": [],
        "companies": [],
        "technologies": [],
        "locations": []
    }
    
    # Comprehensive tech terms and programming languages
    tech_keywords = [
        # Programming Languages
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", 
        "kotlin", "swift", "php", "ruby", "scala", "r", "matlab", "julia",
        
        # Frontend Technologies  
        "react", "angular", "vue", "svelte", "next.js", "nuxt", "gatsby",
        "html", "css", "sass", "less", "tailwind", "bootstrap", "material-ui",
        "jquery", "d3.js", "three.js", "webpack", "vite", "parcel",
        
        # Backend & Frameworks
        "node.js", "express", "fastapi", "django", "flask", "spring boot",
        "laravel", "rails", "asp.net", "gin", "fiber", "actix", "rocket",
        "socket.io", "yjs", "crdt", "crdts", "operational transformation",
        
        # Databases
        "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "sqlite",
        "cassandra", "dynamodb", "firestore", "neo4j", "influxdb", "clickhouse",
        
        # Cloud & DevOps
        "aws", "gcp", "azure", "docker", "kubernetes", "jenkins", "gitlab ci",
        "github actions", "terraform", "ansible", "vagrant", "helm", "istio",
        "prometheus", "grafana", "datadog", "splunk",
        
        # Data & AI/ML
        "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "jupyter",
        "apache spark", "hadoop", "kafka", "airflow", "mlflow", "kubeflow",
        
        # Testing & Tools
        "jest", "pytest", "junit", "selenium", "cypress", "postman", "git",
        "vs code", "intellij", "vim", "emacs", "jira", "confluence", "slack",
        
        # Architecture & Concepts
        "microservices", "api", "rest", "graphql", "grpc", "websockets",
        "oauth", "jwt", "ssl", "https", "ci/cd", "agile", "scrum", "tdd",
        "clean architecture", "solid principles", "design patterns"
    ]
    
    # Known major tech companies
    major_companies = [
        "google", "microsoft", "amazon", "apple", "meta", "facebook", "netflix",
        "tesla", "uber", "airbnb", "spotify", "slack", "zoom", "salesforce",
        "oracle", "ibm", "intel", "nvidia", "amd", "adobe", "twitter", "x",
        "linkedin", "github", "gitlab", "atlassian", "mongodb", "redis labs",
        "databricks", "snowflake", "cloudflare", "stripe", "shopify", "square",
        "paypal", "dropbox", "pinterest", "reddit", "discord", "twitch"
    ]
    
    # Common locations and remote work terms
    location_keywords = [
        "san francisco", "new york", "seattle", "austin", "boston", "chicago",
        "los angeles", "denver", "atlanta", "miami", "toronto", "vancouver",
        "london", "berlin", "amsterdam", "singapore", "sydney", "tokyo",
        "remote", "hybrid", "on-site", "distributed", "work from home", "wfh"
    ]
    
    text_lower = text.lower()
    
    # Extract technologies (case insensitive with context)
    for tech in tech_keywords:
        if tech in text_lower:
            # Add proper casing
            if tech.lower() in ["javascript", "typescript"]:
                entities["technologies"].append("JavaScript" if tech == "javascript" else "TypeScript")
            elif tech.lower() == "c++":
                entities["technologies"].append("C++")
            elif tech.lower() == "c#":
                entities["technologies"].append("C#")
            elif "." in tech:
                entities["technologies"].append(tech)  # Keep frameworks as-is (e.g., "Next.js")
            else:
                entities["technologies"].append(tech.title())
    
    # Extract companies (case insensitive)
    for company in major_companies:
        if company in text_lower:
            # Special handling for certain companies
            if company == "meta" and "facebook" not in text_lower:
                entities["companies"].append("Meta")
            elif company == "x" and "twitter" not in text_lower:
                entities["companies"].append("X (Twitter)")
            elif company != "meta" and company != "x":  # Avoid duplicates
                entities["companies"].append(company.title())
    
    # Extract locations
    for location in location_keywords:
        if location in text_lower:
            if location in ["remote", "hybrid", "on-site", "distributed", "work from home", "wfh"]:
                entities["locations"].append(location.title() if location != "wfh" else "WFH")
            else:
                entities["locations"].append(location.title())
    
    # Enhanced name extraction with better heuristics
    # Look for capitalized words (potential names/companies)
    name_patterns = [
        r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b',  # First Last
        r'\b[A-Z][a-z]+\s+[A-Z]\.\s*[A-Z][a-z]+\b',  # First M. Last
        r'\b[A-Z]\.\s*[A-Z][a-z]+\b',  # F. Last
    ]
    
    for pattern in name_patterns:
        names = re.findall(pattern, text)
        for name in names:
            name = name.strip()
            # Filter out common false positives and check if it's not already a known company
            if (name.lower() not in [c.lower() for c in entities["companies"]] and
                not any(stop in name.lower() for stop in [
                    'interview', 'question', 'problem', 'solution', 'discussion',
                    'project', 'system', 'design', 'code', 'test', 'data', 'user'
                ])):
                entities["people"].append(name)
    
    # Look for additional company patterns (Inc., Corp., LLC, etc.)
    company_patterns = [
        r'\b[A-Z][a-zA-Z\s&]+(?:Inc\.?|Corp\.?|LLC|Ltd\.?|Co\.?)\b',
        r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\s+(?:Technologies|Solutions|Systems|Software|Labs|Studios)\b'
    ]
    
    for pattern in company_patterns:
        companies = re.findall(pattern, text)
        for company in companies:
            company = company.strip()
            if len(company) > 3 and company not in entities["companies"]:
                entities["companies"].append(company)
    
    # Remove duplicates and clean up
    for key in entities:
        entities[key] = list(set(entities[key]))
        # Enhanced filtering of false positives
        entities[key] = [e for e in entities[key] if (
            len(e.strip()) > 1 and
            e.lower() not in [
                'the', 'and', 'or', 'but', 'this', 'that', 'with', 'from', 'they',
                'have', 'been', 'will', 'would', 'could', 'should', 'about', 'through',
                'during', 'before', 'after', 'above', 'below', 'between', 'among',
                'interview', 'candidate', 'interviewer', 'question', 'answer', 'time',
                'first', 'second', 'next', 'last', 'good', 'great', 'nice', 'okay'
            ] and
            not e.isdigit()
        )]
    
    # Sort entities for consistent output
    for key in entities:
        entities[key] = sorted(entities[key])
    
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
    """Categorize content segments into interview phases with human-readable names.
    
    Args:
        content (str): Content to categorize
        
    Returns:
        str: Human-readable category name
    """
    content_lower = content.lower()
    
    # Define categories and their keywords with human-readable names
    categories = {
        "Introduction": ["introduce", "background", "tell me about yourself", "experience", "welcome", "hello", "hi", "thank you for joining"],
        "Problem Description": ["problem", "challenge", "issue", "requirement", "task", "scenario", "case study", "situation"],
        "Solution Discussion": ["solution", "approach", "implement", "design", "architecture", "strategy", "plan", "methodology"],
        "Coding Session": ["code", "function", "algorithm", "data structure", "implementation", "programming", "write code", "let's code"],
        "Testing & Validation": ["test", "debug", "validate", "verify", "edge case", "unit test", "testing", "bug"],
        "Q&A Session": ["question", "ask", "clarify", "understand", "explain", "any questions", "do you have", "wondering"],
        "Technical Discussion": ["technical", "architecture", "system", "database", "framework", "technology", "stack"],
        "Behavioral Questions": ["tell me about a time", "describe a situation", "how do you handle", "teamwork", "leadership"],
        "Conclusion": ["conclusion", "final", "summary", "next steps", "feedback", "wrap up", "that's all", "thank you"]
    }
    
    # Score each category
    category_scores = {}
    for category, keywords in categories.items():
        score = sum(1 for keyword in keywords if keyword in content_lower)
        if score > 0:
            category_scores[category] = score
    
    # Return the highest scoring category, or "Discussion" as default
    if category_scores:
        return max(category_scores.items(), key=lambda x: x[1])[0]
    return "Discussion"


def timeline_consolidator_func(timeline_json: str) -> str:
    """Consolidate consecutive timeline events with the same category into coherent segments.
    
    Args:
        timeline_json (str): JSON string containing timeline events
        
    Returns:
        str: JSON string containing consolidated timeline events
    """
    import json
    from datetime import datetime, timedelta
    
    def parse_timestamp(timestamp_str):
        """Parse timestamp string to seconds for comparison."""
        if not timestamp_str:
            return 0
        
        # Handle various timestamp formats
        if ':' not in timestamp_str:
            return 0
        
        parts = timestamp_str.split(':')
        if len(parts) == 2:  # MM:SS
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:  # HH:MM:SS
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return 0
    
    try:
        timeline_events = json.loads(timeline_json)
        if not isinstance(timeline_events, list):
            return timeline_json  # Return as-is if not a list
        
        if len(timeline_events) <= 1:
            return timeline_json  # No consolidation needed
        
        consolidated_events = []
        current_group = []
        
        for event in timeline_events:
            if not isinstance(event, dict):
                continue
                
            timestamp = event.get('timestamp')
            category = event.get('category', 'Discussion')
            content = event.get('content', '')
            confidence = event.get('confidence_score', 0.8)
            
            # Start new group if first event or different category
            if not current_group or current_group[0]['category'] != category:
                # Process previous group if exists
                if current_group:
                    consolidated_events.append(_consolidate_group(current_group))
                current_group = [event]
            else:
                # Check if events are close in time (within 2 minutes)
                current_timestamp = parse_timestamp(timestamp)
                last_timestamp = parse_timestamp(current_group[-1].get('timestamp'))
                
                if abs(current_timestamp - last_timestamp) <= 120:  # 2 minutes
                    current_group.append(event)
                else:
                    # Too far apart, process current group and start new one
                    consolidated_events.append(_consolidate_group(current_group))
                    current_group = [event]
        
        # Process final group
        if current_group:
            consolidated_events.append(_consolidate_group(current_group))
        
        return json.dumps(consolidated_events, indent=2)
        
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        # Return original if parsing fails
        return timeline_json


def _consolidate_group(events):
    """Helper function to consolidate a group of similar events."""
    if len(events) == 1:
        return events[0]
    
    # Get timestamp range
    timestamps = [e.get('timestamp') for e in events if e.get('timestamp')]
    if timestamps:
        start_seconds = min(parse_timestamp(ts) for ts in timestamps)
        end_seconds = max(parse_timestamp(ts) for ts in timestamps)
        timestamp_range = format_timestamp_range(start_seconds, end_seconds)
    else:
        timestamp_range = events[0].get('timestamp')
    
    # Combine content intelligently
    contents = [e.get('content', '') for e in events if e.get('content')]
    category = events[0].get('category', 'Discussion')
    
    # Create meaningful summary based on category
    if len(contents) == 1:
        combined_content = contents[0]
    elif category == "Introduction":
        combined_content = f"Introduction phase covering {', '.join(contents[:3])}"
    elif category == "Q&A Session":
        combined_content = f"Q&A session with {len(contents)} questions and discussions"
    else:
        # Combine first and last content with count
        if len(contents) >= 2:
            combined_content = f"{contents[0]}. Discussion continued with {len(contents)-1} additional points including {contents[-1]}"
        else:
            combined_content = contents[0] if contents else ""
    
    # Calculate average confidence
    confidences = [e.get('confidence_score', 0.8) for e in events]
    avg_confidence = sum(confidences) / len(confidences)
    
    # Calculate duration if possible
    duration = None
    if len(timestamps) >= 2:
        duration_seconds = end_seconds - start_seconds
        if duration_seconds > 0:
            if duration_seconds >= 60:
                minutes = duration_seconds // 60
                seconds = duration_seconds % 60
                duration = f"{minutes}m {seconds}s" if seconds > 0 else f"{minutes}m"
            else:
                duration = f"{duration_seconds}s"
    
    consolidated_event = {
        "timestamp": timestamp_range,
        "category": category,
        "content": combined_content,
        "confidence_score": round(avg_confidence, 2),
        "event_count": len(events)
    }
    
    if duration:
        consolidated_event["duration"] = duration
    
    return consolidated_event


def parse_timestamp(timestamp_str):
    """Parse timestamp string to seconds for comparison."""
    if not timestamp_str:
        return 0
    
    # Handle various timestamp formats and ranges
    if '-' in timestamp_str:  # Range format like "00:00:00-00:00:04"
        start_time = timestamp_str.split('-')[0].strip()
        return parse_timestamp(start_time)
    
    if ':' not in timestamp_str:
        return 0
    
    parts = timestamp_str.split(':')
    try:
        if len(parts) == 2:  # MM:SS
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:  # HH:MM:SS
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except ValueError:
        pass
    return 0


def format_timestamp_range(start_seconds, end_seconds):
    """Format timestamp range for display."""
    def seconds_to_timestamp(seconds):
        if seconds >= 3600:  # Has hours
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:  # Minutes and seconds only
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes:02d}:{secs:02d}"
    
    if start_seconds == end_seconds:
        return seconds_to_timestamp(start_seconds)
    else:
        return f"{seconds_to_timestamp(start_seconds)}-{seconds_to_timestamp(end_seconds)}"


# Create tools
transcript_parser: BaseTool = tool(transcript_parser_func)
transcript_parser.name = "TranscriptParser"

entity_extractor: BaseTool = tool(entity_extractor_func)
entity_extractor.name = "EntityExtractor"

sentiment_analyzer: BaseTool = tool(sentiment_analyzer_func)
sentiment_analyzer.name = "SentimentAnalyzer"

content_categorizer: BaseTool = tool(content_categorizer_func)
content_categorizer.name = "ContentCategorizer"

timeline_consolidator: BaseTool = tool(timeline_consolidator_func)
timeline_consolidator.name = "TimelineConsolidator"
