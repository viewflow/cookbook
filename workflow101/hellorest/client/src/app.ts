import { LitElement, html } from 'lit'
import { customElement, property} from 'lit/decorators.js'
import { ALL } from './api.ts';
import './flowsList.ts';
import './flowMenu.ts';

@customElement('vf-app')
export class App extends LitElement {
  @property({ type: JSON }) selectedFlow = ALL;

  createRenderRoot() { return this }

  handleFlowChange(event: any) {
    this.selectedFlow = event.detail;
  }

  render() {
    return html`
      <div class="flex h-screen w-screen">
        <vf-flows-list
          class="w-1/6 bg-gray-200"
          .selected=${this.selectedFlow}
          @link-clicked=${this.handleFlowChange}>
        </vf-flows-list>
        <vf-flow-menu
          class="w-1/6 bg-blue-200"
          .flow=${this.selectedFlow}>
        </vf-flow-menu>
        <vf-task-list></vf-task-list>
        <vf-task-form></vf-task-form>
      </div>
    `
  }
}
