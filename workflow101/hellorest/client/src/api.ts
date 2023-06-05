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

export const ALL: Flow = {
  flow_class: 'ALL',
  title: 'All flows',
  description: '',
  start_actions: [],
  process_list: '',
  task_list: '',
  chart: '',
}
