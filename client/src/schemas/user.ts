export interface UserSchema {
    username: string;
    name: string;
    lastname: string;
    password: string | null;
    profile: string;
    account: string;
    createdAt: string;
}

export interface UserInfoSchema {
    username: string;
    name: string;
    lastname: string;
    profile: string;
}