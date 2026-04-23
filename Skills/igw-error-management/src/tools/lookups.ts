import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { IgwApiClient, truncateResult, handleApiError } from "../services/api.js";

export function registerLookupTools(
  server: McpServer,
  api: IgwApiClient
): void {
  server.tool(
    "igw_products_search",
    `Search IGW products by name. Returns product list with IDs that can be used in error filter parameters (ProductId).

Example products: "Allianz Sigorta Kapsamlı Kasko", "Bereket Sigorta Trafik", "Doğa Sigorta Tamamlayıcı Sağlık".
Each product has an ID, name, branch, and associated insurance company.`,
    {
      query: z.string().optional().describe("Search query for product name (e.g. 'Kasko', 'Trafik', 'Allianz')"),
      page: z.number().optional().describe("Page number (default 1)"),
      pageSize: z.number().optional().describe("Page size (default 20)"),
    },
    async ({ query, page, pageSize }) => {
      try {
        const result = await api.searchProducts(query, page, pageSize);
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
    "igw_insurance_companies",
    `List all insurance companies available to the current user. Returns company IDs and names for use in error filters (InsuranceCompanyId).

Common companies: Allianz (45), Zurich (18), Doğa Sigorta (43), Bereket (57), Türkiye Sigorta (116), Sompo (61), Quick (110), Katılım Emeklilik (105), Ankara Sigorta (37).`,
    {},
    async () => {
      try {
        const result = await api.getMyInsuranceCompanies();
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
