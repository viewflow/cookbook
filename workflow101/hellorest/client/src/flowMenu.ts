import { LitElement, TemplateResult, html } from 'lit'
import { customElement, property} from 'lit/decorators.js'
import {FlowsList, Flow} from './api.ts';
import { ALL } from './api.ts';


@customElement('vf-flow-menu')
export class FlowMenuElement extends LitElement {
  createRenderRoot() { return this }

  @property({ type: JSON }) flow = ALL;

  render() {
    return html`
      <div class="bg-gray-600 text-white py-4">
        <h1 class="text-2xl text-center">${this.flow.title}</h1>
      </div>

      <div class="py-6">
      <nav class="flex flex-col items-center mx-2">
        <!--a href="#" class="text-blue-500 hover:text-blue-700 hover:bg-blue-100 w-full py-2 px-4 rounded-lg text-center">Dashboard</a>
        <a href="#" class="text-blue-500 hover:text-blue-700 hover:bg-blue-100 w-full py-2 px-4 rounded-lg text-center">Process list</a>
        <div class="h-4"></div-->
        <a href="#" class="bg-blue-50 text-blue-500 hover:text-blue-700 hover:bg-blue-100 w-full py-2 px-4 rounded-lg text-center">Inbox</a>
        <a href="#" class="text-blue-500 hover:text-blue-700 hover:bg-blue-100 w-full py-2 px-4 rounded-lg text-center">Queue</a>
        <a href="#" class="text-blue-500 hover:text-blue-700 hover:bg-blue-100 w-full py-2 px-4 rounded-lg text-center">Archive</a>
      </nav>
      </div>
      <div class="flex justify-center py-2">
      <button class="bg-blue-500 hover:bg-blue-700 text-white py-2 px-4 rounded-lg">Start</button>
      </div>
    `
  }
}
