import { LoginController } from "../../controllers/login.controller";
import { AdminController } from "../../controllers/admin.controller";
import { userStatus } from "../../../constants/userStatus";
import type { AdminModel } from "../../models/admin";
import type { UserModel } from "../../models/user";
import { Zoom, Slide } from "react-awesome-reveal";
import { useEffect, useState } from "react";

interface Props {
    token: string;
}

export default function ContainerUsers({ token }: Props) {

    const [users, setUsers] = useState<Array<AdminModel | UserModel>>([]);
    const [error, setError] = useState<boolean>(false);
    const [isLoading, setLoading] = useState<boolean>(true);

    const enabledUserHandler = async (username: string) => {
        const status = await AdminController.allowUser(token, username);
        if (status) {
            alert("Usuario habilitado con éxito");
            location.reload();
        }
        else alert("Error al habilitar al usuario");
    }

    const disabledUserHandler = async (username: string) => {
        console.log('alo')
        const status = await AdminController.deleteUser(token, username);
        if (status) {
            alert("Usuario deshabilitado con éxito");
            location.reload();
        }
        else alert("Error al deshabilitar al usuario");
    }

    useEffect(() => {
        const getUsers = async () => {
            const allUsers = await AdminController.getAllUsers(token);
            const myuser = await LoginController.getDataUser(token);
            if ((allUsers) && (allUsers.length > 0) && (myuser)) {
                let users = allUsers.filter((user: AdminModel | UserModel) => ((user.username != myuser.username) && (user.status == userStatus.enabled)));
                setUsers(users);
            }
            else setError(true);
            setLoading(false);
        }
        getUsers();
    }, []);

    console.log(users);

    return(
        <div className="h-full w-full mt-4 bg-blue-500 rounded-t-2xl p-4">
            <div className="h-full w-full bg-gray-550 min-w-fit rounded-xl flex flex-col items-center p-4">
                <Zoom><h2 className="font-lexend font-bold text-3xl text-blue-500">Lista de Usuarios</h2></Zoom>
                <div className="h-1 rounded-full bg-blue-500 w-full mt-2"></div>
                {!isLoading && error &&
                    <div className="w-full h-full flex flex-col justify-center items-center">
                        <img src="/assets/error.png" alt="" className='w-14 py-4' />
                        <h3 className="font-lexend font-bold text-2xl text-gray-900">Error al obtener los datos de los usuarios</h3>
                    </div>
                }
                {!isLoading && !error && !users &&
                    <div className="w-full h-full flex flex-col justify-center items-center">
                        <img src="/assets/error.png" alt="" className='w-14 py-4' />
                        <h3 className="font-lexend font-bold text-2xl text-gray-900">Error al obtener los datos de los usuarios</h3>
                    </div>
                }
                {!isLoading && !error && 
                    <section className="w-full h-full flex flex-row gap-4 flex-wrap mt-1">
                        {users.length > 0 && users.map((user: (AdminModel | UserModel), index) => {
                            return(
                                <Zoom key={index}>
                                    {user.status != userStatus.pending &&
                                        <div key={index} className="bg-gray-800 h-fit min-w-80 p-4 rounded-xl">
                                            <h4 className="font-lexend text-blue-500 font-semibold">Nombre de Usuario: <span className="text-black-500">{user.username}</span></h4>
                                            <h4 className="font-lexend text-blue-500 font-semibold">Nombre: <span className="text-black-500">{user.name}</span></h4>
                                            <h4 className="font-lexend text-blue-500 font-semibold">Apellido: <span className="text-black-500">{user.name}</span></h4>
                                            <h4 className="font-lexend text-blue-500 font-semibold">Tipo de usuario: <span className="text-black-500">{user.name}</span></h4>
                                            {user.status == userStatus.enabled && <button className="font-lexend text-white bg-blue-500 px-4 py-2 transition-all duration-300 ease-in-out rounded-full mt-2 hover:bg-red-500" onClick={() => {disabledUserHandler(user.username)}}>Desactivar usuario</button>}
                                            {user.status == userStatus.disabled && <button className="font-lexend text-white bg-blue-500 px-4 py-2 transition-all duration-300 ease-in-out rounded-full mt-2 hover:bg-green-500" onClick={() => {enabledUserHandler(user.username)}}>Activar usuario</button>}
                                        </div>
                                    }
                                </Zoom>
                            );
                        })}
                        {users.length <= 0 &&
                            <div className="w-full bg-gray-700 rounded-md text-3xl font-lexend font-bold text-gray-900 flex flex-row justify-center items-center text-center max-md:py-20">
                                Sin usuarios encontrados
                            </div>
                        }
                    </section>
                }
            </div>
        </div>
    );
}