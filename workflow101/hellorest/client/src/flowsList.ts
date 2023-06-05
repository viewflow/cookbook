import { LitElement, TemplateResult, html } from 'lit'
import { customElement, property} from 'lit/decorators.js'
import {FlowsList, Flow, ALL} from './api.ts';


@customElement('vf-flows-list')
export class FlowsListElement extends LitElement {
  @property({ type: JSON }) selected = ALL;
  @property({ type: Array }) flows: FlowsList = [];
  @property({ type: Boolean }) loading = true;
  @property({ type: String }) error: string | undefined;

  constructor() {
    super();
    this.fetchFlows();
  }

  createRenderRoot() { return this }

  async fetchFlows(): Promise<void> {
    try {
      this.loading = true;
      const response = await fetch('/api/flows/');
      if (!response.ok) {
        throw new Error('An error occurred while fetching the flow list.');
      }
      const data = await response.json();
      this.flows = data;
    } catch (error: any) {
      this.error = error.message || 'An error occurred while fetching the flow list.';
    } finally {
      this.loading = false;
    }
  }

  handleClick(event: Event) {
    const target = event.target as HTMLElement;
    const flowClass = target.getAttribute('data-flow-class');

    this.selected = this.flows.find((flow) => flow.flow_class === flowClass) || ALL

    this.dispatchEvent(new CustomEvent('link-clicked', { detail: this.selected }));
  }

  renderFlowsLinks(flow: Flow): TemplateResult {
    return html`
      <a
        href="#"
        @click="${this.handleClick}"
        data-flow-class="${flow.flow_class}"
        class="${this.selected.flow_class === flow.flow_class ? 'bg-blue-50 ':''}text-blue-500 hover:text-blue-700 hover:bg-blue-100 w-full py-2 px-4 rounded-lg text-center">
        ${flow.title}
      </a>
    `;
  }

  renderErrorMessage(): TemplateResult {
    return html`
      <div class="mt-4 text-red-500 error-message">
        ${this.error}
      </div>
    `;
  }

  renderSpin(): TemplateResult {
    return html`
      <div class="flex justify-center items-center py-4">
        <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    `
  }

  render(): TemplateResult {
    return html`
    <div class="bg-gray-800 text-white py-4">
      <h1 class="text-2xl text-center">Flows</h1>
    </div>

    <div class="py-6">
        <nav class="flex flex-col items-center mx-2">
          <a
            href="#"
            @click="${this.handleClick}"
            class="${this.selected.flow_class === ALL.flow_class ? 'bg-blue-50 ':''}text-blue-500 hover:text-blue-700 hover:bg-blue-100 w-full py-2 px-4 rounded-lg text-center">All flows</a>
          ${this.loading ? this.renderSpin() : this.flows.map((flow) => this.renderFlowsLinks(flow))}
        </nav>

        ${this.error ? this.renderErrorMessage() : ''}
    </div>
    `;
  }
}
