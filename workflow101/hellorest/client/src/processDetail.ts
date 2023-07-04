import { LitElement, TemplateResult, html } from 'lit'
import { customElement, property} from 'lit/decorators.js'
import { Process } from './api.ts';


@customElement('vf-process-detail')
export class ProcessDetailElement extends LitElement {
  @property({ type: JSON }) process: Process | null = null;

  createRenderRoot() { return this }

  toTitleCase(str: string) {
    return str
      .replace(/_/g, ' ')   // Replace underscores with spaces
      .replace(/\w\S*/g, (txt: string) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()); // Capitalize first letter of each word
  }

  formatValue(value: any) {
    if (!value) {
      return 'N/A';
    }

    if (typeof value === 'object') {
      return JSON.stringify(value, null, 2);
    }

    const iso8601Regex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}\+\d{2}:\d{2}$/;
    const date = (iso8601Regex.test(value)) ? new Date(value) : null;

    if (date && !isNaN(date.getTime())) {
      return date.toLocaleString();
    }

    return value;
  }

  render(): TemplateResult {
    return html`
      <div class="bg-gray-400 text-white py-4">
        <h1 class="text-2xl text-center">Process #${this.process?.id}</h1>
      </div>

      <div class="table-auto container mx-auto py-2 px-2">
        <table class="min-w-full bg-white border border-gray-200 rounded-lg">
          <tbody>
            ${Object.entries(this.process || {}).map(([key, value]) => html`
              <tr>
                <td class="border px-3 py-2 font-bold text-sm">${this.toTitleCase(key)}</td>
                <td class="border px-3 py-2 text-sm">${this.formatValue(value)}</td>
              </tr>
            `)}
          </tbody>
        </table>
      </div>
    `
  }
}
