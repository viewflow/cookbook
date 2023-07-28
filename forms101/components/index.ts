import { FileUploadWithPreview } from 'file-upload-with-preview';


export class MyFileUploadComponent extends HTMLElement {
  upload: any;

  connectedCallback() {
    this.upload = new FileUploadWithPreview(this.getAttribute('id') || 'id');
  }

  disconnectedCallback() {
  }
}
