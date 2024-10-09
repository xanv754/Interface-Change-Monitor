import { AdminController } from "../../controllers/admin.controller";
import type { Element } from "../../models/element";
import type { UserModel } from "../../models/user";

interface Props {
    token: string;
    users: UserModel[];
}

function selectAll() {
    const allInputs = document.querySelectorAll('input');
    const allInput = document.getElementById('all') as HTMLInputElement;
    const status = allInput.checked;
    allInputs.forEach(input => {
        if (status) input.checked = true;
        else input.checked = false;
    });
    if (status) allInput.checked = true;
    else allInput.checked = false;
}

export default function ContainerAssign({ token, users}: Props) {

    const autoAssignmentHandler = async () => {
        let assignUsers: string[] = [];
        const allInputs = document.querySelectorAll('input');
        allInputs.forEach(input => {
            if (input.id == 'all') return;
            if (input.checked) assignUsers.push(input.id);
        });
        if ((assignUsers) && (assignUsers.length > 0)) {
            const status = await AdminController.autoAssignment(token, assignUsers);
            if (status) {
                alert('Se ha realizado la asignación automática de interfaces a los usuarios');
                location.href = '/admin';
            } else {
                alert('Error al realizar la asignación automática. Por favor, intente de nuevo');
                location.reload();
            }
        }
    }

    return(
        <div className="h-full w-full mt-4 bg-blue-500 rounded-t-2xl p-4">
            <div className="h-full w-full bg-white min-w-fit rounded-xl flex flex-col items-center p-4">
                <section className="w-full flex flex-col items-center">
                    <h2 className="font-lexend text-blue-500 text-3xl font-bold text-center">Asignación Automática de Interfaces</h2>
                    <div className="w-full h-1 bg-blue-500 rounded-full mt-1"></div>
                    <small className="font-lexend text-red-500 text-sm max-md:text-justify">* Nota: La asignación automática divide el total de interfaces entre los usuarios disponibles para asignar. No tiene preferencias, ni condiciones especiales. No se permite la reasignación.</small>
                </section>
                <section className="h-fit w-fit flex flex-col items-center py-2">
                    <h3 className="font-lexend text-blue-500 text-2xl font-bold text-center">Seleccione los usuarios a asignar</h3>
                </section>
                {users.length > 0 && 
                    <div className="w-full h-full flex flex-col items-center justify-between overflow-y-auto">
                        <section className="h-fit w-50 flex flex-row flex-wrap justify-center gap-7 py-4 max-md:w-full">
                            <div className="w-fit h-fit py-2 flex flex-row items-center gap-3 max-md:flex-col">
                                <label htmlFor="all" className="font-lexend font-normal text-blue-500 text-lg">Todos</label>
                                <input id="all" type="checkbox" className="h-5 w-5 bg-white" onClick={() => {selectAll()}} />
                            </div>
                            {users.map((user: UserModel, index) => {
                                return(
                                    <div key={index} className="w-fit h-fit py-2 flex flex-row items-center gap-3 max-md:flex-col">
                                        <label htmlFor={user.username} className="font-lexend font-normal text-blue-500 text-lg">{user.name} {user.lastname}</label>
                                        <input id={user.username} type="checkbox" className="h-5 w-5 bg-white" />
                                    </div>
                                );
                            })}
                        </section>
                        <section className="w-full h-fit flex flex-row justify-center gap-4 max-md:flex-col">
                            <button className="font-lexend text-white bg-blue-500 transition-all duration-300 ease-out hover:bg-red-500 px-6 py-2 w-fit rounded-full max-md:w-full" onClick={() => {location.href = '/admin'}}>Cancelar</button>
                            <button className="font-lexend text-white bg-blue-500 transition-all duration-300 ease-out hover:bg-green-500 px-6 py-2 w-fit rounded-full max-md:w-full" onClick={() => {autoAssignmentHandler()}}>Asignar</button>
                        </section>
                        
                    </div>
                }
                {users.length <= 0 && 
                    <div className="w-full h-full flex flex-col items-center justify-center overflow-y-auto bg-gray-500 rounded-lg">
                        <h1 className="font-lexend text-3xl font-bol text-gray-900 text-center">No existen usuarios para asignar</h1>
                    </div>
                }
            </div>
        </div>
    );
}