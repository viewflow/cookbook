import { LitElement, TemplateResult, html } from 'lit'
import { customElement, property} from 'lit/decorators.js'
import { ALL, Process, Task } from './api.ts';

import './flowsList.ts';
import './flowMenu.ts';
import './flowChart.ts';
import './processList.ts';
import './processDetail.ts';
import './taskList.ts';
import './taskDetail.ts';

import './actions/index.ts';
import './hellorest/index.ts';

import './index.css';


type SelectedItem =
  | { kind: "process"; data: Process}
  | { kind: "task"; data: Task}
  | { kind: "action"; data: string}

@customElement('vf-app')
export class App extends LitElement {
  @property({ type: JSON }) selectedFlow = ALL;
  @property({ type: JSON }) selectedList = ALL.process_list;
  @property({ type: JSON }) selectedItem: SelectedItem | null = null;

  createRenderRoot() { return this }

  handleFlowChange(event: any) {
    this.selectedFlow = event.detail;
    this.selectedList = this.selectedFlow.process_list;
  }

  handleListChange(event: any) {
    this.selectedList = event.detail;
  }

  handleProcessLinkClick(event: any) {
    this.selectedItem = {kind: 'process', data: event.detail}
  }

  handleTaskLinkClick(event: any) {
    this.selectedItem = {kind: 'task', data: event.detail}
  }

  handleActionLinkClick(event: any) {
    this.selectedItem = {kind: 'action', data: event.detail}
  }

  renderDetailTab(): TemplateResult {
      switch (this.selectedItem?.kind) {
        case 'process':
          return html`<vf-process-detail class="w-3/12 bg-red-200" .process=${this.selectedItem.data}></vf-process-detail>`;
        case 'task':
          return html`<vf-task-detail class="w-3/12 bg-red-200" .task=${this.selectedItem.data}></vf-task-detail>`;
        case 'action':
          if(/\/api\/\w+\/task\/4\/approve\/\d+\/approve/.test(this.selectedItem.data)) {
            return html`<vf-task-assign class="w-3/12 bg-red-200" .task=${this.selectedItem.data}></vf-task-assign>`
          } else if(this.selectedItem.data === '/api/hellorest/task/start/') {
              return html `<vf-hellorest-start class="w-3/12 bg-red-200"></vf-hellorest-start>`;
          } else if(/\/api\/hellorest\/task\/4\/approve\/\d+/.test(this.selectedItem.data)) {
              return html `<vf-hellorest-approve class="w-3/12 bg-red-200" .task=${this.selectedItem.data}></vf-hellorest-approve>`;
          }
      }
      return html`
        <div class="w-3/12 bg-red-200">
          <div class="bg-gray-400 text-white py-4">
            <h1 class="text-2xl text-center">No active item</h1>
          </div>
        </div>
      `;
  }

  render(): TemplateResult {
    return html`
      <div class="flex min-h-screen w-screen">
        <vf-flows-list
          class="w-2/12 bg-gray-200"
          .selected=${this.selectedFlow}
          @link-clicked=${this.handleFlowChange}>
        </vf-flows-list>

        <vf-flow-menu
          class="w-2/12 bg-blue-200"
          .flow=${this.selectedFlow}
          @action-clicked=${this.handleActionLinkClick}
          @link-clicked=${this.handleListChange}>
        </vf-flow-menu>

        ${this.selectedList == this.selectedFlow.process_list ?
          html`<vf-process-list
                  class="w-5/12 bg-green-200"
                  url=${this.selectedList}
                  @link-clicked="${this.handleProcessLinkClick}">
               </vf-process-list>
          `:
          html`<vf-task-list
                  class="w-5/12 bg-yellow-200"
                  url=${this.selectedList}
                  @link-clicked="${this.handleTaskLinkClick}">
               </vf-task-list>
          `}

        ${this.renderDetailTab()}
      </div>
    `
  }
}
