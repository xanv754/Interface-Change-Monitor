'use client';

import SelectorForm from '@components/form/select';
import InputTextForm from '@components/form/input';
import InterfaceAssignedCard from '@/app/components/card/assigned';
import InterfaceAssignCard from '../components/card/assign';
import { Login } from '@/controllers/login';
import { User } from '@/controllers/myUser';
import { ChangeSchema } from '@/schemas/changes';
import { UserSchema } from '@/schemas/user';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Test() {
  const router = useRouter();

  const operatorExample: UserSchema = {
    username: 'unittest',
    name: 'Unit',
    lastname: 'Test',
    password: null,
    profile: 'ADMIN',
    account: 'ACTIVE',
    createdAt: '2023-01-01',
  };

  const changeExample: ChangeSchema = {
    ip: '192.168.1.1',
    community: 'public',
    sysname: 'switch',
    ifIndex: 1,
    oldInteface: {
      id: 1,
      date: '2023-01-01',
      ifName: 'eth0',
      ifDescr: 'eth0 interface',
      ifAlias: 'eth0',
      ifSpeed: 1000,
      ifHighSpeed: 1000,
      ifPhysAddress: '00:00:00:00:00:00',
      ifType: 'ethernet',
      ifOperStatus: 'up',
      ifAdminStatus: 'up',
      ifPromiscuousMode: false,
      ifConnectorPresent: true,
      ifLastChange: '2023-01-01',
    },
    newInteface: {
      id: 1,
      date: '2023-01-02',
      ifName: 'ethasdaslkdhasdklahsdjhajkdasjkdhasjkdkshdjkasdkajsdhjkasd0',
      ifDescr: 'eth0 interface',
      ifAlias: 'eth0',
      ifSpeed: 1000,
      ifHighSpeed: 1000,
      ifPhysAddress: '00:00:00:00:00:00',
      ifType: 'ethernet',
      ifOperStatus: 'up',
      ifAdminStatus: 'up',
      ifPromiscuousMode: false,
      ifConnectorPresent: true,
      ifLastChange: '2023-01-01',
    },
  };

  const inputContent = (value: string) => {
    console.log(value);
  };

  const validateInput = (value: string) => {
    if (value.length > 5) {
      return true;
    }
    return false;
  };

  const [user, setUser] = useState<UserSchema | null>(null);

  useEffect(() => {
    const dataUser = sessionStorage.getItem('user');
    if (dataUser) {
      const user = JSON.parse(dataUser) as UserSchema;
      if (user) setUser(user);
    }
  }, []);

  return (
    <main className='min-w-fit p-4'>
      {!user &&
        <div>Hello, Stranger!</div>
      }
      {user &&
        <div>Hello, {user.name} {user.lastname}!</div>
      }
      <button onClick={() => router.push('/')} className='bg-blue-700 text-white-50 px-4 py-1 mx-1'>Home</button>
      <h1 className='font-bold'>Selector:</h1>
      <SelectorForm id='testSelector' label='Selector Default' options={['option 1', 'option 2', 'option 3']} /> 
      <h1 className='font-bold'>Input Text:</h1>
      <InputTextForm id='testInput' label='Label Input Text Default Error' type='text' getInput={inputContent} validateInput={validateInput} />
      <h1 className='font-bold'>Change Card (Assigned):</h1>
      <InterfaceAssignedCard data={changeExample} />
      <h1 className='font-bold'>Change Card (Assign):</h1>
      <InterfaceAssignCard data={changeExample} operators={[operatorExample]} />
    </main>
  );
}