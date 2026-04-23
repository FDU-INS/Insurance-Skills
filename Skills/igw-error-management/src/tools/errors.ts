import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { IgwApiClient, truncateResult, handleApiError } from "../services/api.js";

/**
 * Map tool params (user-facing) to API params (camelCase, matching portal behavior).
 * Strips undefined values so the API only receives explicitly set filters.
 */
function buildErrorFilter(params: Record<string, unknown>): Record<string, unknown> {
  const filter: Record<string, unknown> = {};

  if (params.BeginDate !== undefined) filter.beginDate = params.BeginDate;
  if (params.EndDate !== undefined) filter.endDate = params.EndDate;
  if (params.AgentId !== undefined) filter.agentId = params.AgentId;
  if (params.BranchId !== undefined) filter.branchId = params.BranchId;
  if (params.ProductId !== undefined) filter.productId = params.ProductId;
  if (params.InsuranceCompanyId !== undefined) filter.insuranceCompanyId = params.InsuranceCompanyId;
  if (params.ServiceOperationId !== undefined) filter.serviceOperationId = params.ServiceOperationId;
  if (params.NotAnalysed !== undefined) filter.notAnalysed = params.NotAnalysed;
  if (params.Solved !== undefined) filter.solved = params.Solved;
  if (params.InProgress !== undefined) filter.inProgress = params.InProgress;
  if (params.NothingToDo !== undefined) filter.nothingToDo = params.NothingToDo;
  if (params.UserMistake !== undefined) filter.userMistake = params.UserMistake;
  if (params.ConnectionError !== undefined) filter.connectionError = params.ConnectionError;
  if (params.OperationTimeout !== undefined) filter.operationTimeout = params.OperationTimeout;
  if (params.ErrorQuery !== undefined) filter.errorQuery = params.ErrorQuery;
  if (params.IncludeProducts !== undefined) filter.includeProducts = params.IncludeProducts;
  if (params.ClientChannel !== undefined) filter.clientChannel = params.ClientChannel;
  if (params.PageNumber !== undefined) filter.page = params.PageNumber;
  if (params.PageSize !== undefined) filter.pageSize = params.PageSize;
  if (params.SortColumn !== undefined) filter.sortColumn = params.SortColumn;
  if (params.SortDescending !== undefined) filter.sortDescending = params.SortDescending;

  return filter;
}

const commonFilterSchema = {
  BeginDate: z
    .string()
    .optional()
    .describe("Start date filter (ISO 8601, e.g. 2024-01-01 or 2024-01-01T00:00:00)"),
  EndDate: z
    .string()
    .optional()
    .describe("End date filter (ISO 8601)"),
  AgentId: z.number().optional().describe("Filter by specific agent ID"),
  BranchId: z.number().optional().describe("Branch ID filter"),
  ProductId: z.number().optional().describe("Product ID filter"),
  InsuranceCompanyId: z
    .number()
    .optional()
    .describe("Insurance company ID filter"),
  ServiceOperationId: z
    .number()
    .optional()
    .describe("Service operation ID filter (1=Teklif/Proposal, 2=Poliçe/Policy)"),
  NotAnalysed: z.boolean().optional().describe("Include not-analysed errors (default: true in portal)"),
  Solved: z.boolean().optional().describe("Include solved errors"),
  InProgress: z.boolean().optional().describe("Include in-progress errors"),
  NothingToDo: z.boolean().optional().describe("Include nothing-to-do errors (default: false in portal)"),
  UserMistake: z.boolean().optional().describe("Include user mistake errors"),
  ConnectionError: z
    .boolean()
    .optional()
    .describe("Include connection errors"),
  OperationTimeout: z
    .boolean()
    .optional()
    .describe("Include operation timeout errors"),
  ErrorQuery: z
    .string()
    .optional()
    .describe("Free text search within error messages. Useful for finding specific error patterns."),
  IncludeProducts: z
    .boolean()
    .optional()
    .describe("Whether to include product details (default: true)"),
  ClientChannel: z
    .string()
    .optional()
    .describe("Filter by client channel"),
};

export function registerErrorTools(server: McpServer, api: IgwApiClient): void {
  server.tool(
    "igw_errors_list",
    `List IGW errors with filters. Returns grouped errors with counts.

Response includes:
- ErrorCategories: Summary counts per ServiceOperationID (1=Teklif, 2=Poliçe) with status breakdowns (NotPinned, Solved, InProgress, UserMistake, ConnectionError, OperationTimeout)
- Errors: Array of grouped errors with AgentName, ProductName, ErrorExplanation, GroupCount, LastErrorDate, InsuranceCompanyName, AnalyzeStatus, ErrorExplanationHash

Sorting: Use SortColumn (e.g. "GroupCount", "AgentName", "LastErrorDate") with SortDescending to order results.
Text search: Use ErrorQuery to search within error messages.
Pagination: Use PageNumber and PageSize (default 10).

AnalyzeStatus values: 0=NotAnalysed, 1=InProgress, 2=Solved, 3=NothingToDo, 4=UserMistake, 5=ConnectionError`,
    {
      ...commonFilterSchema,
      PageNumber: z.number().optional().describe("Page number (default 1)"),
      PageSize: z.number().optional().describe("Items per page (default 10)"),
      SortColumn: z
        .string()
        .optional()
        .describe("Sort by column: 'GroupCount', 'AgentName', 'LastErrorDate', 'InsuranceCompanyName', 'ProductName'"),
      SortDescending: z
        .boolean()
        .optional()
        .describe("Sort descending (default false). Set true to get highest counts first."),
    },
    async (params) => {
      try {
        const filter = buildErrorFilter(params);
        const result = await api.listErrors(filter);
        return { content: [{ type: "text", text: truncateResult(result) }] };
      } catch (error) {
        return {
          content: [{ type: "text", text: handleApiError(error) }],
          isError: true,
        };
      }
    }
  );

  server.tool(
    "igw_errors_summary",
    `Get error summary/statistics without the full error list. Returns only ErrorCategories with counts per ServiceOperationID.

Lightweight alternative to igw_errors_list when you only need counts.
Response format: { "1": { "NotPinned": N, "Solved": N, "InProgress": N, ... }, "2": { ... } }
Keys: 1=Teklif (Proposal), 2=Poliçe (Policy)`,
    {
      ...commonFilterSchema,
    },
    async (params) => {
      try {
        const filter = buildErrorFilter({ ...params, PageSize: 1 });
        const result = await api.listErrors(filter) as any;
        const summary = {
          ErrorCategories: result?.ErrorCategories ?? {},
          _totalErrorGroups: result?.Errors?.length ?? 0,
        };
        return { content: [{ type: "text", text: JSON.stringify(summary, null, 2) }] };
      } catch (error) {
        return {
          content: [{ type: "text", text: handleApiError(error) }],
          isError: true,
        };
      }
    }
  );

  server.tool(
    "igw_errors_operations",
    `Get service operations with their error statistics. Shows which operations (Teklif, Poliçe, etc.) produce errors and their counts.`,
    {
      ...commonFilterSchema,
    },
    async (params) => {
      try {
        const filter = buildErrorFilter(params);
        const result = await api.getErrorOperations(filter);
        return { content: [{ type: "text", text: truncateResult(result) }] };
      } catch (error) {
        return {
          content: [{ type: "text", text: handleApiError(error) }],
          isError: true,
        };
      }
    }
  );

  server.tool(
    "igw_errors_logs",
    `Get detailed error log entries with request/response data. Use for investigating specific errors.

Note: This endpoint may require specific filters to return results (e.g. date range + company/product).`,
    {
      ...commonFilterSchema,
      PageNumber: z.number().optional().describe("Page number"),
      PageSize: z.number().optional().describe("Page size"),
    },
    async (params) => {
      try {
        const filter = buildErrorFilter(params);
        const result = await api.getErrorLogs(filter);
        return { content: [{ type: "text", text: truncateResult(result) }] };
      } catch (error) {
        return {
          content: [{ type: "text", text: handleApiError(error) }],
          isError: true,
        };
      }
    }
  );

  server.tool(
    "igw_errors_log_detail",
    `Get full request/response data for a specific error log by ID. Shows the complete XML/JSON payload that was sent to the insurance company and the response received.`,
    {
      id: z.number().describe("Error log ID (from FailedOperationId or error list)"),
    },
    async ({ id }) => {
      try {
        const result = await api.getErrorLogDetail(id);
        return { content: [{ type: "text", text: truncateResult(result) }] };
      } catch (error) {
        return {
          content: [{ type: "text", text: handleApiError(error) }],
          isError: true,
        };
      }
    }
  );

  server.tool(
    "igw_errors_analyze",
    `Analyze a specific error by ID. Returns analysis details including possible root causes, affected products, and resolution suggestions.`,
    {
      id: z.number().describe("Error ID to analyze"),
    },
    async ({ id }) => {
      try {
        const result = await api.analyzeError(id);
        return { content: [{ type: "text", text: truncateResult(result) }] };
      } catch (error) {
        return {
          content: [{ type: "text", text: handleApiError(error) }],
          isError: true,
        };
      }
    }
  );
}
