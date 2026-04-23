#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { IgwApiClient } from "./services/api.js";
import { IgwAuthConfig } from "./types.js";
import { DEFAULT_IGW_BASE_URL } from "./constants.js";
import { registerErrorTools } from "./tools/errors.js";
import { registerErrorActionTools } from "./tools/error-actions.js";
import { registerReportTools } from "./tools/reports.js";
import { registerLookupTools } from "./tools/lookups.js";

function getRequiredEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    console.error(`Missing required environment variable: ${name}`);
    process.exit(1);
  }
  return value;
}

const config: IgwAuthConfig = {
  baseUrl: process.env.IGW_BASE_URL || DEFAULT_IGW_BASE_URL,
  username: getRequiredEnv("IGW_USERNAME"),
  password: getRequiredEnv("IGW_PASSWORD"),
  webApiKey: getRequiredEnv("IGW_WEB_API_KEY"),
};

const api = new IgwApiClient(config);

const server = new McpServer({
  name: "igw-error-management",
  version: "1.0.0",
});

registerErrorTools(server, api);
registerErrorActionTools(server, api);
registerReportTools(server, api);
registerLookupTools(server, api);

const transport = new StdioServerTransport();
await server.connect(transport);
