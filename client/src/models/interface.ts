import type { AssignmentModel } from "./assignment";

export interface InterfaceModel {
    idElement: string;
    ip: string;
    community: string;
    assignment: AssignmentModel;
}