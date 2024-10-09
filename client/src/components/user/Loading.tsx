import { ElementController } from '../../controllers/element.controller';
import { assignmentStatus } from '../../../constants/assigmentStatus';
import styles from '../../styles/spinner.module.css';
import type { Element } from '../../models/element';
import type { UserModel } from '../../models/user';
import ContainerHistory from './ViewHistory';
import { useState, useEffect } from 'react';
import Footer from '../../layouts/Footer';
import ContainerHome from './ViewHome';

interface Props {
    token: string;
    container: string;
    user: UserModel;
}

function filterInterfacesAssigned(elements: Element[]): Element[] {
    let elementsFilter: Element[] = [];
    elements.map((element: Element) => {
        if (element.assignment.status == assignmentStatus.pending) elementsFilter.push(element);
    })  
    return elementsFilter;
}

export default function Loading({ token, container, user }: Props) {
    const [error, setError] = useState<boolean>(false);
    const [elements, setElements] = useState<Element[]>([]);
    const [isLoading, setLoading] = useState<boolean>(true);
    
    useEffect(() => {
        const getElementsUser = async () => {
            let elementsUser = await ElementController.getElementsByUser(token, user.username);
            if (!elementsUser) setError(true);
            else {
                elementsUser = filterInterfacesAssigned(elementsUser);
                setElements(elementsUser);
            }
            setLoading(false);
        }

        getElementsUser();
    }, []);

    return (
        <div className='min-h-fit h-80vh w-full max-md:h-fit'>
            <section className='min-h-fit max-h-fit w-full rounded-t-3xl shadow-md max-md:h-fit'>
                {isLoading && 
                    <div className='flex h-80vh w-full mt-4 bg-blue-500 rounded-t-3xl flex-col justify-center items-center'>
                        <div className={styles.spinner}></div>
                    </div>
                }
                {!isLoading && error &&
                    <div className='flex h-80vh w-full flex-col bg-gray-100 mt-3 rounded-t-3xl justify-center items-center'>
                        <img src="/assets/error.png" alt="" className='w-14 py-4' />
                        <h2 className='text-black-100 font-bold text-3xl max-sm:text-lg'>Error al obtener la información</h2>
                    </div>
                }
                {!isLoading && !error && !user &&
                    <div className='flex h-80vh w-full flex-col bg-gray-100 mt-3 rounded-t-3xl justify-center items-center'>
                        <img src="/assets/error.png" alt="" className='w-14 py-4' />
                        <h2 className='text-black-100 font-bold text-3xl max-sm:text-lg'>Información de usuario  no obtenida</h2>
                    </div>
                }
                {!isLoading && !error && user && container == 'Home' && elements.length <= 0 &&
                    <div className='flex h-80vh w-full flex-col bg-gray-100 rounded-t-3xl justify-center items-center'>
                        <img src="/assets/check.png" alt="" className='w-14 py-4' />
                        <h2 className='text-black-100 font-bold text-3xl max-sm:text-lg'>Sin Asignación</h2>
                        <h3 className='text-black-100 max-sm:text-sm'>No tiene interfaces asignadas</h3>
                    </div>
                }
                {!isLoading && !error && user && container == 'Home' && elements.length > 0 && 
                    <ContainerHome token={token} elements={elements} user={user} />
                }
                {!isLoading && !error && user && container == 'History' &&
                    <ContainerHistory token={token} user={user} />
                }
            </section>
            <Footer></Footer>
        </div>
    );
}