"use client";
import { LoginController } from "@/controllers/login";


export default function Home() {

  const handlerLogin = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const username = (form.elements.namedItem('username') as HTMLInputElement).value;
    const password = (form.elements.namedItem('password') as HTMLInputElement).value;
    if (username && password) {
      const token = LoginController.login(username, password);
    }
  }


  return (
    <main className="w-full bg-blue-950 h-screen flex flex-col items-center justify-center">
      <form className="w-3/12 p-4 bg-white rounded-md h-fit flex flex-col gap-4" onSubmit={(e) => handlerLogin(e)}>
        <h1 className="text-4xl font-bold text-blue-900 text-center">Monitor de Cambios de Interfaces</h1>
        <div className="w-full h-fit flex flex-col justify-start gap-2">
          <label htmlFor="username" className="text-md font-bold text-blue-950">Usuario</label>
          <input type="text" placeholder="Nombre de Usuario" name="username" id="username" className="w-full rounded-md border-2 border-gray-500 px-2 py-1" />
        </div>
        <div className="w-full h-fit flex flex-col justify-start gap-2">
          <label htmlFor="password" className="text-md font-bold text-blue-950">Contraseña</label>
          <input type="password" placeholder="Nombre de Usuario" name="password" id="password" className="w-full rounded-md border-2 border-gray-500 px-2 py-1" />
        </div>
        <button className="w-fit px-4 p-1 rounded-md bg-blue-800 text-white self-center hover:bg-blue-900 active:bg-blue-700">Iniciar Sesión</button>
      </form>
    </main>
  );
}
