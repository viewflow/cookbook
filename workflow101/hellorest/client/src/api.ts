export type FlowAction = {
  name: string;
  flow_task: string;
  title: string;
  description: string;
  url: string;
};

export type Flow = {
  flow_class: string;
  title: string;
  description: string;
  start_actions: FlowAction[];
  process_list: string;
  task_list: string;
  chart: string;
};

export type FlowsList = Flow[];

export type Process = {
  id: number;
  flow_class: string;
  url: string;
  title: string;
  description: string;
  brief: string;
  status: string;
  created: string;
  finished: null | string;
  data: object;
  artifact_object_id: null | string;
  parent_task: null | string;
  artifact_content_type: null | string;
}

export type ProcessList = Process[];

export type Action = {
  label: string;
  conditions_met: boolean;
  has_permission: boolean;
}

export type Owner = {
  email: string;
  id: number;
  username: string;
  short_name: string;
  full_name: string;
}

export type Task = {
  id: number;
  flow_task: string;
  url: string;
  title: string;
  description: string;
  brief: string;
  process_brief: string;
  actions: Action[];
  owner: Owner | null;
  flow_task_type: string;
  status: string;
  created: string;
  assigned: null | string;
  started: string;
  finished: null | string;
  token: string;
  external_task_id: null | string;
  owner_permission: null | string;
  owner_permission_obj_pk: null | number;
  data: null | any;
  artifact_object_id: null | number;
  owner_permission_content_type: null | any;
  process: Process;
  artifact_content_type: null | any;
  previous: Task[];
  leading: Task[];
}

export type TaskList = Task[];

export const ALL: Flow = {
  flow_class: 'ALL',
  title: 'All flows',
  description: '',
  start_actions: [],
  process_list: '/api/process/',
  task_list: '/api/task/',
  chart: '',
}
