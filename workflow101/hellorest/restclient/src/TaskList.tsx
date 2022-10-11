import type { Component } from 'solid-js';
import { createResource, Show } from 'solid-js';


const fetchTasks = async (listName: string) => (
  await fetch(`/api/hellorest/task/?task_list=${listName}`)
).json();


export const TaskList: Component<any> = (props: any) => {
  const [data, { mutate, refetch }] = createResource(props.listName, fetchTasks);

  const renderTask = (task: any) => {
    return (
      <div className="task_list__task">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">#{task.process.id} {task.title}</h5>
            <div class="card-text">
              <div>{task.process_summary}</div>
              <div>{task.summary}</div>
            </div>
          </div>
          <div class="card-body task_list__actions">
            {/*task.actions.map(action => this.renderTaskAction(task, action))*/}
          </div>
        </div>
      </div>
    )
  }

  return (
    <>
      <div class="task_list">
        <Show when={!data.loading} fallback="Loading...">
          <Show when={data() && data()['results'].length} fallback={<h1>No tasks available</h1>}>
            {data().results.map((task: any) => renderTask(task))}
          </Show>
        </Show>
      </div>
      <div>
        <button class="btn btn-primary btn-action btn-circle" onClick={refetch}>&#8635;</button>
      </div>
    </>
  )
}

export const Inbox: Component = () => {
  return <TaskList listName="INBOX"/>
}

export const Queue: Component = () => {
  return <TaskList listName="QUEUE"/>
}

export const Archive: Component = () => {
  return <TaskList listName="ARCHIVE"/>
}
