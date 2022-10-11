import type { Component } from 'solid-js';
import { createEffect } from "solid-js";
import { TextInput } from './TextInput';

declare global {
  interface Window {
      bootstrap:any;
  }
}

export const Start: Component = () => {
  let modalEl: any;

  createEffect(() => {
    const bsModal = new window.bootstrap.Modal(modalEl);

    modalEl.addEventListener('hide.bs.modal', () => {
      window.history.back();
    })

    bsModal.show();
  });

  return (
    <div class="modal" tabindex="-1" ref={modalEl}>
      <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
              <div class="modal-title">Send message to the world</div>
            </div>
          <div class="modal-body">
            <div class="Alert" color="danger"></div>
            <form class="row g-3">
              <TextInput name="text" label="Message"/>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-primary">Start</button>
          </div>
        </div>
      </div>
    </div>
  );
}
