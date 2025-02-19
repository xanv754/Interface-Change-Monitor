'use client';

import { useEffect, useState, createContext } from 'react';
import { User } from '@/controllers/myUser';
import { UserSchema } from '@/schemas/user';
import { TokenSchema } from '@/schemas/token';
import { useRouter } from 'next/navigation';

export default function Home() {
  
  const router = useRouter();

  const handleLogout = () => {
    sessionStorage.removeItem('user');
  };

  const handleLogin = async () => {
    const user = new User('unittest', 'test123');
    
    const credentials = await user.login();
    if (credentials) {
      const data = await user.myInfo(credentials.access_token);
      if (data) {
        sessionStorage.setItem('user', JSON.stringify(data));
      }
    }
  }

  useEffect(() => {
    sessionStorage.clear();
  }, []);

  return (
    <div>
      <h1>Hello World!</h1>
      <button onClick={handleLogin} className='bg-blue-700 text-white-50 px-4 py-1 mx-1'>Iniciar Sesión</button>
      <button onClick={handleLogout} className='bg-blue-700 text-white-50 px-4 py-1 mx-1'>Cerrar Sesión</button>
      <h3>Menu:</h3>
      <button onClick={() => router.push('/test')} className='bg-blue-700 text-white-50 px-4 py-1 mx-1'>Test</button>
    </div>
  );
}