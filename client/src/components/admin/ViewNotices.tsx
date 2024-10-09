import { AdminController } from "../../controllers/admin.controller";
import { userType } from "../../../constants/userType";
import type { AdminModel } from "../../models/admin";
import type { UserModel } from "../../models/user";
import { useState, useEffect } from "react";
import { userStatus } from "../../../constants/userStatus";

interface Props {
    token: string
}

export default function ContainerNotices({ token }: Props) {

    const [usersPending, setUsersPending] = useState<any[]>([]);
    const [error, setError] = useState<boolean>(false);

    const allowUserHandler = async (username: string) => {
        const response = AdminController.allowUser(token, username);
        if (response) alert("Usuario aceptado con éxito");
        else alert("Error al aceptar al usuario");
        location.reload();
    }

    const allowChangePasswordHandler = async (username: string) => {
        const response = AdminController.allowChangePassword(token, username);
        if (response) alert("Cambio de contraseña aceptado con éxito");
        else alert("Error al aceptar el cambio de contraseña");
        location.reload();
    }

    const denyUserHandler = async (username: string) => {
        const response = AdminController.denyUser(token, username);
        if (response) alert("Usuario rechazado con éxito");
        else alert("Error al rechazar al usuario");
        location.reload();
    }

    const denyChangePasswordHandler = async (username: string) => {
        const response = AdminController.denyChangePassword(token, username);
        if (response) alert("Cambio de contraseña rechazado con éxito");
        else alert("Error al rechazar el cambio de contraseña");
        location.reload();
    }

    useEffect(() => {
        const getUsersPending = async () => {
            const users = await AdminController.getUsersPending(token);
            if (!users) setError(true);
            else setUsersPending(users);
        }
        getUsersPending();
    }, []);

    return(
        <div className="h-full w-full p-4 mt-4 bg-blue-500 rounded-t-3xl max-md:h-fit">
            <section className="h-full w-full bg-gray-550 flex flex-col gap-2 items-center py-4 px-6 rounded-2xl">
                <h2 className="font-lexend font-bold text-blue-500 text-3xl">Notificaciones</h2>
                <div className="h-1 w-full bg-blue-500 rounded-full"></div>
                {!error && usersPending.length > 0 &&
                    <div className="h-full w-full flex flex-col gap-3 bg-gray-700 p-6 rounded-lg overflow-y-auto">
                        {usersPending.map((user: (AdminModel | UserModel), index) => {
                            return(
                                <div key={index} className="w-full h-fit rounded-xl px-4 py-2 bg-gray-500">
                                    {user.status == userStatus.pending && <h2 className="font-lexend font-bold text-blue-500 text-lg"><span className="text-red-500">Notificación:</span> Solicitud de nuevo usuario</h2>}
                                    {user.status == userStatus.passwordPending && <h2 className="font-lexend font-bold text-blue-500 text-lg"><span className="text-red-500">Notificación:</span> Solicitud de Cambio de Contreseña</h2>}
                                    <h3 className="font-lexend text-blue-500 font-bold px-4">Persona: <span className="font-normal">{user.name} {user.lastname}</span></h3>
                                    {user.type == userType.admin && <h4 className="font-lexend text-blue-500 font-bold px-4">Tipo de usuario: <span className="font-normal">Administrador</span></h4>}
                                    {user.type == userType.user && <h4 className="font-lexend text-blue-500 font-bold px-4">Tipo de usuario: <span className="font-normal">Común</span></h4>}
                                    <h4 className="font-lexend text-blue-500 font-bold px-4">Nombre de usuario: <span className="font-normal">{user.username}</span></h4>
                                    {user.status == userStatus.pending && 
                                        <div className="flex flex-row gap-3 mt-2 max-md:flex-col">
                                            <button className="font-lexend font-bold text-white text-sm px-6 py-2 rounded-full bg-blue-500 transition-all duration-300 ease-in-out hover:bg-red-500" onClick={() => {denyUserHandler(user.username)}}>Denegar Usuario</button>
                                            <button className="font-lexend font-bold text-white text-sm px-6 py-2 rounded-full bg-blue-500 transition-all duration-300 ease-in-out hover:bg-green-500" onClick={() => {allowUserHandler(user.username)}}>Aceptar Usuario</button>
                                        </div>
                                    }
                                    {user.status == userStatus.passwordPending && 
                                        <div className="flex flex-row gap-3 mt-2 max-md:flex-col">
                                            <button className="font-lexend font-bold text-white text-sm px-6 py-2 rounded-full bg-blue-500 transition-all duration-300 ease-in-out hover:bg-red-500" onClick={() => {denyChangePasswordHandler(user.username)}}>Denegar Cambio</button>
                                            <button className="font-lexend font-bold text-white text-sm px-6 py-2 rounded-full bg-blue-500 transition-all duration-300 ease-in-out hover:bg-green-500" onClick={() => {allowChangePasswordHandler(user.username)}}>Aceptar Cambio</button>
                                        </div>
                                    }
                                </div>
                            )
                        })}
                    </div>
                }
                {!error && usersPending.length <= 0 &&
                    <div className="h-full w-full flex flex-col justify-center items-center bg-gray-700 rounded-lg overflow-y-auto">
                        <img src="/assets/check.png" alt="" className='w-14 py-4' />
                        <h2 className='text-gray-900 font-bold text-3xl max-sm:text-lg'>Sin Notificaciones</h2>
                    </div>
                }
                {error && 
                    <div className="h-full w-full flex flex-col justify-center items-center bg-gray-700 rounded-lg overflow-y-auto">
                        <img src="/assets/error.png" alt="" className='w-14 py-4' />
                        <h2 className='text-gray-900 font-bold text-3xl max-sm:text-lg'>Error al obtener las notificaciones</h2>
                    </div>
                }
            </section>
        </div>
    );
}