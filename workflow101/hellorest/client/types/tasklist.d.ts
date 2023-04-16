import { LitElement } from 'lit';
import { Task } from './api';
export declare class TaskList extends LitElement {
    static get properties(): {
        taskList: {
            type: StringConstructor;
        };
        tasks: {
            type: ArrayConstructor;
        };
        loading: {
            type: BooleanConstructor;
        };
        error: {
            type: StringConstructor;
        };
    };
    taskList: string;
    tasks: Task[];
    loading: boolean;
    error: string | undefined;
    constructor();
    fetchTasks(): Promise<void>;
    render(): import("lit-html").TemplateResult<1>;
    static styles: import("lit").CSSResult;
}
