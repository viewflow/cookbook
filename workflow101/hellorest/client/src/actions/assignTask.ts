import { LitElement, TemplateResult, html } from 'lit'
import { customElement, property} from 'lit/decorators.js'
import { Task } from '../api.ts';


@customElement('vf-task-assign')
export class TaskAssignElement extends LitElement {
  @property({ type: JSON }) task: Task | null = null;

  createRenderRoot() { return this }

  render(): TemplateResult {
    return html`
    `;
  }
}
