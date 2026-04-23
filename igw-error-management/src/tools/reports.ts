import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { IgwApiClient, truncateResult, handleApiError } from "../services/api.js";

const reportFilterSchema = {
  BeginDate: z
    .string()
    .optional()
    .describe("Start date filter (ISO 8601, e.g. 2024-01-01)"),
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
    .describe("Service operation ID filter (1=Teklif, 2=Poliçe)"),
};

function buildReportFilter(params: Record<string, unknown>): Record<string, unknown> {
  const filter: Record<string, unknown> = {};
  if (params.BeginDate !== undefined) filter.beginDate = params.BeginDate;
  if (params.EndDate !== undefined) filter.endDate = params.EndDate;
  if (params.AgentId !== undefined) filter.agentId = params.AgentId;
  if (params.BranchId !== undefined) filter.branchId = params.BranchId;
  if (params.ProductId !== undefined) filter.productId = params.ProductId;
  if (params.InsuranceCompanyId !== undefined) filter.insuranceCompanyId = params.InsuranceCompanyId;
  if (params.ServiceOperationId !== undefined) filter.serviceOperationId = params.ServiceOperationId;
  return filter;
}

export function registerReportTools(server: McpServer, api: IgwApiClient): void {
  server.tool(
    "igw_errors_success_rate",
    `Get overall error success/failure rates. Returns total operations, successful operations, failed operations, and success percentage.

Breaks down by: Genel (Overall), Teklifler (Proposals), Poliçeler (Policies).
Use date range to see trends over time.`,
    {
      ...reportFilterSchema,
    },
    async (params) => {
      try {
        const filter = buildReportFilter(params);
        const result = await api.getErrorReport(filter);
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
    "igw_errors_report_by_branch",
    `Get error report broken down by branch (Kasko, Trafik, Tamamlayıcı Sağlık, etc.). Shows total/successful/failed per branch with success rates.`,
    {
      ...reportFilterSchema,
    },
    async (params) => {
      try {
        const filter = buildReportFilter(params);
        const result = await api.getErrorReportByBranch(filter);
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
    "igw_errors_report_by_company",
    `Get error report broken down by insurance company (Allianz, Zurich, Doğa, Bereket, etc.). Shows total/successful/failed per company with success rates.`,
    {
      ...reportFilterSchema,
    },
    async (params) => {
      try {
        const filter = buildReportFilter(params);
        const result = await api.getErrorReportByCompany(filter);
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
    "igw_errors_report_by_agent",
    `Get error report broken down by agent/acente. Shows total/successful/failed per agent with success rates.`,
    {
      ...reportFilterSchema,
    },
    async (params) => {
      try {
        const filter = buildReportFilter(params);
        const result = await api.getErrorReportByAgent(filter);
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
