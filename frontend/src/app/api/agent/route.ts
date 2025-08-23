import { env } from "@/env";
import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

interface AgentQueryRequest {
  agent_name?: string;
  message: string;
  model?: string;
  thread_id?: string;
  user_id?: string;
  agent_config: {
    temperature: number;
  };
}

export async function GET() {
  try {
    const response = await fetch(`${env.BACKEND_URL}/api/v1/agent`);
    const data: unknown = await response.json();

    if (
      data &&
      typeof data === "object" &&
      "success" in data &&
      data.success &&
      "data" in data
    ) {
      return NextResponse.json(data);
    } else {
      return NextResponse.json(
        {
          success: false,
          error: { message: "Invalid response format from backend" },
        },
        { status: 500 },
      );
    }
  } catch {
    return NextResponse.json(
      { success: false, error: { message: "Failed to fetch agents" } },
      { status: 500 },
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body: unknown = await request.json();

    if (
      !body ||
      typeof body !== "object" ||
      !("message" in body) ||
      typeof (body as Record<string, unknown>).message !== "string"
    ) {
      return NextResponse.json(
        { success: false, error: { message: "Invalid request body" } },
        { status: 400 },
      );
    }

    const { message, agent_config, agent_name } =
      body as unknown as AgentQueryRequest;

    const response = await fetch(
      `${env.BACKEND_URL}/api/v1/agent/${agent_name}/invoke`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message, agent_config }),
      },
    );

    const data: unknown = await response.json();

    if (
      data &&
      typeof data === "object" &&
      "success" in data &&
      data.success &&
      "data" in data
    ) {
      return NextResponse.json(data);
    } else {
      return NextResponse.json(
        {
          success: false,
          error: { message: "Invalid response format from backend" },
        },
        { status: 500 },
      );
    }
  } catch {
    return NextResponse.json(
      { success: false, error: { message: "Failed to process request" } },
      { status: 500 },
    );
  }
}
