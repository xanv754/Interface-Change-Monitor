import { ElementController } from '../../controllers/element.controller';
import { AdminController } from '../../controllers/admin.controller';
import styles from '../../styles/spinner.module.css';
import type { Element } from '../../models/element';
import type { UserModel } from '../../models/user';
import ContainerProfile from './ViewProfile';
import ContainerHistory from './ViewHistory';
import ContainerNotices from './ViewNotices';
import { useState, useEffect } from 'react';
import ContainerAssign from './ViewAssign';
import Footer from '../../layouts/Footer';
import ContainerUsers from './ViewUsers';
import ContainerHome from './ViewHome';
import ContainerData from './ViewData';

interface Props {
    token: string;
    container: string;
}

export default function Loading({ token, container }: Props) {
    const [elements, setElements] = useState<Element[]>([]);
    const [users, setUsers] = useState<UserModel[]>([]);
    const [error, setError] = useState<boolean>(false);
    const [isLoading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        const getData = async () => {
            const elements = await ElementController.getElementsToday(token);
            if (!elements) setError(true);
            else setElements(elements);

            const users = await AdminController.getUsers(token);
            if (!users) setError(true);
            else setUsers(users);
            
            setLoading(false);
        }
        getData();
    }, []);

    return (
        <div id="container" className='min-h-fit h-80vh max-h-fit w-full max-md:h-fit'>
            <article className='min-h-fit h-full w-full rounded-t-3xl shadow-md max-md:h-fit'>
                {isLoading && 
                    <div className='flex h-80vh mt-4 w-full bg-blue-500 rounded-t-3xl flex-col justify-center items-center'>
                        <div className={styles.spinner}></div>
                    </div>
                }
                {!isLoading && error &&
                    <div className='flex h-80vh w-full flex-col bg-gray-100 mt-3 rounded-t-3xl justify-center items-center max-sm:py-4'>
                        <img src="/assets/error.png" alt="" className='w-14 py-4' />
                        <h2 className='text-black-100 font-bold text-3xl max-sm:text-lg'>Error al cargar la información</h2>
                    </div>
                }
                {/* TABLE OF ASSIGMENTS */}
                {!isLoading && !error && container == 'Table' && elements.length <= 0 &&
                    <div className='flex h-80vh w-full flex-col bg-gray-100 rounded-t-3xl mt-2 justify-center items-center max-sm:py-4'>
                        <img src="/assets/check.png" alt="" className='w-14 py-4' />
                        <h2 className='text-black-100 font-bold text-3xl max-sm:text-lg'>Sin cambios</h2>
                        <h3 className='text-black-100 max-sm:text-sm'>No se han detectado cambios nuevos en las interfaces</h3>
                    </div>
                }
                {!isLoading && !error && container == 'Table' && elements.length > 0 &&
                    <ContainerHome token={token} elements={elements} users={users} />
                }
                {/* HISTORY - STATICS*/}
                {!isLoading && !error && container == 'History' &&
                    <ContainerHistory token={token} elements={elements} users={users}/>
                }
                {/* DATA - REGISTER */}
                {!isLoading && !error && container == 'Data' &&
                    <ContainerData elements={elements} users={users}/>
                }
                {/* NOTIFICATIONS */}
                {!isLoading && !error && container == 'Notices' &&
                    <ContainerNotices token={token} />
                }
                {/* PROFILE */}
                {!isLoading && !error && container == 'Profile' &&
                    <ContainerProfile token={token} />
                }
                {/* USERS ADMINISTRARION */}
                {!isLoading && !error && container == 'Users' &&
                    <ContainerUsers token={token} />
                }
                {/* ASSIGNMENT MULTIPLE */}
                {!isLoading && !error && container == 'Assign' &&
                    <ContainerAssign token={token} users={users} />
                }                
            </article>
            <Footer />
        </div>
    );
}