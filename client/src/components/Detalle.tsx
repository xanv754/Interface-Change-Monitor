import { ElementController } from '../controllers/element.controller';
import { assignmentStatus } from '../../constants/assigmentStatus';
import { UserController } from '../controllers/user.controller';
import { userType } from '../../constants/userType';
import styles from '../styles/spinner.module.css';
import type { AdminModel } from '../models/admin';
import type { Element } from '../models/element';
import type { UserModel } from '../models/user';
import { useEffect, useState } from 'react';
import Footer from '../layouts/Footer';

interface Props {
    token: string;
    idElement: string;
    user: (UserModel | AdminModel);
}

export default function ContainerDetalle({ token, idElement, user }: Props){

    const [element, setElement] = useState<Element>(null);
    const [isLoading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<boolean>(false);

    const updateStatusHandler = async () => {
        const selectStatus = document.getElementById("status") as HTMLSelectElement;
        const status = selectStatus.value.toString();
        if (status) {
            const update_status = await UserController.updateAssignment(token, user.username, idElement, status);
            if (update_status) {
                alert("Estatus actualizado!");
                location.href = "/home";
            } else {
                alert("Ha ocurrido un error al actualizar el estatus. Por favor, intente de nuevo");
            }
        }
    }

    const backHandler = () => {
        if (user) {
            if (user.type == userType.admin) location.href = "/admin/history";
            else location.href = "/home";
        }
    }

    useEffect(() => {
        const getElement = async () => {
            const dataElement = await ElementController.getElement(token, idElement);
            if (!dataElement) setError(true);
            else setElement(dataElement);
            setLoading(false);
        }
        getElement();
    }, []);

    return(
        <div className='min-h-fit h-80vh w-full px-4 max-md:h-fit'>
            <section className='min-h-fit h-full w-full rounded-t-3xl shadow-md max-md:h-fit'>
                {isLoading && 
                    <div className='flex h-80vh w-full bg-blue-500 rounded-t-3xl flex-col justify-center items-center'>
                        <div className={styles.spinner}></div>
                    </div>
                }
                {!isLoading && error &&
                    <div className='flex h-full w-full flex-col bg-gray-100 rounded-t-3xl justify-center items-center'>
                        <img src="/assets/error.png" alt="" className='w-14 py-4' />
                        <h2 className='text-red-500 font-bold text-xl max-sm:text-lg'>Error ha ocurrido un error al obtener la información</h2>
                        <h4 className='text-black-100 font-bold text-lg max-sm:text-lg'>Refresque la página e intente de nuevo</h4>
                    </div>
                }
                {!isLoading && !error &&
                    <div className='flex h-full w-full flex-col bg-gray-500 rounded-t-3xl p-6'> 
                        <section className='h-fit w-full flex flex-row flex-wrap gap-4 items-center py-2 max-sm:flex-col'>
                            <div className='flex flex-row items-center w-30 min-w-fit max-md:flex-col max-md:w-full'>
                                <label className='font-lexend font-semibold text-white bg-blue-500 md:rounded-l-md px-8 py-2 max-md:rounded-t-md max-md:w-full max-md:text-center'>IP</label>
                                <div className='w-full min-w-fit font-lexend font-semibold text-blue-500 bg-white md:rounded-r-md px-6 py-2 max-md:rounded-b-md max-md:text-center'>{element.current.ip}</div>
                            </div>
                            <div className='flex flex-row items-center w-50 min-w-fit max-md:flex-col max-md:w-full'>
                                <label className='font-lexend font-semibold text-white bg-blue-500 md:rounded-l-md px-6 py-2 max-md:rounded-t-md max-md:w-full max-md:text-center'>Comunidad</label>
                                <div className='w-full min-w-fit font-lexend font-semibold text-blue-500 bg-white md:rounded-r-md px-6 py-2 max-md:rounded-b-md max-md:text-center'>{element.current.community}</div>
                            </div>
                            {user.type == userType.user && element.assignment.status == assignmentStatus.pending &&
                                <>
                                    <div className='flex flex-row items-center max-md:flex-col max-md:w-full'>
                                        <label htmlFor="status" className='font-lexend font-semibold text-white bg-blue-500 md:rounded-l-md px-6 py-2 max-md:rounded-t-md max-md:w-full'>Estatus</label>
                                        <select name="status" id="status" className='font-lexend font-normal text-blue-500 bg-white md:rounded-r-md px-4 py-2 max-md:rounded-b-md max-md:w-full'>
                                            <option value="">----</option>
                                            <option value="1">{assignmentStatus.rediscovered}</option>
                                            <option value="2">{assignmentStatus.reviewed}</option>
                                        </select>
                                    </div>
                                    <button className='h-fit font-lexend font-bold text-white bg-blue-500 px-6 py-2 rounded-3xl transition-all duration-300 ease-in-out hover:bg-green-500 max-md:w-full' onClick={() => {updateStatusHandler()}}>Guardar</button>
                                </>                        
                            }
                            {user.type == userType.user && element.assignment.status != assignmentStatus.default && element.assignment.status != assignmentStatus.pending &&
                                <div className='flex flex-row items-center max-md:flex-col max-md:w-full'>
                                    <label className='font-lexend font-semibold text-white bg-green-500 md:rounded-l-md px-6 py-2 max-md:rounded-t-md max-md:w-full'>Estatus</label>
                                    <div className='font-lexend font-normal text-blue-500 bg-white md:rounded-r-md px-4 py-2 max-md:rounded-b-md max-md:w-full'>{element.assignment.status}</div>
                                </div>
                            }
                            {user.type == userType.admin &&
                                <div className='flex flex-row items-center max-md:flex-col max-md:w-full'>
                                    {element.assignment.status != assignmentStatus.pending && element.assignment.status != assignmentStatus.default &&  
                                        <label className='font-lexend font-semibold text-white bg-green-500 md:rounded-l-md px-6 py-2 max-md:rounded-t-md max-md:w-full'>Estatus</label>
                                    }
                                    {element.assignment.status == assignmentStatus.pending &&
                                        <label className='font-lexend font-semibold text-white bg-red-500 md:rounded-l-md px-6 py-2 max-md:rounded-t-md max-md:w-full'>Estatus</label>
                                    }
                                    {element.assignment.status == assignmentStatus.default &&
                                        <label className='font-lexend font-semibold text-white bg-red-500 md:rounded-l-md px-6 py-2 max-md:rounded-t-md max-md:w-full'>Estatus</label>
                                    }
                                    <div className='font-lexend font-normal text-blue-500 bg-white md:rounded-r-md px-4 py-2 max-md:rounded-b-md max-md:w-full'>{element.assignment.status}</div>
                                </div>
                            }
                        </section>                        
                        <section className='w-full h-full py-2 px-10 flex flex-row gap-6 max-md:h-fit max-md:flex-col'>
                            <div className='w-50 h-full flex flex-col flex-nowrap justify-center items-center gap-3 py-4 max-md:w-full'>
                                <h3 className='font-lexend font-bold text-blue-500 text-2xl'>Datos Anteriores</h3>
                                {element.old.ifName == element.current.ifName &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-blue-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Nombre</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.old.ifName}</div>
                                    </div>                                    
                                }
                                {element.old.ifName != element.current.ifName &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-red-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Nombre</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.old.ifName}</div>
                                    </div>                                    
                                }
                                {element.old.ifAlias == element.current.ifAlias &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-blue-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Alias</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.old.ifAlias}</div>
                                    </div>
                                }
                                {element.old.ifAlias != element.current.ifAlias &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-red-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Alias</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.old.ifAlias}</div>
                                    </div>
                                }
                                {element.old.ifDescr == element.current.ifDescr && 
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-blue-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Descripción</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.old.ifDescr}</div>
                                    </div>
                                }
                                {element.old.ifDescr != element.current.ifDescr && 
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-red-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Descripción</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.old.ifDescr}</div>
                                    </div>
                                }
                                {element.old.ifHighSpeed == element.current.ifHighSpeed &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-blue-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Capacidad</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.old.ifHighSpeed}</div>
                                    </div>
                                }
                                {element.old.ifHighSpeed != element.current.ifHighSpeed &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-red-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Capacidad</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.old.ifHighSpeed}</div>
                                    </div>
                                }
                                {element.old.ifOperStatus == element.current.ifOperStatus &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 font-lexend font-bold text-white bg-blue-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Estatus Operativo</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.old.ifOperStatus}</div>
                                    </div>                                    
                                }
                                {element.old.ifOperStatus != element.current.ifOperStatus &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 font-lexend font-bold text-white bg-red-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Estatus Operativo</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.old.ifOperStatus}</div>
                                    </div>                                    
                                }
                                {element.old.ifAdminStatus == element.current.ifAdminStatus &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 font-lexend font-bold text-white bg-blue-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Estatus Administrativo</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 flex flex-row items-center max-sm:rounded-b-md'>{element.old.ifAdminStatus}</div>
                                    </div>
                                }
                                {element.old.ifAdminStatus != element.current.ifAdminStatus &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 font-lexend font-bold text-white bg-red-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Estatus Administrativo</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.old.ifAdminStatus}</div>
                                    </div>
                                }
                            </div>
                            <div className='w-50 h-full flex flex-col flex-nowrap justify-center items-center gap-3 py-4 max-md:w-full'>
                                <h3 className='font-lexend font-bold text-blue-500 text-2xl'>Datos Actuales</h3>
                                {element.old.ifName == element.current.ifName &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-blue-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Nombre</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.current.ifName}</div>
                                    </div>                                    
                                }
                                {element.old.ifName != element.current.ifName &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-red-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Nombre</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.current.ifName}</div>
                                    </div>                                    
                                }
                                {element.old.ifAlias == element.current.ifAlias &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-blue-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Alias</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.current.ifAlias}</div>
                                    </div>
                                }
                                {element.old.ifAlias != element.current.ifAlias &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-red-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Alias</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.current.ifAlias}</div>
                                    </div>
                                }
                                {element.old.ifDescr == element.current.ifDescr && 
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-blue-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Descripción</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.current.ifDescr}</div>
                                    </div>
                                }
                                {element.old.ifDescr != element.current.ifDescr && 
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-red-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Descripción</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.current.ifDescr}</div>
                                    </div>
                                }
                                {element.old.ifHighSpeed == element.current.ifHighSpeed &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-blue-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Capacidad</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.current.ifHighSpeed}</div>
                                    </div>
                                }
                                {element.old.ifHighSpeed != element.current.ifHighSpeed &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 min-w-fit font-lexend font-bold text-white bg-red-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Capacidad</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.current.ifHighSpeed}</div>
                                    </div>
                                }
                                {element.old.ifOperStatus == element.current.ifOperStatus &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 font-lexend font-bold text-white bg-blue-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Estatus Operativo</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.current.ifOperStatus}</div>
                                    </div>                                    
                                }
                                {element.old.ifOperStatus != element.current.ifOperStatus &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 font-lexend font-bold text-white bg-red-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Estatus Operativo</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.current.ifOperStatus}</div>
                                    </div>                                    
                                }
                                {element.old.ifAdminStatus == element.current.ifAdminStatus &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 font-lexend font-bold text-white bg-blue-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Estatus Administrativo</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.current.ifAdminStatus}</div>
                                    </div>
                                }
                                {element.old.ifAdminStatus != element.current.ifAdminStatus &&
                                    <div className='flex flex-row justify-center w-full max-sm:flex-col'>
                                        <label className='w-50 font-lexend font-bold text-white bg-red-500 md:rounded-l-md sm:rounded-l-md px-4 py-2 max-sm:w-full max-sm:rounded-t-md'>Estatus Administrativo</label>
                                        <div className='w-full max-h-fit font-lexend font-bold text-blue-500 bg-white overflow-hidden overflow-x-auto md:rounded-r-md px-4 py-2 max-sm:rounded-b-md'>{element.current.ifAdminStatus}</div>
                                    </div>
                                }
                            </div>
                        </section>
                        <section className='w-full h-fit flex flex-row justify-center'>
                            <button className='font-lexend font-bold text-white bg-blue-500 text-lg rounded-full px-6 py-2 transition-all duration-300 ease-in-out hover:bg-blue-800' onClick={() => {backHandler()}}>Regresar</button>
                        </section>
                    </div>
                }
            </section>
            <Footer></Footer>
        </div>
    )
}