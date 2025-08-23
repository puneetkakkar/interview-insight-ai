import { env } from "@/env";
import { type NextRequest, NextResponse } from "next/server";

interface TranscriptRequest {
  transcript_text: string;
}

interface BackendResponse {
  success: boolean;
  message: string;
  data: unknown;
  run_id: string | null;
}

export async function POST(request: NextRequest) {
  try {
    const body = (await request.json()) as TranscriptRequest;

    console.log("body", body);

    // Forward request to backend API
    const backendResponse = await fetch(
      `${env.BACKEND_URL}/api/v1/transcript/analyze`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      },
    );

    const data = (await backendResponse.json()) as BackendResponse;

    // Return the response with the same status code
    return NextResponse.json(data, {
      status: backendResponse.status,
    });
  } catch (error) {
    console.error("Error forwarding request to backend:", error);
    return NextResponse.json(
      {
        success: false,
        message: "Failed to connect to backend service",
        data: null,
        run_id: null,
      },
      { status: 500 },
    );
  }
}
