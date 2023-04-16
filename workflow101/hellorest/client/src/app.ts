import { Router } from '@vaadin/router';
import { LitElement, html, css } from 'lit'
import { customElement} from 'lit/decorators.js'
import './dashboard';
import './tasklist';

@customElement('vf-rest-client')
export class App extends LitElement {

  router!: Router;

  firstUpdated() {
    if(!this.router) {
      this.router = new Router(
        this.shadowRoot?.querySelector('main'), {
        baseUrl: '/client/',
      });
      this.router.setRoutes([
        { path: '/', component: 'vf-task-list'},
        { path: '/queue', component: 'vf-task-list' },
        { path: '/archive', component: 'vf-task-list' },
        { path: '/dashboard', component: 'vf-dashboard' },
      ]);
    }
  }

  render() {
    return html`
      <div class="app-page">
        <aside class="app-page__sidebar">
          <a href="/client/">Inbox</a>
          <a href="/client/queue">Queue</a>
          <a href="/client/archive">Archive</a>
          <a href="/client/dashboard">Dashboard</a>
        </aside>
        <main class="app-page__outlet"></main>
      </div>
    `
  }

  static styles = css`
    :host {
      width: 100%;
      height: 100%;
    }

    .app-page {
      display: flex;
      flex-direction: row;
      width: 100%;
      height: 100%;
    }

    .app-page__sidebar {
      width: 250px;
      height: 100%;
      flex-shrink: 0;
      box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
      position: relative;
    }

    .app-page__sidebar>a {
      display: block;
      padding: 10px;
      text-decoration: none;
      color: #333333;
      border-left: 8px solid #877804;
      margin-bottom: 2px;
    }

    a:hover {
      background-color: #eee;
    }

    .app-page__outlet {
      flex-grow: 1
    }
  `;
}

declare global {
  interface HTMLElementTagNameMap {
    'vf-rest-client': App
  }
}
