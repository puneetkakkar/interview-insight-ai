// Backend transcript analysis types matching the Pydantic schemas
export interface TranscriptInput {
  transcript_text: string;
  model?: string;
  thread_id?: string;
  user_id?: string;
  custom_categories?: string[];
}

export interface TimelineEntry {
  timestamp: string | null;
  category: string;
  content: string;
  confidence_score?: number;
}

export interface EntityExtraction {
  people: string[];
  companies: string[];
  technologies: string[];
  locations: string[];
}

export interface HighlightsLowlights {
  highlights: string[];
  lowlights: string[];
}

export interface TranscriptSummary {
  entities: EntityExtraction;
  sentiment_analysis: HighlightsLowlights;
  timeline: TimelineEntry[];
  total_duration?: string;
  key_topics: string[];
  overall_sentiment: string;
  metadata: Record<string, unknown>;
}

export interface TranscriptAnalysisResponse {
  success: boolean;
  message: string;
  data: TranscriptSummary | null;
  run_id: string | null;
}

// UI state interface
export interface InterviewSummaryState {
  transcript: string;
  summary: TranscriptSummary | null;
  isLoading: boolean;
  error: string | null;
}
