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