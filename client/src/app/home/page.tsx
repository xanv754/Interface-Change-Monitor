'use client';

import { UserController } from "@/controllers/user";
import { Token } from "@utils/token";
import { UserSchema } from "@schemas/user";
import { useEffect, useState } from "react";

export default function HomeView() {
    const [user, setUser] = useState<UserSchema | null>(null);

    const handlerSaveUser = async () => {
        sessionStorage.removeItem('user');
        const token = Token.getToken();
        if (!token) return;
        const user = await UserController.myInfo(token);
        setUser(user);
    };

    useEffect(() => {
        handlerSaveUser();
    }, []);

    useEffect(() => {
        if (user) {
            const data = {
                username: user.username,
                name: user.name,
                lastname: user.lastname,
                profile: user.profile,
            }
            sessionStorage.setItem('user', JSON.stringify(data));
        }
    }, [user]);

    return (
        <main className="w-full h-full">
            {user && 
                <div>Bienvenido, {user.name}</div>
            }
        </main>
    );
}