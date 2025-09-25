import { JsonObject } from './common-types';

export class Task {
  id: string;
  account_id: string;
  title: string;
  description: string;
  active: boolean;
  created_at: string;
  updated_at: string;

  constructor(json: JsonObject) {
    this.id = String(json.id ?? json._id ?? '');
    this.account_id = String(json.account_id ?? '');
    this.title = String(json.title ?? '');
    this.description = String(json.description ?? '');
    this.created_at = String(json.created_at ?? '');
    this.updated_at = String(json.updated_at ?? '');
    this.active = Boolean(json.active ?? true);
  }
}
