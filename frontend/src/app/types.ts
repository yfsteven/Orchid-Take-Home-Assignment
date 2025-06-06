export interface CloneJob {
  id: string;
  url: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
}

export interface CloneStatus {
  id: string;
  status: 'pending' | 'initializing' | 'scraping' | 'generating' | 'completed' | 'failed';
  progress: number;
  message: string;
  html?: string;
  error?: string;
}

export interface CloneRequest {
  url: string;
} 