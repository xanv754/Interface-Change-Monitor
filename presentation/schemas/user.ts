export interface SessionSchema {
    username: string;
    name: string;
    lastname: string;
    status: string;
    role: string;
    can_assign: boolean;
    can_receive_assignment: boolean;
    view_information_global: boolean;
}

export interface UserSchema {
    username: string;
    name: string;
    lastname: string;
    status: string;
    role: string;
    created_at: string;
    updated_at: string | null;
}

export interface UserUpdateSchema {
    username: string;
    name: string;
    lastname: string;
    status: string; 
    role: string;
}