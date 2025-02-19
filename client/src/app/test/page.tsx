'use client';

import SelectorForm from '@components/form/select';
import InputTextForm from '@components/form/input';
import InterfaceAssignedCard from '@/app/components/card/assigned';
import InterfaceAssignCard from '../components/card/assign';
import { Login } from '@/controllers/login';
import { ChangeSchema } from '@/schemas/changes';
import { OperatorSchema } from '@/schemas/operator';
import { useEffect } from 'react';

export default function Test() {
  const operatorExample: OperatorSchema = {
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

  useEffect(() => {
    const getToken = async () => {
      const res = await Login.getToken('unittest', 'test123');
      console.log("Token:", res?.access_token);
    };
    getToken();
  }, []);

  return (
    <main className='min-w-fit p-4'>
      <div>Hello Test!</div>
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