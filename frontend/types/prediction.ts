export type PredictRequest = {
  request_id: string;
  request_text: string;
  product_family: string;
  warranty_status: string;
  channel: string;
  source?: string;
};

export type PredictResponse = {
  request_id: string;
  predicted_team: string;
  confidence_score: number;
  relative_confidence: number;
  score_type: string;
  reasons: string[];
};

export type HealthResponse = {
  status: string;
  model_loaded: boolean;
};
