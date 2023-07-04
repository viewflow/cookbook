import { LitElement, TemplateResult, html } from 'lit'
import { customElement, property, query} from 'lit/decorators.js'
import { Task } from '../api.ts';


@customElement('vf-hellorest-start')
export class HelloRestStartElement extends LitElement {
  @property({ type: JSON }) task: Task | null = null;
  @property({ type: Boolean }) loading = false;
  @property({ type: String }) error: string | undefined;

  @query('form')
  private form!: HTMLFormElement;

  createRenderRoot() { return this }

  private async submitForm(e: Event) {
    e.preventDefault();

    try {
      this.loading = true;
      const formData = new FormData(this.form);
      const response = await fetch('/api/hellorest/task/start/', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('An error occurred while submitting form.');
      }

      // const data = await response.json();
      // this.tasks = data;
      // if(this.tasks) {
      //   this.dispatchEvent(new CustomEvent('link-clicked', { detail: this.tasks[0] }));
      // }

    } catch (error: any) {
      this.error = error.message || 'An error occurred while submitting form.';
    } finally {
      this.loading = false;
    }
  }

  renderSpin(): TemplateResult {
    return html`
      <div class="flex justify-center items-center py-4 animate-spin-container">
        <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    `
  }

  renderButton(): TemplateResult {
    return html`
      <button
        ?disabled=${this.loading}
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="submit">
        Submit
      </button>
    `;
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
      <div class="bg-gray-400 text-white py-4">
        <h1 class="text-2xl text-center">Start</h1>
      </div>

      <div class="container mx-2 my-2 py-2 px-2 bg-white rounded-lg shadow-md">
        <form @submit="${this.submitForm}">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="text">
              Text
            </label>
            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="text" type="text" name="text" placeholder="Enter text">
          </div>
          <div class="flex items-center justify-between">
            ${this.renderButton()}
          </div>
        </form>
        ${this.error ? this.renderErrorMessage() : ''}
      </div>
    `;
  }
}
