import { AdminController } from '../../controllers/admin.controller';
import type { Element } from '../../models/element';
import type { UserModel } from '../../models/user';
import { useEffect, useState } from 'react';
import { Zoom } from 'react-awesome-reveal';

interface Props {
    token: string;
    elements: Element[];
    users: UserModel[];
}

function filterData(elements: Element[], filter: string): Element[] {
    let elementsFilter: Element[] = [];

    elements.map((element: Element) => {
        if ((filter == 'ifName') && (element.old.ifName != element.current.ifName)) elementsFilter.push(element);
        else if ((filter == 'ifAlias') && (element.old.ifAlias != element.current.ifAlias)) elementsFilter.push(element);
        else if ((filter == 'ifHighSpeed') && (element.old.ifHighSpeed != element.current.ifHighSpeed)) elementsFilter.push(element);
        else if ((filter == 'ifOperStatus') && (element.old.ifOperStatus != element.current.ifOperStatus)) elementsFilter.push(element);
        else if ((filter == 'ifAdminStatus') && (element.old.ifAdminStatus != element.current.ifAdminStatus)) elementsFilter.push(element);
    });

    return elementsFilter;
}

export default function ViewHome({ token, elements, users }: Props) {

    const [filter, setFilter] = useState<string>('Ninguno');
    const [elementsFilter, setElementsFilter] = useState<Element[]>([]);

    const assignInterfaceHandler = async (idElement: string) => {
        const selector = document.getElementById(idElement) as HTMLSelectElement;
        const username = selector.value;
        if (idElement && username) {
            const status = await AdminController.addAssignInterface(token, username, idElement);
            if (status) alert("Interfaz asignada con éxito");
            else alert("Error al asignar la interfaz no asignada");
            location.reload();
        }
    }

    useEffect(() => {
        setElementsFilter(filterData(elements, filter));
    }, [filter]);

    return (
        <div className='h-90 w-full min-h-fit'>
            <header className='w-full h-fit py-2 mb-3 flex flex-row justify-between items-center max-md:flex-col max-md:justify-start max-md:gap-4'>
                <div className='w-fit h-9 rounded-lg flex flex-row flex-nowrap items-center max-md:flex-col max-md:h-fit max-md:w-full'>
                    <h3 className='font-lexend text-white bg-blue-500 font-semibold px-4 py-2 text-nowrap md:rounded-l-md max-md:rounded-t-md max-md:w-full max-md:text-center'>Total de Interfaces</h3>
                    <p className='font-lexend bg-white text-blue-500 px-4 py-2 md:rounded-r-md max-md:rounded-b-md max-md:w-full max-md:text-center'>{elements.length}</p>
                </div>
                <div className='w-fit h-9 rounded-lg flex flex-row flex-nowrap items-center max-md:flex-col max-md:h-fit max-md:w-full'>
                    <button type='button' onClick={() => {location.href = '/admin/assign'}} className='px-4 py-2 bg-blue-500 transition-all duration-300 hover:bg-blue-800 font-lexend text-nowrap text-white rounded-full max-md:w-full'>Asignación Automática</button>
                </div>
                <div className='w-fit h-9 rounded-lg flex flex-row flex-nowrap items-center text-nowrap max-md:flex-col max-md:h-fit max-md:w-full'>
                    <h3 className='font-lexend text-white bg-blue-500 font-semibold px-4 py-2 md:rounded-l-md max-md:rounded-t-md max-md:w-full max-md:text-center'>Filtrar Interfaces por</h3>
                    <select name="filter" id="filter" className='bg-white px-4 py-2 md:rounded-r-md max-md:rounded-b-md max-md:w-full max-md:text-center' onClick={(e) => {setFilter((e.target as HTMLSelectElement).value)}}>
                        <option value="Ninguno">Todo</option>
                        <option value="ifName">Nombre</option>
                        <option value="ifAlias">Alias</option>
                        <option value="ifDescr">Descripción</option>
                        <option value="ifHighSpeed">Capacidad</option>
                        <option value="ifOperStatus">Estatus de Operación</option>
                        <option value="ifAdminStatus">Estatus de Administración</option>
                    </select>
                </div>
            </header>
            {filter == 'Ninguno' && 
                <section id='table' className='h-full max-h-fit w-full overflow-y-scroll bg-white rounded-t-3xl'>
                    <table className='table-fixed w-full max-lg:w-max'>
                        <thead className='font-lexend font-bold text-white text-sm bg-blue-500'>
                            <tr>
                                <th className=' max-lg:px-2 max-sm:text-xs'>IP</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Comunidad</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Nombre</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Alias</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Descripcion</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Capacidad</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Estatus de Operacion</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Estatus de Administracion</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Asignacion</th>
                            </tr>
                        </thead>
                        <tbody>
                            {elements.map((element: Element, index) => (
                                <tr key={index} className='text-sm text-center font-light h-fit'>
                                    <td className='text-nowrap overflow-hidden text-ellipsis py-4 max-sm:text-xs'>{element.current.ip}</td>
                                    <td className='text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>{element.current.community}</td>
                                    {/*NAME*/}
                                    {element.old.ifName && element.current.ifName && element.old.ifName != element.current.ifName && element.old.ifName != "STRING:" && element.current.ifName != "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'>{element.current.ifName}</td>
                                    }
                                    {element.old.ifName && element.current.ifName && ((element.old.ifName != element.current.ifName && element.old.ifName == "STRING:" || element.current.ifName == "STRING:") || (element.old.ifName == element.current.ifName)) &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>{element.current.ifName}</td>
                                    }
                                    {!element.old.ifName || !element.current.ifName &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>NO OBTENIDO</td>
                                    }

                                    {/*ALIAS*/}
                                    {element.old.ifAlias && element.current.ifAlias && element.old.ifAlias != element.current.ifAlias && element.old.ifAlias != "STRING:" && element.current.ifAlias != "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'>{element.current.ifAlias}</td>
                                    }
                                    {element.old.ifAlias && element.current.ifAlias && ((element.old.ifAlias != element.current.ifAlias && element.old.ifAlias == "STRING:" || element.current.ifAlias == "STRING:") || (element.old.ifAlias == element.current.ifAlias)) &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>{element.current.ifAlias}</td>
                                    }
                                    {!element.old.ifAlias && !element.current.ifAlias && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>NO OBTENIDO</td>
                                    }

                                    {/*DESCR*/}
                                    {element.old.ifDescr && element.current.ifDescr && element.old.ifDescr != element.current.ifDescr && element.old.ifDescr != "STRING:" && element.current.ifDescr != "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'>{element.current.ifDescr}</td>
                                    }
                                    {element.old.ifDescr && element.current.ifDescr && ((element.old.ifDescr != element.current.ifDescr && element.old.ifDescr == "STRING:" || element.current.ifDescr == "STRING:") || (element.old.ifDescr == element.current.ifDescr)) &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>{element.current.ifDescr}</td>
                                    }
                                    {!element.old.ifDescr || !element.current.ifDescr && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>NO OBTENIDO</td>
                                    }

                                    {/*HIGHSPEED*/}
                                    {element.old.ifHighSpeed && element.current.ifHighSpeed && element.old.ifHighSpeed != element.current.ifHighSpeed && element.old.ifHighSpeed != "Gauge32:" && element.current.ifHighSpeed != "Gauge32:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'>{element.current.ifHighSpeed}</td>
                                    }
                                    {element.old.ifHighSpeed && element.current.ifHighSpeed && ((element.old.ifHighSpeed != element.current.ifHighSpeed && element.old.ifHighSpeed == "Gauge32:" || element.current.ifHighSpeed == "Gauge32:") || (element.old.ifHighSpeed == element.current.ifHighSpeed)) &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>{element.current.ifHighSpeed}</td>
                                    }
                                    {!element.old.ifHighSpeed || !element.current.ifHighSpeed && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>NO OBTENIDO</td>
                                    }

                                    {/*OPERSTATUS*/}
                                    {element.old.ifOperStatus && element.current.ifOperStatus && element.old.ifOperStatus != element.current.ifOperStatus && element.old.ifOperStatus != "INTEGER:" && element.current.ifOperStatus != "INTEGER:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'>{element.current.ifOperStatus}</td>
                                    }
                                    {element.old.ifOperStatus && element.current.ifOperStatus && ((element.old.ifOperStatus != element.current.ifOperStatus && element.old.ifOperStatus == "INTEGER:" || element.current.ifOperStatus == "INTEGER:") || (element.old.ifOperStatus == element.current.ifOperStatus)) &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>{element.current.ifOperStatus}</td>
                                    }
                                    {!element.old.ifOperStatus || !element.current.ifOperStatus && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>NO OBTENIDO</td>
                                    }

                                    {/*ADMINSTATUS*/}
                                    {element.old.ifAdminStatus && element.current.ifAdminStatus && element.old.ifAdminStatus != element.current.ifAdminStatus && element.old.ifAdminStatus != "INTEGER:" && element.current.ifAdminStatus != "INTEGER:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'>{element.current.ifAdminStatus}</td>
                                    }
                                    {element.old.ifAdminStatus && element.current.ifAdminStatus && ((element.old.ifAdminStatus != element.current.ifAdminStatus && element.old.ifAdminStatus == "INTEGER:" || element.current.ifAdminStatus == "INTEGER:") || (element.old.ifAdminStatus == element.current.ifAdminStatus)) &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>{element.current.ifAdminStatus}</td>
                                    }
                                    {!element.old.ifAdminStatus || !element.current.ifAdminStatus && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>NO OBTENIDO</td>
                                    }

                                    {/*ASIGNACION*/}
                                    <td>
                                        {element.assignment.isAssigned == "false" && 
                                            
                                                <div className='flex gap-2 justify-center'>
                                                    <select className='rounded-md w-60' name="assigment" id="assigment">
                                                        <option value="">----</option>
                                                        {users && users.map((user: UserModel, index) => {
                                                            return(<option key={index} id={element.id} value={user.username} className='text-sm'>{user.name} {user.lastname}</option>)
                                                        })}
                                                    </select>
                                                    <button onClick={() => {assignInterfaceHandler(element.id)}} className='bg-blue-500 rounded-md p-2 text-white font-lexend font-medium transition-all duration-300 ease-in-out hover:bg-green-500'>
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" className="bi bi-check-lg" viewBox="0 0 16 16">
                                                            <path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425z"/>
                                                        </svg>
                                                    </button>
                                                </div>
                                            
                                        }
                                        {element.assignment.isAssigned == "true" &&
                                            <h5 className='font-semibold text-green-800'>Asignado</h5>
                                        }
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </section>
            }
            {filter != 'Ninguno' && elementsFilter.length <= 0 &&
                <section id='table' className='h-full w-full bg-white rounded-t-3xl'>
                    <div className='h-full w-full bg-gray-500 flex flex-col justify-center items-center rounded-t-3xl p-4'>
                        <img src="/assets/check.png" alt="" className='w-14 py-4' />
                        <h2 className='text-center text-gray-800 text-xl font-lexend'>No hay elementos que coincidan con tu búsqueda</h2>
                    </div>
                </section>
            }
            {filter != 'Ninguno' && elementsFilter.length > 0 &&
                <section id='table' className='h-full w-full overflow-y-scroll bg-white rounded-t-3xl'>
                    <table className='table-fixed w-full max-lg:w-max'>
                        <thead className='font-lexend font-bold text-white text-sm bg-blue-500'>
                            <tr>
                                <th className=' max-lg:px-2 max-sm:text-xs'>IP</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Comunidad</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Nombre</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Alias</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Descripcion</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Capacidad</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Estatus de Operacion</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Estatus de Administracion</th>
                                <th className=' max-lg:px-2 max-sm:text-xs'>Asignacion</th>
                            </tr>
                        </thead>
                        <tbody>
                            {elementsFilter.map((element: Element, index) => (
                                <tr key={index} className='text-sm text-center font-light'>
                                    <td className='text-nowrap overflow-hidden text-ellipsis py-4 max-sm:text-xs'>{element.current.ip}</td>
                                    <td className='text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>{element.current.community}</td>
                                    {/*NAME*/}
                                    {element.old.ifName && element.current.ifName && element.old.ifName != element.current.ifName && element.old.ifName != "STRING:" && element.current.ifName != "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'>{element.current.ifName}</td>
                                    }
                                    {element.old.ifName && element.current.ifName && ((element.old.ifName != element.current.ifName && element.old.ifName == "STRING:" || element.current.ifName == "STRING:") || (element.old.ifName == element.current.ifName)) &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>{element.current.ifName}</td>
                                    }
                                    {!element.old.ifName || !element.current.ifName &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>NO OBTENIDO</td>
                                    }

                                    {/*ALIAS*/}
                                    {element.old.ifAlias && element.current.ifAlias && element.old.ifAlias != element.current.ifAlias && element.old.ifAlias != "STRING:" && element.current.ifAlias != "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'>{element.current.ifAlias}</td>
                                    }
                                    {element.old.ifAlias && element.current.ifAlias && ((element.old.ifAlias != element.current.ifAlias && element.old.ifAlias == "STRING:" || element.current.ifAlias == "STRING:") || (element.old.ifAlias == element.current.ifAlias)) &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>{element.current.ifAlias}</td>
                                    }
                                    {!element.old.ifAlias && !element.current.ifAlias && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>NO OBTENIDO</td>
                                    }

                                    {/*DESCR*/}
                                    {element.old.ifDescr && element.current.ifDescr && element.old.ifDescr != element.current.ifDescr && element.old.ifDescr != "STRING:" && element.current.ifDescr != "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'>{element.current.ifDescr}</td>
                                    }
                                    {element.old.ifDescr && element.current.ifDescr && ((element.old.ifDescr != element.current.ifDescr && element.old.ifDescr == "STRING:" || element.current.ifDescr == "STRING:") || (element.old.ifDescr == element.current.ifDescr)) &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>{element.current.ifDescr}</td>
                                    }
                                    {!element.old.ifDescr || !element.current.ifDescr && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>NO OBTENIDO</td>
                                    }

                                    {/*HIGHSPEED*/}
                                    {element.old.ifHighSpeed && element.current.ifHighSpeed && element.old.ifHighSpeed != element.current.ifHighSpeed && element.old.ifHighSpeed != "Gauge32:" && element.current.ifHighSpeed != "Gauge32:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'>{element.current.ifHighSpeed}</td>
                                    }
                                    {element.old.ifHighSpeed && element.current.ifHighSpeed && ((element.old.ifHighSpeed != element.current.ifHighSpeed && element.old.ifHighSpeed == "Gauge32:" || element.current.ifHighSpeed == "Gauge32:") || (element.old.ifHighSpeed == element.current.ifHighSpeed)) &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>{element.current.ifHighSpeed}</td>
                                    }
                                    {!element.old.ifHighSpeed || !element.current.ifHighSpeed && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>NO OBTENIDO</td>
                                    }

                                    {/*OPERSTATUS*/}
                                    {element.old.ifOperStatus && element.current.ifOperStatus && element.old.ifOperStatus != element.current.ifOperStatus && element.old.ifOperStatus != "INTEGER:" && element.current.ifOperStatus != "INTEGER:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'>{element.current.ifOperStatus}</td>
                                    }
                                    {element.old.ifOperStatus && element.current.ifOperStatus && ((element.old.ifOperStatus != element.current.ifOperStatus && element.old.ifOperStatus == "INTEGER:" || element.current.ifOperStatus == "INTEGER:") || (element.old.ifOperStatus == element.current.ifOperStatus)) &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>{element.current.ifOperStatus}</td>
                                    }
                                    {!element.old.ifOperStatus || !element.current.ifOperStatus && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>NO OBTENIDO</td>
                                    }

                                    {/*ADMINSTATUS*/}
                                    {element.old.ifAdminStatus && element.current.ifAdminStatus && element.old.ifAdminStatus != element.current.ifAdminStatus && element.old.ifAdminStatus != "INTEGER:" && element.current.ifAdminStatus != "INTEGER:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'>{element.current.ifAdminStatus}</td>
                                    }
                                    {element.old.ifAdminStatus && element.current.ifAdminStatus && ((element.old.ifAdminStatus != element.current.ifAdminStatus && element.old.ifAdminStatus == "INTEGER:" || element.current.ifAdminStatus == "INTEGER:") || (element.old.ifAdminStatus == element.current.ifAdminStatus)) &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>{element.current.ifAdminStatus}</td>
                                    }
                                    {!element.old.ifAdminStatus || !element.current.ifAdminStatus && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'>NO OBTENIDO</td>
                                    }

                                    {/*ASIGNACION*/}
                                    <td>
                                        {element.assignment.isAssigned == "false" && 
                                            
                                                <div className='flex gap-2 justify-center'>
                                                    <select className='rounded-md w-60 px-2' name="assigment" id="assigment">
                                                        <option value="">----</option>
                                                        {users && users.map((user: UserModel, index) => {
                                                            return(<option key={index} id={element.id} value={user.username} className='text-sm'>{user.name} {user.lastname}</option>)
                                                        })}
                                                    </select>
                                                    <button onClick={() => {assignInterfaceHandler(element.id)}} className='bg-blue-500 rounded-md p-2 text-white font-lexend font-medium transition-all duration-300 ease-in-out hover:bg-green-500'>
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" className="bi bi-check-lg" viewBox="0 0 16 16">
                                                            <path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425z"/>
                                                        </svg>
                                                    </button>
                                                </div>
                                            
                                        }
                                        {element.assignment.isAssigned == "true" &&
                                            <h5 className='font-semibold text-green-800'>Asignado</h5>
                                        }
                                    </td>                                        
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </section>
            }
        </div>
    );
}