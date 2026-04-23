export interface IgwAuthConfig {
  baseUrl: string;
  username: string;
  password: string;
  webApiKey: string;
}

export interface IgwTokenResponse {
  Token: string;
  RefreshToken: string;
  Expiration: string;
}

export interface IgwErrorFilter {
  beginDate?: string;
  endDate?: string;
  agentId?: number;
  branchId?: number;
  productId?: number;
  insuranceCompanyId?: number;
  serviceOperationId?: number;
  notAnalysed?: boolean;
  solved?: boolean;
  inProgress?: boolean;
  nothingToDo?: boolean;
  userMistake?: boolean;
  connectionError?: boolean;
  operationTimeout?: boolean;
  errorQuery?: string;
  includeProducts?: boolean;
  clientChannel?: string;
  page?: number;
  pageSize?: number;
  sortColumn?: string;
  sortDescending?: boolean;
}

export interface IgwErrorItem {
  AgentId: number;
  AgentName: string;
  ProductId: number;
  ProductName: string;
  ErrorExplanation: string;
  GroupCount: number;
  LastErrorDate: string;
  InsuranceCompanyID: number;
  InsuranceCompanyName: string;
  ProductBranchName: string;
  ErrorExplanationHash: string;
  PatternText: string | null;
  ErrorPatternId: number | null;
  FailedOperationId: string;
  AnalyzeStatus: number | null;
  ClientChannel: string;
  ServiceOperationID: number;
}

export interface IgwErrorCategories {
  [serviceOperationId: string]: {
    NotPinned: number;
    Solved: number;
    InProgress: number;
    NothingToDo: number;
    UserMistake: number;
    ConnectionError: number;
    OperationTimeout: number;
  };
}

export interface IgwErrorListResponse {
  ErrorCategories: IgwErrorCategories;
  Errors: IgwErrorItem[];
}

export interface IgwProductSearchParams {
  query?: string;
  page?: number;
  pageSize?: number;
}

export interface IgwPinErrorRequest {
  errorId: number;
  isPinned: boolean;
}

export interface IgwSendErrorReportRequest {
  errorId: number;
  description: string;
}

export interface IgwUpdateStatusRequest {
  errorExplanationHash: string;
  analyzeStatus: number;
  serviceOperationId?: number;
}
