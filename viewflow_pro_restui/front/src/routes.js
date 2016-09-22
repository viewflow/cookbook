import React from 'react';
import { IndexRoute, Route }  from 'react-router';

import App from './App';
import InboxPage from './components/pages/inbox';
import QueuePage from './components/pages/queue';
import ArchivePage from './components/pages/archive';

export default (
  <Route component={App} path='/'>
    <IndexRoute component={InboxPage} />
    <Route component={QueuePage} path='queue' />
    <Route component={ArchivePage} path='archive' />
  </Route>
);
