import { LitElement, html, css } from 'lit'
import { customElement} from 'lit/decorators.js'
import {Task} from './api';

@customElement('vf-task-list')
export class TaskList extends LitElement {
  static get properties() {
    return {
      taskList: { type: String },
      tasks: { type: Array },
      loading: { type: Boolean },
      error: { type: String },
    };
  }

  taskList: string = 'INBOX';
  tasks: Task[] = [];
  loading: boolean = true;
  error: string | undefined;

  constructor() {
    super();
    this.taskList = 'INBOX';
    this.tasks = [];
    this.loading = true;
    this.fetchTasks();
  }

  async fetchTasks() {
    try {
      this.loading = true;
      const data = await fetch(
        `/api/tasks/?task_list=${this.taskList}`
      ).then(
        response => response.json()
      );
      this.tasks = data;
    } catch (error) {
      if (error instanceof Error) {
        this.error = error.message || 'An error occurred while fetching the task list.';
      } else {
        this.error = 'An error occurred while fetching the task list.';
      }
    } finally {
      this.loading = false;
    }
  }

  render() {
    if (this.loading) {
      return html`<div class="loading-indicator">loading</div>`;
    } else if (this.error) {
      return html`<div class="error-message">${this.error}</div>`;
    } else {
      return html`
        <h1>Tasks</h1>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            ${this.tasks.map(task => html`
              <tr>
                <td>${task.id}</td>
                <td>${task.title}</td>
                <td>${task.status}</td>
              </tr>
            `)}
          </tbody>
        </table>
      `;
    }
  }


  static styles = css`
  `;
}
