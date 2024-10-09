import type { Element } from '../../models/element';
import type { UserModel } from '../../models/user';
import { useEffect, useState } from 'react';
import { Zoom } from 'react-awesome-reveal';

interface Props {
    token: string;
    elements: Element[];
    user: UserModel;
}

function filterData(elements: Element[], filter: string): Element[] {
    let elementsFilter: Element[] = [];

    elements.map((element: Element) => {
        if ((filter == 'ifName') && (element.old.ifName != element.current.ifName)) elementsFilter.push(element);
        else if ((filter == 'ifAlias') && (element.old.ifAlias != element.current.ifAlias)) elementsFilter.push(element);
        else if ((filter == 'ifHighSpeed') && (element.old.ifHighSpeed!= element.current.ifHighSpeed)) elementsFilter.push(element);
        else if ((filter == 'ifOperStatus') && (element.old.ifOperStatus!= element.current.ifOperStatus)) elementsFilter.push(element);
        else if ((filter == 'ifAdminStatus') && (element.old.ifAdminStatus!= element.current.ifAdminStatus)) elementsFilter.push(element);
    });

    return elementsFilter;
}

export default function ContainerHome({ token, elements, user }: Props) {

    const [filter, setFilter] = useState<string>('Ninguno');
    const [elementsFilter, setElementsFilter] = useState<Element[]>([]);

    useEffect(() => {
        setElementsFilter(filterData(elements, filter));
    }, [filter]);

    return (
        <div className='h-80vh w-full'>
            <header className='w-full h-fit mb-2 flex flex-row justify-between items-center max-sm:flex-col max-sm:justify-start max-sm:gap-4'>
                <div className='w-fit h-9 rounded-lg flex flex-row flex-nowrap items-center max-sm:flex-col max-sm:h-fit max-sm:w-full'>
                    <h3 className='font-lexend text-white bg-blue-500 font-semibold px-4 py-2 md:rounded-l-md max-sm:rounded-t-md max-sm:w-full max-sm:text-center'>Total de Interfaces</h3>
                    <p className='font-lexend bg-white text-blue-500 px-4 py-2 md:rounded-r-md max-sm:rounded-b-md max-sm:w-full max-sm:text-center'>{elements.length}</p>
                </div>
                <div className='w-fit h-9 rounded-lg flex flex-row flex-nowrap items-center max-sm:flex-col max-sm:h-fit max-sm:w-full'>
                    <h3 className='font-lexend text-white bg-blue-500 font-semibold px-4 py-2 md:rounded-l-md max-sm:rounded-t-md max-sm:w-full max-sm:text-center'>Filtrar Interfaces por</h3>
                    <select name="filter" id="filter" className='bg-white px-4 py-2 md:rounded-r-md max-sm:rounded-b-md max-sm:w-full max-sm:text-center' onClick={(e) => {setFilter((e.target as HTMLSelectElement).value)}}>
                        <option value="Ninguno">----</option>
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
                <section id='table' className='h-95 w-full overflow-y-scroll bg-white rounded-t-3xl'>
                    <table className='table-fixed w-full max-lg:w-max'>
                        <thead className='font-lexend font-bold text-white text-sm bg-blue-500'>
                            <tr>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>IP</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Comunidad</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Nombre</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Alias</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Descripcion</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Capacidad</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Estatus de Operacion</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Estatus de Administracion</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Detalles</Zoom></th>
                            </tr>
                        </thead>
                        <tbody>
                            {elements.map((element: Element, index) => (
                                <tr key={index} className='text-sm text-center font-light'>
                                    <td className='text-nowrap overflow-hidden text-ellipsis py-4 max-sm:text-xs'><Zoom>{element.current.ip}</Zoom></td>
                                    <td className='text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.community}</Zoom></td>
                                    {/*NAME*/}
                                    {element.old.ifName != element.current.ifName && element.old.ifName != "STRING:" && element.current.ifName != "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'><Zoom>{element.current.ifName}</Zoom></td>
                                    }
                                    {element.old.ifName != element.current.ifName && element.old.ifName == "STRING:" || element.current.ifName == "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifName}</Zoom></td>
                                    }
                                    {element.old.ifName == element.current.ifName && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifAlias}</Zoom></td>
                                    }
                                    {/*ALIAS*/}
                                    {element.old.ifAlias != element.current.ifAlias && element.old.ifAlias != "STRING:" && element.current.ifAlias != "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'><Zoom>{element.current.ifAlias}</Zoom></td>
                                    }
                                    {element.old.ifAlias != element.current.ifAlias && element.old.ifAlias == "STRING:" || element.current.ifAlias == "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifAlias}</Zoom></td>
                                    }
                                    {element.old.ifAlias == element.current.ifAlias && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifAlias}</Zoom></td>
                                    }
                                    {/*DESCR*/}
                                    {element.old.ifDescr != element.current.ifDescr && element.old.ifDescr != "STRING:" && element.current.ifDescr != "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'><Zoom>{element.current.ifDescr}</Zoom></td>
                                    }
                                    {element.old.ifDescr != element.current.ifDescr && element.old.ifDescr == "STRING:" || element.current.ifDescr == "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifDescr}</Zoom></td>
                                    }
                                    {element.old.ifDescr == element.current.ifDescr && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifDescr}</Zoom></td>
                                    }
                                    {/*HIGHSPEED*/}
                                    {element.old.ifHighSpeed != element.current.ifHighSpeed && element.old.ifHighSpeed != "Gauge32:" && element.current.ifHighSpeed != "Gauge32:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'><Zoom>{element.current.ifHighSpeed}</Zoom></td>
                                    }
                                    {element.old.ifHighSpeed != element.current.ifHighSpeed && element.old.ifHighSpeed == "Gauge32:" || element.current.ifHighSpeed == "Gauge32:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifHighSpeed}</Zoom></td>
                                    }
                                    {element.old.ifHighSpeed == element.current.ifHighSpeed && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifHighSpeed}</Zoom></td>
                                    }
                                    {/*OPERSTATUS*/}
                                    {element.old.ifOperStatus != element.current.ifOperStatus && element.old.ifOperStatus != "INTEGER:" && element.current.ifOperStatus != "INTEGER:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'><Zoom>{element.current.ifOperStatus}</Zoom></td>
                                    }
                                    {element.old.ifOperStatus != element.current.ifOperStatus && element.old.ifOperStatus == "INTEGER:" || element.current.ifOperStatus == "INTEGER:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifOperStatus}</Zoom></td>
                                    }
                                    {element.old.ifOperStatus == element.current.ifOperStatus && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifOperStatus}</Zoom></td>
                                    }
                                    {/*ADMINSTATUS*/}
                                    {element.old.ifAdminStatus != element.current.ifAdminStatus && element.old.ifAdminStatus != "INTEGER:" && element.current.ifAdminStatus != "INTEGER:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'><Zoom>{element.current.ifAdminStatus}</Zoom></td>
                                    }
                                    {element.old.ifAdminStatus != element.current.ifAdminStatus && element.old.ifAdminStatus == "INTEGER:" || element.current.ifAdminStatus == "INTEGER:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifAdminStatus}</Zoom></td>
                                    }
                                    {element.old.ifAdminStatus == element.current.ifAdminStatus && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifAdminStatus}</Zoom></td>
                                    }
                                    {/*DETALLES*/}
                                    <td>
                                        <Zoom><button className='w-fit py-2 px-6 font-lexend font-semibold text-white bg-blue-500 rounded-3xl transition-all duration-300 ease-in-out hover:bg-red-500' onClick={() => {location.href = `/detalle/${element.id}`}}>Detalle</button></Zoom>
                                    </td>
                                    
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </section>
            }
            {filter != 'Ninguno' && elementsFilter.length <= 0 &&
                <section id='table' className='h-95 w-full bg-white rounded-t-3xl'>
                    <div className='h-full w-full bg-gray-500 flex flex-col justify-center items-center rounded-t-3xl p-4'>
                        <img src="/assets/check.png" alt="" className='w-14 py-4' />
                        <h2 className='text-center text-gray-800 text-xl font-lexend'>No hay elementos que coincidan con tu búsqueda</h2>
                    </div>
                </section>
            }
            {filter != 'Ninguno' && elementsFilter.length > 0 &&
                <section id='table' className='h-95 w-full overflow-y-scroll bg-white rounded-t-3xl'>
                    <table className='table-fixed w-full max-lg:w-max'>
                        <thead className='font-lexend font-bold text-white text-sm bg-blue-500'>
                            <tr>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>IP</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Comunidad</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Nombre</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Alias</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Descripcion</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Capacidad</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Estatus de Operacion</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Estatus de Administracion</Zoom></th>
                                <th className=' max-lg:px-2 max-sm:text-xs'><Zoom>Asignacion</Zoom></th>
                            </tr>
                        </thead>
                        <tbody>
                            {elementsFilter.map((element: Element, index) => (
                                <tr key={index} className='text-sm text-center font-light'>
                                    <td className='text-nowrap overflow-hidden text-ellipsis py-4 max-sm:text-xs'><Zoom>{element.current.ip}</Zoom></td>
                                    <td className='text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.community}</Zoom></td>
                                    {/*NAME*/}
                                    {element.old.ifName != element.current.ifName && element.old.ifName != "STRING:" && element.current.ifName != "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'><Zoom>{element.current.ifName}</Zoom></td>
                                    }
                                    {element.old.ifName != element.current.ifName && element.old.ifName == "STRING:" || element.current.ifName == "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifName}</Zoom></td>
                                    }
                                    {element.old.ifName == element.current.ifName && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifAlias}</Zoom></td>
                                    }
                                    {/*ALIAS*/}
                                    {element.old.ifAlias != element.current.ifAlias && element.old.ifAlias != "STRING:" && element.current.ifAlias != "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'><Zoom>{element.current.ifAlias}</Zoom></td>
                                    }
                                    {element.old.ifAlias != element.current.ifAlias && element.old.ifAlias == "STRING:" || element.current.ifAlias == "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifAlias}</Zoom></td>
                                    }
                                    {element.old.ifAlias == element.current.ifAlias && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifAlias}</Zoom></td>
                                    }
                                    {/*DESCR*/}
                                    {element.old.ifDescr != element.current.ifDescr && element.old.ifDescr != "STRING:" && element.current.ifDescr != "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'><Zoom>{element.current.ifDescr}</Zoom></td>
                                    }
                                    {element.old.ifDescr != element.current.ifDescr && element.old.ifDescr == "STRING:" || element.current.ifDescr == "STRING:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifDescr}</Zoom></td>
                                    }
                                    {element.old.ifDescr == element.current.ifDescr && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifDescr}</Zoom></td>
                                    }
                                    {/*HIGHSPEED*/}
                                    {element.old.ifHighSpeed != element.current.ifHighSpeed && element.old.ifHighSpeed != "Gauge32:" && element.current.ifHighSpeed != "Gauge32:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'><Zoom>{element.current.ifHighSpeed}</Zoom></td>
                                    }
                                    {element.old.ifHighSpeed != element.current.ifHighSpeed && element.old.ifHighSpeed == "Gauge32:" || element.current.ifHighSpeed == "Gauge32:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifHighSpeed}</Zoom></td>
                                    }
                                    {element.old.ifHighSpeed == element.current.ifHighSpeed && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifHighSpeed}</Zoom></td>
                                    }
                                    {/*OPERSTATUS*/}
                                    {element.old.ifOperStatus != element.current.ifOperStatus && element.old.ifOperStatus != "INTEGER:" && element.current.ifOperStatus != "INTEGER:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'><Zoom>{element.current.ifOperStatus}</Zoom></td>
                                    }
                                    {element.old.ifOperStatus != element.current.ifOperStatus && element.old.ifOperStatus == "INTEGER:" || element.current.ifOperStatus == "INTEGER:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifOperStatus}</Zoom></td>
                                    }
                                    {element.old.ifOperStatus == element.current.ifOperStatus && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifOperStatus}</Zoom></td>
                                    }
                                    {/*ADMINSTATUS*/}
                                    {element.old.ifAdminStatus != element.current.ifAdminStatus && element.old.ifAdminStatus != "INTEGER:" && element.current.ifAdminStatus != "INTEGER:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis text-red-500 max-sm:text-xs'><Zoom>{element.current.ifAdminStatus}</Zoom></td>
                                    }
                                    {element.old.ifAdminStatus != element.current.ifAdminStatus && element.old.ifAdminStatus == "INTEGER:" || element.current.ifAdminStatus == "INTEGER:" &&
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifAdminStatus}</Zoom></td>
                                    }
                                    {element.old.ifAdminStatus == element.current.ifAdminStatus && 
                                        <td className='py-2 text-nowrap overflow-hidden text-ellipsis max-sm:text-xs'><Zoom>{element.current.ifAdminStatus}</Zoom></td>
                                    }
                                    {/*DETALLES*/}
                                    <td>
                                        <Zoom><button className='w-fit py-2 px-6 font-lexend font-semibold text-white bg-blue-500 rounded-3xl transition-all duration-300 ease-in-out hover:bg-red-500' onClick={() => {location.href = `/detalle/${element.id}`}}>Detalle</button></Zoom>
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