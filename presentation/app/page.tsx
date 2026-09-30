"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { PATHS } from '@/constants/paths';
import { SessionController } from "@/controllers/session";
import Image from "next/image";
import "./globals.css";


export default function Home() {
    const router = useRouter();
    const [error, setError] = useState<boolean>(false);

    const handlerLogin = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const form = e.target as HTMLFormElement;
        const username = (form.elements.namedItem('username') as HTMLInputElement).value;
        const password = (form.elements.namedItem('password') as HTMLInputElement).value;
        if (username && password) {
            const isLogged = await SessionController.login(username, password);
            if (isLogged) {
                const user = await SessionController.getInfo();
                if (user && user.can_assign) router.push(PATHS.DASHBOARD_ADMIN);
                else if (user && !user.can_assign) router.push(PATHS.DASHBOARD_USER);
            } else {
              setError(true);
            }
        }
    }


  return (
    <main className="w-full min-w-fit min-h-screen h-screen flex flex-col items-center justify-center gradient px-4">
      <form className="w-full max-w-sm p-8 bg-(--white) rounded-xl shadow-[var(--shadow-modal)] h-fit flex flex-col gap-5" onSubmit={(e) => handlerLogin(e)}>
        <div className="w-full flex flex-col items-center gap-3">
          <Image src="/logo.png" alt="Logo" width={72} height={72} className="self-center" />
          <h1 className="font-display m-0 text-xl font-semibold text-(--ink) text-center">
            Monitor de Cambios de Interfaces
          </h1>
        </div>
        <div className="w-full h-fit flex flex-col justify-start gap-2">
          <label htmlFor="username" className="text-sm font-medium text-(--ink)">Usuario</label>
          <input type="text" placeholder="Nombre de usuario" name="username" id="username" className="field" />
        </div>
        <div className="w-full h-fit flex flex-col justify-start gap-2">
          <label htmlFor="password" className="text-sm font-medium text-(--ink)">Contraseña</label>
          <input type="password" placeholder="Contraseña" name="password" id="password" className="field" />
          <span className={`text-xs text-(--red) ${error ? "visible" : "hidden"}`}>* Usuario o contraseña incorrectos</span>
        </div>
        <button className="btn btn-primary w-full mt-1">Iniciar Sesión</button>
      </form>
    </main>
  );
}
