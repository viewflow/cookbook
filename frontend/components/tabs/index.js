export default class MyTabs extends HTMLElement {
  connectedCallback() {
    this._tabs = M.Tabs.init(this.querySelector('.tabs'));
  }

  disconnectedCallback() {
    this._tabs.destroy();
  }
}