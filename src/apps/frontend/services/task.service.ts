import APIService from 'frontend/services/api.service';
import { JsonObject } from 'frontend/types/common-types';
import { ApiResponse } from 'frontend/types';
import { Task } from 'frontend/types/task';

export default class TaskService extends APIService {
  getTasks = async (
    accountId: string,
    token: string,
  ): Promise<ApiResponse<Task[]>> => {
    const response = await this.apiClient.get<JsonObject>(
      `/accounts/${accountId}/tasks`,
      {
        headers: { Authorization: `Bearer ${token}` },
      },
    );

    const items = response.data.items as JsonObject[];
    const tasks = items.map((obj: JsonObject) => new Task(obj));

    return new ApiResponse<Task[]>(tasks);
  };

  getTask = async (
    accountId: string,
    taskId: string,
    token: string,
  ): Promise<ApiResponse<Task>> => {
    const response = await this.apiClient.get<JsonObject>(
      `/accounts/${accountId}/tasks/${taskId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );
    return new ApiResponse(new Task(response.data));
  };

  createTask = async (
    accountId: string,
    data: Partial<Task>,
    token: string,
  ): Promise<ApiResponse<Task>> => {
    const response = await this.apiClient.post<JsonObject>(
      `/accounts/${accountId}/tasks`,
      data,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );
    return new ApiResponse(new Task(response.data));
  };

  updateTask = async (
    accountId: string,
    taskId: string,
    data: Partial<Task>,
    token: string,
  ): Promise<ApiResponse<Task>> => {
    const response = await this.apiClient.patch<JsonObject>(
      `/accounts/${accountId}/tasks/${taskId}`,
      data,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );
    return new ApiResponse(new Task(response.data));
  };

  deleteTask = async (
    accountId: string,
    taskId: string,
    token: string,
  ): Promise<ApiResponse<void>> => {
    await this.apiClient.delete(`/accounts/${accountId}/tasks/${taskId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return new ApiResponse(undefined);
  };
}
