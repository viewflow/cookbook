import { LitElement, TemplateResult, html } from 'lit'
import { customElement, property} from 'lit/decorators.js'
import { ALL, FlowAction } from './api.ts';


@customElement('vf-flow-menu')
export class FlowMenuElement extends LitElement {
  createRenderRoot() { return this }

  @property({ type: JSON }) flow = ALL;
  @property({ type: String }) selected = '';

  handleLinkClick(event: Event) {
    const target = event.target as HTMLElement;
    this.selected = target.getAttribute('data-list-url') || '';
    this.dispatchEvent(new CustomEvent('link-clicked', { detail: this.selected }));
  }

  handleActionClick(event: Event) {
    const target = event.target as HTMLElement;
    const action_url = target.getAttribute('data-action-url') || '';
    this.dispatchEvent(new CustomEvent('action-clicked', { detail: action_url }));
  }

  updated(changedProperties: any) {
    if (changedProperties.has('flow')) {
      this.selected = this.flow.process_list;
    }
  }

  renderLink(linkText: string, linkUrl: string) : TemplateResult {
    const itemCss = 'text-blue-500 hover:text-blue-700 hover:bg-blue-100 w-full py-2 px-4 rounded-lg text-center';

    return html`
      <a
        href="#"
        class="${this.selected==linkUrl?"bg-blue-50 ": ""} ${itemCss}"
        data-list-url="${linkUrl}"
        @click="${this.handleLinkClick}"
      >${linkText}</a>
    `;
  }

  renderStartAction(action: FlowAction): TemplateResult {
    return html`
      <div class="flex justify-center py-2">
        <button
          data-action-url="${action.url}"
          @click="${this.handleActionClick}"
          class="bg-blue-500 hover:bg-blue-700 text-white py-2 px-4 rounded-lg">${action.title}</button>
      </div>
    `;
  }

  render() : TemplateResult {
    return html`
      <div class="bg-gray-600 text-white py-4">
        <h1 class="text-2xl text-center">${this.flow.title}</h1>

      </div>

      <div class="py-2">
        <nav class="flex flex-col items-center mx-2">
          ${this.renderLink("Process", this.flow.process_list)}
          <div class="h-4"></div>
          <h4 class="text-sm font-bold">Tasks</h4>
          ${this.renderLink("Inbox", this.flow.task_list+"?task_list=INBOX")}
          ${this.renderLink("Queue", this.flow.task_list+"?task_list=QUEUE")}
          ${this.renderLink("Archive", this.flow.task_list+"?task_list=ARCHIVE")}
        </nav>
      </div>

      <div class="flex py-2 mx-2">
        ${this.flow.chart?html`<vf-flow-chart url="${this.flow.chart}">`:''}
      </div>

      ${this.flow.start_actions.map((action) => this.renderStartAction(action))}    `
  }
}
