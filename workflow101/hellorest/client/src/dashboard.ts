import { LitElement, html, css } from 'lit'
import { customElement} from 'lit/decorators.js'

@customElement('vf-dashboard')
export class Dashboard extends LitElement {
  render() {
    return html`
      <div>Dashboard</div>
    `
  }

  static styles = css`
  `;
}
