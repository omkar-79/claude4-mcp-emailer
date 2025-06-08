import { McpAgent } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { Hono } from 'hono'
import { cors } from 'hono/cors'


// Define our MCP agent with tools
export class MyMCP extends McpAgent {
	server = new McpServer({
		name: "Authless Calculator",
		version: "1.0.0",
	});

	async init() {
		// Simple addition tool
		this.server.tool(
			"add",
			{ a: z.number(), b: z.number() },
			async ({ a, b }) => ({
				content: [{ type: "text", text: String(a + b) }],
			})
		);

		// Calculator tool with multiple operations
		this.server.tool(
			"calculate",
			{
				operation: z.enum(["add", "subtract", "multiply", "divide"]),
				a: z.number(),
				b: z.number(),
			},
			async ({ operation, a, b }) => {
				let result: number;
				switch (operation) {
					case "add":
						result = a + b;
						break;
					case "subtract":
						result = a - b;
						break;
					case "multiply":
						result = a * b;
						break;
					case "divide":
						if (b === 0)
							return {
								content: [
									{
										type: "text",
										text: "Error: Cannot divide by zero",
									},
								],
							};
						result = a / b;
						break;
				}
				return { content: [{ type: "text", text: String(result) }] };
			}
		);
	}
}

const app = new Hono()

// Enable CORS
app.use('*', cors())

// Mock MCP server endpoint to accept CSV file uploads
app.post('/upload', async (c) => {
	const formData = await c.req.formData()
	const file = formData.get('file') as File
	if (!file) {
		return c.json({ error: 'No file provided' }, 400)
	}
	const content = await file.text()
	// Store the file content in KV (mock storage)
	const contextId = `context_${Date.now()}`
	await c.env.MCP_RESOURCES.put(contextId, content)
	return c.json({ context_id: contextId })
})

export default app