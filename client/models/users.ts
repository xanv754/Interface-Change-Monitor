export interface UserModel {
    username: string;
    password: string | null;
    name: string;
    lastname: string;
    status: string;
    role: string;
    created_at: string;
    updated_at: string | null;
}

export interface UserLoggedModel {
    username: string;
    name: string;
    lastname: string;
    status: string;
    role: string;
    can_assign: boolean;
    can_receive_assignment: boolean;
    view_information_global: boolean;
}