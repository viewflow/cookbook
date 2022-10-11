import type { Component } from 'solid-js';
import { ErrorBoundary } from "solid-js";
import { Routes, Route, Link } from "solid-app-router"
import {Dashboard} from './Dashboard';
import { Start } from './Start';
import {Inbox, Queue, Archive} from './TaskList';

const App: Component = () => {
  return (
    <div className="app-page">
      <nav className="app-page__sidebar">
        <p>Tasks</p>
        <ul class="nav flex-column">
          <li class="nav-item">
            <Link href="/inbox/" class="nav-link">Inbox</Link>
          </li>
          <li class="nav-item">
            <Link href="/queue/" class="nav-link">Queue</Link>
          </li>
          <li class="nav-item">
            <Link href="/archive/" class="nav-link">Archive</Link>
          </li>
        </ul>
        <p>Dashboard</p>
        <ul class="nav flex-column">
          <li class="nav-item">
            <Link href="/dashboard/" class="nav-link">Hello REST</Link>
          </li>
        </ul>
      </nav>
      <div className="app-page__outlet">
        <ErrorBoundary fallback={(err, reset) => <div onClick={reset}>Error: {err.toString()}</div>}>
          <Routes>
            <Route path="/inbox/" element={<Inbox/>} />
            <Route path="/queue/" element={<Queue/>} />
            <Route path="/archive/" element={<Archive/>} />
            <Route path="/dashboard/*" element={<Dashboard/>} />
          </Routes>
        </ErrorBoundary>
      </div>
    </div>
  )
};

export default App;
