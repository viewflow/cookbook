import type { Component } from 'solid-js';
import { createResource } from 'solid-js';
import { Routes, Route, Link, Outlet   } from "solid-app-router"
import { Start } from './Start';
import { Approve } from './Approve';
import { Assign } from './Assign';

// serve index html


const FlowGraph: Component = () => {
  const defaultSvg = `
  <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
       width="24px" height="30px" viewBox="0 0 24 30" style="enable-background:new 0 0 50 50;" xml:space="preserve">
    <rect x="0" y="10" width="4" height="10" fill="#333" opacity="0.2">
      <animate attributeName="opacity" attributeType="XML" values="0.2; 1; .2" begin="0s" dur="0.6s" repeatCount="indefinite" />
      <animate attributeName="height" attributeType="XML" values="10; 20; 10" begin="0s" dur="0.6s" repeatCount="indefinite" />
      <animate attributeName="y" attributeType="XML" values="10; 5; 10" begin="0s" dur="0.6s" repeatCount="indefinite" />
    </rect>
    <rect x="8" y="10" width="4" height="10" fill="#333"  opacity="0.2">
      <animate attributeName="opacity" attributeType="XML" values="0.2; 1; .2" begin="0.15s" dur="0.6s" repeatCount="indefinite" />
      <animate attributeName="height" attributeType="XML" values="10; 20; 10" begin="0.15s" dur="0.6s" repeatCount="indefinite" />
      <animate attributeName="y" attributeType="XML" values="10; 5; 10" begin="0.15s" dur="0.6s" repeatCount="indefinite" />
    </rect>
    <rect x="16" y="10" width="4" height="10" fill="#333"  opacity="0.2">
      <animate attributeName="opacity" attributeType="XML" values="0.2; 1; .2" begin="0.3s" dur="0.6s" repeatCount="indefinite" />
      <animate attributeName="height" attributeType="XML" values="10; 20; 10" begin="0.3s" dur="0.6s" repeatCount="indefinite" />
      <animate attributeName="y" attributeType="XML" values="10; 5; 10" begin="0.3s" dur="0.6s" repeatCount="indefinite" />
    </rect>
  </svg>`

  const [chart] = createResource(
    async () => (await fetch(`/api/hellorest/chart/`)).text()
  );

  return (
    <div  innerHTML={ chart.loading ? defaultSvg : chart() }></div>
  )
}

export const Dashboard: Component = () => {
  return (
    <div className="dashboard">
      <Routes>
        <Route path='/hellorest/start' element={<Start/>}/>
        <Route path='/hellorest/:process_id/approve/:task_id/assign/' element={<Assign/>}/>
        <Route path='/hellorest/:process_id/approve/:task_id/' element={<Approve/>}/>
      </Routes>
      <div className="dashboard__column">
        <div className="dashboard__title">Start</div>
        <div className="dashboard__content">
          <div class="card">
            <div class="card-body">
              <p class="card-title">This process demonstrates hello world approval request flow.</p>
              <FlowGraph/>
              <Link class="btn btn-primary btn-sm" href="/dashboard/hellorest/start/">Start</Link>
            </div>
          </div>
        </div>
      </div>

      <div className="dashboard__column">
        <div className="dashboard__title">Approve</div>
      </div>

      <div className="dashboard__column">
        <div className="dashboard__title">Send</div>
      </div>

      <div className="dashboard__column">
        <div className="dashboard__title">Complete</div>
      </div>

    </div>
  )
}
