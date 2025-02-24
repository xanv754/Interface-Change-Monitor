import { ConfigurationSchema } from "./configuration";

export interface UserSchema {
    username: string;
    name: string;
    lastname: string;
    password: string | null;
    profile: string;
    account: string;
    createdAt: string;
}

export interface UserUpdateSchema {
    name: string;
    lastname: string;
}

export interface UserResponseSchema {
    username: string;
    name: string;
    lastname: string;
    profile: string;
    account: string;
    createdAt: string;
    configuration: ConfigurationSchema;
}

export interface UserInfoSchema {
    username: string;
    name: string;
    lastname: string;
    profile: string;
}

export interface UserUpdateDataBodySchema {
    name: string;
    lastname: string;
}

export interface UserUpdatePasswordBodySchema {
    password: string;
}

export interface UserProfileBodySchema {
    username: string;
    profile: string;
}

export interface UserAccountBodySchema {
    username: string;
    account: string;
}