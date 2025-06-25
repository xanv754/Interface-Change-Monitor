"use client";

import { useRouter } from 'next/navigation';
import { PATHS } from '@/constants/paths';
import { SessionController } from "@/controllers/session";
import Image from "next/image";
import "./globals.css";


export default function Home() {
    const router = useRouter();

    const handlerLogin = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const form = e.target as HTMLFormElement;
        const username = (form.elements.namedItem('username') as HTMLInputElement).value;
        const password = (form.elements.namedItem('password') as HTMLInputElement).value;
        if (username && password) {
            const isLogged = await SessionController.login(username, password);
            if (isLogged) {
                const user = await SessionController.getUser();
                if (user && user.can_assign) router.push(PATHS.DASHBOARD_ADMIN);
                else if (user && !user.can_assign) router.push(PATHS.DASHBOARD_USER);
            }
        }
    }


  return (
    <main className="w-full min-w-fit min-h-screen bg-blue-950 h-screen flex flex-col items-center justify-center gradient">
      <form className="w-fit lg:w-3/12 p-4 bg-white rounded-md h-fit flex flex-col gap-4" onSubmit={(e) => handlerLogin(e)}>
        <div className="w-56 lg:w-full flex flex-col items-center">
          <Image src="/logo.png" alt="Logo" width={100} height={100} className="self-center" />
          <h1 className="text-4xl font-bold text-(--blue-dark) text-center">
            <span className="text-(--red)">M</span>onitor de <span className="text-(--red)">C</span>ambios de <span className="text-(--red)">I</span>nterfaces
          </h1>
        </div>
        <div className="w-full h-fit flex flex-col justify-start gap-2">
          <label htmlFor="username" className="text-md font-bold text-(--blue-dark)">Usuario</label>
          <input type="text" placeholder="Nombre de Usuario" name="username" id="username" className="w-full rounded-md border-2 border-gray-500 px-2 py-1" />
        </div>
        <div className="w-full h-fit flex flex-col justify-start gap-2">
          <label htmlFor="password" className="text-md font-bold text-(--blue-dark)">Contraseña</label>
          <input type="password" placeholder="Nombre de Usuario" name="password" id="password" className="w-full rounded-md border-2 border-gray-500 px-2 py-1" />
        </div>
        <button className="w-fit px-4 p-1 rounded-md bg-(--blue) text-white self-center hover:bg-(--blue-dark) active:bg-(--blue-bright)">Iniciar Sesión</button>
      </form>
    </main>
  );
}
