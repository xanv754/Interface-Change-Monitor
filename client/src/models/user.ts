import type { InterfaceModel } from "./interface";

export interface UserModel {
    id: string;
    username: string;
    name: string;
    lastname: string;
    type: string;
    assigned: InterfaceModel[];
    status: string;
}