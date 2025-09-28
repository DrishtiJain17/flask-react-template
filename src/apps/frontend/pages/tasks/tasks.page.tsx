import React, { useCallback, useEffect, useState } from 'react';

import { Button, Input, FormControl } from 'frontend/components';
import { useAccountContext } from 'frontend/contexts/account.provider';
import TaskService from 'frontend/services/task.service';
import { getAccessTokenFromStorage } from 'frontend/utils/storage-util';

import { ButtonType, ButtonKind } from 'frontend/types/button';
import { Task } from 'frontend/types/task';

const TasksPage: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const { accountDetails } = useAccountContext();
  const accessToken = getAccessTokenFromStorage();
  const token = accessToken?.token;
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');

  const startEditing = (task: Task) => {
    setEditingTaskId(task.id);
    setEditTitle(task.title);
    setEditDescription(task.description);
  };

  const fetchTasks = useCallback(async () => {
    if (!accountDetails?.id || !token) return;

    setLoading(true);
    try {
      const response = await new TaskService().getTasks(
        accountDetails.id,
        token,
      );
      if (response.data) {
        setTasks(response.data);
      }
    } catch (err) {
    } finally {
      setLoading(false);
    }
  }, [accountDetails?.id, token]);

  const createNewTask = async () => {
    if (!title.trim() || !accountDetails?.id || !token) return;
    try {
      const response = await new TaskService().createTask(
        accountDetails.id,
        { title, description },
        token,
      );
      if (response.data) {
        setTasks([response.data, ...tasks]);
        setTitle('');
        setDescription('');
      }
    } catch (err) {
    }
  };

  const deleteTask = async (taskId: string) => {
    if (!accountDetails?.id || !token) return;
    try {
      await new TaskService().deleteTask(accountDetails.id, taskId, token);
      setTasks(tasks.filter((t) => t.id !== taskId));
    } catch (err) {
    }
  };
  const cancelEditing = () => {
    setEditingTaskId(null);
    setEditTitle('');
    setEditDescription('');
  };
  const updateTask = async () => {
    if (!accountDetails?.id || !token || !editingTaskId) return;
    try {
      const response = await new TaskService().updateTask(
        accountDetails.id,
        editingTaskId,
        { title: editTitle, description: editDescription },
        token,
      );
      if (response.data) {
        const updatedTask = response.data;
        setTasks(tasks.map((t) => (t.id === editingTaskId ? updatedTask : t)));
        cancelEditing();
      }
    } catch (err) {
    }
  };

  useEffect(() => {
    if (accountDetails?.id && token) {
      void fetchTasks();
    }
  }, [accountDetails?.id, token, fetchTasks]);

  return (
    <div className="p-4 space-y-6">
      <h2 className="text-xl font-bold">Tasks</h2>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          void createNewTask();
        }}
        className="space-y-4"
      >
        <FormControl label="Title">
          <Input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Task title"
          />
        </FormControl>

        <FormControl label="Description">
          <Input
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Task description"
          />
        </FormControl>

        <Button type={ButtonType.SUBMIT} disabled={loading}>
          Add Task
        </Button>
      </form>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul className="space-y-2">
          {tasks.map((task) => (
            <li
              key={task.id}
              className="flex items-center justify-between border p-2 rounded"
            >
              {editingTaskId === task.id ? (
                <div className="flex-1 space-y-2">
                  <Input
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    placeholder="Edit title"
                  />
                  <Input
                    value={editDescription}
                    onChange={(e) => setEditDescription(e.target.value)}
                    placeholder="Edit description"
                  />
                  <div className="flex space-x-2 mt-2">
                    <Button type={ButtonType.SUBMIT} onClick={() => void updateTask()}>
                      Save
                    </Button>
                    <Button
                      type={ButtonType.SUBMIT}
                      kind={ButtonKind.SECONDARY}
                      onClick={cancelEditing}
                    >
                      Cancel
                    </Button>
                  </div>
                </div>
              ) : (
                <>
                  <div>
                    <p className="font-semibold">{task.title}</p>
                    <p className="text-sm text-gray-500">{task.description}</p>
                  </div>
                  <div className="flex space-x-2">
                    <Button
                      type={ButtonType.SUBMIT}
                      kind={ButtonKind.SECONDARY}
                      onClick={() => startEditing(task)}
                    >
                      Edit
                    </Button>
                    <Button
                      type={ButtonType.SUBMIT}
                      kind={ButtonKind.SECONDARY}
                      onClick={() => void deleteTask(task.id)}
                    >
                      Delete
                    </Button>
                  </div>
                </>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TasksPage;
