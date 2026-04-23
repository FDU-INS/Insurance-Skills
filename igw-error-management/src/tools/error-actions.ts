import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { IgwApiClient, truncateResult, handleApiError } from "../services/api.js";

export function registerErrorActionTools(
  server: McpServer,
  api: IgwApiClient
): void {
  server.tool(
    "igw_errors_pin",
    `Pin or unpin an error for tracking. Pinned errors are highlighted in the error list for easy follow-up.`,
    {
      errorId: z.number().describe("Error ID to pin/unpin"),
      isPinned: z.boolean().describe("true to pin, false to unpin"),
    },
    async (params) => {
      try {
        const result = await api.pinError(params);
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
    "igw_errors_update_status",
    `Update the analysis status of an error. Use this to mark errors as solved, in-progress, user mistake, etc.

AnalyzeStatus values:
  0 = Not Analysed (Analiz Edilmedi)
  1 = In Progress (İnceleniyor)
  2 = Solved (Çözüldü)
  3 = Nothing To Do (Şirket Kuralı / Önlenemez Hata)
  4 = User Mistake (Kullanıcı Hatası)
  5 = Connection Error (Servis Bağlantı Hatası)
  6 = Operation Timeout (Zaman Aşımı)`,
    {
      errorExplanationHash: z
        .string()
        .describe("ErrorExplanationHash of the error group to update (from igw_errors_list response)"),
      analyzeStatus: z
        .number()
        .describe("New status: 0=NotAnalysed, 1=InProgress, 2=Solved, 3=NothingToDo, 4=UserMistake, 5=ConnectionError, 6=OperationTimeout"),
      serviceOperationId: z
        .number()
        .optional()
        .describe("Service operation ID (1=Teklif, 2=Poliçe). Required for scoping the update."),
    },
    async (params) => {
      try {
        const result = await api.updateErrorStatus(params);
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
    "igw_errors_send_report",
    `Send an error report to the relevant team. Include a description explaining the issue and what you've found during analysis.`,
    {
      errorId: z.number().describe("Error ID to report"),
      description: z.string().describe("Description/notes for the error report"),
    },
    async (params) => {
      try {
        const result = await api.sendErrorReport(params);
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
    "igw_errors_send_bug_report",
    `Send a bug report by reference number to the InsurGateway team. Use when you identify a genuine bug in the gateway integration.`,
    {
      referenceNo: z
        .string()
        .describe("Error reference number (e.g. IGW-12345)"),
    },
    async ({ referenceNo }) => {
      try {
        const result = await api.sendBugReport(referenceNo);
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
