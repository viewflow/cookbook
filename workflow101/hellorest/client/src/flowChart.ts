import { LitElement, TemplateResult, html } from 'lit'
import { customElement, property} from 'lit/decorators.js'
import { unsafeHTML } from 'lit-html/directives/unsafe-html.js';


@customElement('vf-flow-chart')
export class FlowMenuElement extends LitElement {
  createRenderRoot() { return this }

  @property({ type: String }) url = '';
  @property({ type: String }) svg = '';
  @property({ type: Boolean }) loading = true;
  @property({ type: String }) error = '';

  updated(changedProperties: any) {
    if (changedProperties.has('url')) {
      this.fetchChart();
    }
  }

  async fetchChart(): Promise<void> {
    try {
      this.loading = true;
      const response = await fetch(this.url);
      if (!response.ok) {
        throw new Error('An error occurred while fetching the flow list.');
      }
      const data = await response.text();
      this.svg = data;
    } catch (error: any) {
      this.error = error.message || 'An error occurred while fetching the flow list.';
    } finally {
      this.loading = false;
    }
  }

  renderErrorMessage(): TemplateResult {
    return html`
      <div class="mt-4 text-red-500 error-message px-2">
        ${this.error}
      </div>
    `;
  }

  render(): TemplateResult {
    return html`
      <div id="chart" class="popup">
        <a href="#" class="close">&times;</a>
        <a href="#">
          <div class="content">
            ${unsafeHTML(this.svg)}
          </div>
        </a>
      </div>
      <a href="#chart" class="chart">
        ${unsafeHTML(this.svg)}
      </a>

      ${this.error ? this.renderErrorMessage() : ''}
    `;
  }
}
