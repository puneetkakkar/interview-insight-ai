// "use client";

// import { useState } from "react";
// import { Button } from "@/components/ui/button";
// import { Card } from "@/components/ui/card";
// import { Textarea } from "@/components/ui/textarea";
// import { Alert } from "@/components/ui/alert";
// import type { TranscriptInput, TranscriptAnalysisResponse, InterviewSummaryState } from "@/types/interview";

// export default function InterviewSummary() {
//   const [state, setState] = useState<InterviewSummaryState>({
//     transcript: "",
//     summary: null,
//     isLoading: false,
//     error: null,
//   });

//   const handleSubmit = async () => {
//     if (!state.transcript.trim()) {
//       setState(prev => ({ ...prev, error: "Please enter an interview transcript" }));
//       return;
//     }

//     setState(prev => ({ ...prev, isLoading: true, error: null }));

//     try {
//       const requestData: TranscriptInput = {
//         transcript_text: state.transcript,
//       };

//       const response = await fetch("/api/v1/transcript/analyze", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify(requestData),
//       });

//       const data: unknown = await response.json();
      
//       if (!response.ok) {
//         const errorData = data as { message?: string };
//         throw new Error(errorData.message ?? `HTTP error! status: ${response.status}`);
//       }
      
//       const analysisData = data as TranscriptAnalysisResponse;

//       if (analysisData.success && analysisData.data) {
//         setState(prev => ({
//           ...prev,
//           summary: analysisData.data,
//           isLoading: false,
//         }));
//       } else {
//         setState(prev => ({
//           ...prev,
//           error: analysisData.message ?? "Failed to generate summary",
//           isLoading: false,
//         }));
//       }
//     } catch {
//       setState(prev => ({
//         ...prev,
//         error: "Network error. Please check your connection and try again.",
//         isLoading: false,
//       }));
//     }
//   };

//   const handleClear = () => {
//     setState({
//       transcript: "",
//       summary: null,
//       isLoading: false,
//       error: null,
//     });
//   };

//   const handleRetry = () => {
//     setState(prev => ({ ...prev, error: null }));
//     void handleSubmit();
//   };

//   return (
//     <div className="w-full max-w-4xl mx-auto space-y-8">
//       <div className="text-center space-y-4">
//         <h1 className="text-3xl md:text-4xl font-bold tracking-tight">
//           Interview Summary Tool
//         </h1>
//         <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
//           Paste your interview transcript below and get an intelligent summary 
//           with key insights, highlights, and actionable takeaways.
//         </p>
//       </div>

//       <Card className="p-6 md:p-8 space-y-6">
//         <div className="space-y-3">
//           <label htmlFor="transcript" className="block text-sm font-semibold">
//             Interview Transcript
//           </label>
//           <Textarea
//             id="transcript"
//             placeholder="Paste your interview transcript here... The more detailed the transcript, the better the summary will be."
//             value={state.transcript}
//             onChange={(e) => setState(prev => ({ ...prev, transcript: e.target.value, error: null }))}
//             className="min-h-48 text-sm leading-relaxed resize-y"
//             disabled={state.isLoading}
//           />
//           <div className="flex justify-between items-center text-xs text-muted-foreground">
//             <span>{state.transcript.length} characters</span>
//             <span>Recommended: 500+ characters for best results</span>
//           </div>
//         </div>

//         <div className="flex flex-col sm:flex-row gap-3 sm:justify-between sm:items-center">
//           <div className="flex gap-3">
//             <Button
//               onClick={handleSubmit}
//               disabled={state.isLoading || !state.transcript.trim()}
//               size="lg"
//               className="flex-1 sm:flex-none"
//             >
//               {state.isLoading ? (
//                 <>
//                   <div className="animate-spin size-4 border-2 border-white/20 border-t-white rounded-full" />
//                   Generating Summary...
//                 </>
//               ) : (
//                 "Generate Summary"
//               )}
//             </Button>
//             {(state.transcript || state.summary) && (
//               <Button
//                 onClick={handleClear}
//                 variant="outline"
//                 size="lg"
//                 disabled={state.isLoading}
//               >
//                 Clear All
//               </Button>
//             )}
//           </div>
//         </div>

//         {state.error && (
//           <Alert variant="destructive" className="flex justify-between items-start">
//             <div className="flex-1">
//               <strong className="text-sm font-medium">Error</strong>
//               <p className="text-sm mt-1">{state.error}</p>
//             </div>
//             <Button
//               onClick={handleRetry}
//               variant="outline"
//               size="sm"
//               className="ml-3 shrink-0"
//             >
//               Retry
//             </Button>
//           </Alert>
//         )}

//         {state.isLoading && (
//           <Card className="p-6 border-dashed">
//             <div className="space-y-4">
//               <div className="flex items-center gap-3">
//                 <div className="animate-spin size-5 border-2 border-primary/20 border-t-primary rounded-full" />
//                 <span className="text-sm font-medium">Analyzing your interview transcript...</span>
//               </div>
//               <div className="space-y-3">
//                 <div className="h-4 bg-muted/50 rounded animate-pulse" />
//                 <div className="h-4 bg-muted/50 rounded animate-pulse w-4/5" />
//                 <div className="h-4 bg-muted/50 rounded animate-pulse w-3/5" />
//               </div>
//             </div>
//           </Card>
//         )}

//         {state.summary && !state.isLoading && (
//           <div className="space-y-6">
//             <div className="flex items-center justify-between">
//               <h3 className="text-lg font-semibold">Interview Analysis</h3>
//               <Button
//                 onClick={() => void navigator.clipboard.writeText(JSON.stringify(state.summary, null, 2))}
//                 variant="outline"
//                 size="sm"
//               >
//                 Copy Full Data
//               </Button>
//             </div>

//             {/* Overall Summary */}
//             <Card className="p-6">
//               <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
//                 <div className="text-center">
//                   <div className="text-2xl font-bold text-primary">{state.summary.overall_sentiment}</div>
//                   <div className="text-sm text-muted-foreground">Overall Sentiment</div>
//                 </div>
//                 {state.summary.total_duration && (
//                   <div className="text-center">
//                     <div className="text-2xl font-bold text-primary">{state.summary.total_duration}</div>
//                     <div className="text-sm text-muted-foreground">Duration</div>
//                   </div>
//                 )}
//                 <div className="text-center">
//                   <div className="text-2xl font-bold text-primary">{state.summary.timeline.length}</div>
//                   <div className="text-sm text-muted-foreground">Timeline Events</div>
//                 </div>
//               </div>
              
//               {state.summary.key_topics.length > 0 && (
//                 <div>
//                   <h4 className="font-semibold mb-2">Key Topics</h4>
//                   <div className="flex flex-wrap gap-2">
//                     {state.summary.key_topics.map((topic, index) => (
//                       <span key={index} className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm">
//                         {topic}
//                       </span>
//                     ))}
//                   </div>
//                 </div>
//               )}
//             </Card>

//             {/* Timeline */}
//             {state.summary.timeline.length > 0 && (
//               <Card className="p-6">
//                 <h4 className="font-semibold mb-4">Interview Timeline</h4>
//                 <div className="space-y-4">
//                   {state.summary.timeline.map((entry, index) => (
//                     <div key={index} className="border-l-2 border-primary/20 pl-4 relative">
//                       <div className="absolute -left-2 top-2 w-3 h-3 bg-primary/60 rounded-full"></div>
//                       <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 mb-2">
//                         <div className="flex items-center gap-2">
//                           {entry.timestamp && (
//                             <span className="text-sm font-mono text-muted-foreground bg-muted px-2 py-1 rounded">
//                               {entry.timestamp}
//                             </span>
//                           )}
//                           <span className="text-sm capitalize px-2 py-1 bg-primary/10 text-primary rounded">
//                             {entry.category.replace(/_/g, ' ')}
//                           </span>
//                         </div>
//                         {entry.confidence_score && (
//                           <span className="text-xs text-muted-foreground">
//                             Confidence: {Math.round(entry.confidence_score * 100)}%
//                           </span>
//                         )}
//                       </div>
//                       <p className="text-sm">{entry.content}</p>
//                     </div>
//                   ))}
//                 </div>
//               </Card>
//             )}

//             {/* Sentiment Analysis */}
//             {(state.summary.sentiment_analysis.highlights.length > 0 || state.summary.sentiment_analysis.lowlights.length > 0) && (
//               <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
//                 {state.summary.sentiment_analysis.highlights.length > 0 && (
//                   <Card className="p-6">
//                     <h4 className="font-semibold mb-4 text-green-700 dark:text-green-400">
//                       ✓ Highlights
//                     </h4>
//                     <ul className="space-y-3">
//                       {state.summary.sentiment_analysis.highlights.map((highlight, index) => (
//                         <li key={index} className="text-sm flex items-start gap-2">
//                           <span className="text-green-500 mt-1">•</span>
//                           <span>{highlight}</span>
//                         </li>
//                       ))}
//                     </ul>
//                   </Card>
//                 )}

//                 {state.summary.sentiment_analysis.lowlights.length > 0 && (
//                   <Card className="p-6">
//                     <h4 className="font-semibold mb-4 text-orange-700 dark:text-orange-400">
//                       ⚠ Areas for Improvement
//                     </h4>
//                     <ul className="space-y-3">
//                       {state.summary.sentiment_analysis.lowlights.map((lowlight, index) => (
//                         <li key={index} className="text-sm flex items-start gap-2">
//                           <span className="text-orange-500 mt-1">•</span>
//                           <span>{lowlight}</span>
//                         </li>
//                       ))}
//                     </ul>
//                   </Card>
//                 )}
//               </div>
//             )}

//             {/* Entities */}
//             {(state.summary.entities.people.length > 0 || 
//               state.summary.entities.companies.length > 0 || 
//               state.summary.entities.technologies.length > 0 || 
//               state.summary.entities.locations.length > 0) && (
//               <Card className="p-6">
//                 <h4 className="font-semibold mb-4">Extracted Entities</h4>
//                 <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
//                   {state.summary.entities.people.length > 0 && (
//                     <div>
//                       <h5 className="text-sm font-medium text-muted-foreground mb-2">People</h5>
//                       <div className="space-y-1">
//                         {state.summary.entities.people.map((person, index) => (
//                           <div key={index} className="text-sm bg-blue-50 dark:bg-blue-950/30 text-blue-700 dark:text-blue-300 px-2 py-1 rounded">
//                             {person}
//                           </div>
//                         ))}
//                       </div>
//                     </div>
//                   )}

//                   {state.summary.entities.companies.length > 0 && (
//                     <div>
//                       <h5 className="text-sm font-medium text-muted-foreground mb-2">Companies</h5>
//                       <div className="space-y-1">
//                         {state.summary.entities.companies.map((company, index) => (
//                           <div key={index} className="text-sm bg-purple-50 dark:bg-purple-950/30 text-purple-700 dark:text-purple-300 px-2 py-1 rounded">
//                             {company}
//                           </div>
//                         ))}
//                       </div>
//                     </div>
//                   )}

//                   {state.summary.entities.technologies.length > 0 && (
//                     <div>
//                       <h5 className="text-sm font-medium text-muted-foreground mb-2">Technologies</h5>
//                       <div className="space-y-1">
//                         {state.summary.entities.technologies.map((tech, index) => (
//                           <div key={index} className="text-sm bg-green-50 dark:bg-green-950/30 text-green-700 dark:text-green-300 px-2 py-1 rounded">
//                             {tech}
//                           </div>
//                         ))}
//                       </div>
//                     </div>
//                   )}

//                   {state.summary.entities.locations.length > 0 && (
//                     <div>
//                       <h5 className="text-sm font-medium text-muted-foreground mb-2">Locations</h5>
//                       <div className="space-y-1">
//                         {state.summary.entities.locations.map((location, index) => (
//                           <div key={index} className="text-sm bg-orange-50 dark:bg-orange-950/30 text-orange-700 dark:text-orange-300 px-2 py-1 rounded">
//                             {location}
//                           </div>
//                         ))}
//                       </div>
//                     </div>
//                   )}
//                 </div>
//               </Card>
//             )}
//           </div>
//         )}
//       </Card>

//       {state.summary && (
//         <div className="text-center text-xs text-muted-foreground">
//           <p>Summary generated using AI. Please review for accuracy.</p>
//         </div>
//       )}
//     </div>
//   );
// }