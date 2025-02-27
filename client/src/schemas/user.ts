import { ConfigurationResponseSchema } from "./configuration";

export interface UserLogginResponseSchema {
    username: string;
    name: string;
    lastname: string;
    profile: string;
    account: string;
    createdAt: string;
    configuration: ConfigurationResponseSchema;
}

export interface UserResponseSchema {
    username: string;
    name: string;
    lastname: string;
    profile: string;
    account: string;
    createdAt: string;
}

export interface UserShortInfoResponseSchema {
    username: string;
    name: string;
    lastname: string;
    profile: string;
}

export interface UserUpdateInfoRequestSchema {
    name: string;
    lastname: string;
}

export interface UserUpdatePasswordRequestSchema {
    password: string;
}

export interface UserUpdateProfileRequestSchema {
    username: string;
    profile: string;
}

export interface UserUpdateAccountRequestSchema {
    username: string;
    account: string;
}