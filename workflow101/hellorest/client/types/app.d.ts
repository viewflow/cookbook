import { Router } from '@vaadin/router';
import { LitElement } from 'lit';
import './dashboard';
import './tasklist';
export declare class App extends LitElement {
    router: Router;
    firstUpdated(): void;
    render(): import("lit-html").TemplateResult<1>;
    static styles: import("lit").CSSResult;
}
declare global {
    interface HTMLElementTagNameMap {
        'vf-rest-client': App;
    }
}
